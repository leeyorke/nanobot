# Common Gotchas

## Do not use `ruff format`

`CONTRIBUTING.md` mentions `ruff format`, but **do not run it** — it destroys git blame history. Only `ruff check` should be used.

## Config `${VAR}` References

`config/loader.py` resolves `${VAR}` patterns in `config.json` at load time. This is **not** a shell-like default-value syntax. If the environment variable is missing, `load_config` raises `ValueError` and the agent falls back to default configuration.

Example valid usage:
```json
{ "providers": { "openrouter": { "apiKey": "${OPENROUTER_KEY}" } } }
```

## Windows Compatibility

nanobot explicitly supports Windows. Key differences to keep in mind:
- `ExecTool` uses `cmd /c` on Windows instead of `sh -c` (`shell.py`).
- `cli/commands.py` forces `sys.stdout`/`stderr` to UTF-8 on startup to handle emoji and multilingual input.
- MCP stdio server commands are normalized for Windows path separators (`mcp.py`).
- Always use `pathlib.Path` for path manipulation; do not assume `/` separators.

## Prompt Templates

Agent system prompts and scenario-specific instructions live in `nanobot/templates/` as Jinja2 markdown files (`identity.md`, `platform_policy.md`, `HEARTBEAT.md`, `SOUL.md`, etc.). Changing these files alters agent behavior as directly as changing Python code. They are loaded by `utils/prompt_templates.py`.

Tool descriptions, skills, and replayed session history also shape model behavior. Treat changes to those surfaces like runtime code: keep them narrow, add a focused regression test when possible, and avoid teaching the model to repeat internal markers, local paths, or tool-call text.

## Context Pollution Persists

Anything written into memory, session history, or prompt inputs can be replayed into future LLM calls. Metadata such as timestamps, local media paths, tool-call echoes, and raw fallback dumps must be bounded and sanitized before they become examples for the model to imitate.

## Skills as Extension Point

Built-in skills live in `nanobot/skills/` (markdown + YAML frontmatter format). Agent capabilities that are "know-how" rather than code should be added as skills, not hardcoded into the agent loop. External skills can be published to and installed from ClawHub.

## Atomic Session Writes

`agent/memory.py` writes `history.jsonl` atomically (temp file + fsync + rename + directory fsync). This guarantees durability across crashes. Do not replace this with a plain `open(..., "w")` write.

## MCP Handshake Failures Are `BaseException`s

When an MCP server rejects the handshake (401/403 from a wrong token, closed socket, ...), the MCP SDK's `anyio` task group tears down its cancel scope from the *wrong task*. What our coroutine receives is a `CancelledError` named after that scope or a `BaseExceptionGroup` wrapping one — both inherit from `BaseException`, so a plain `except Exception` does not catch them and they escape into the agent loop, crashing the gateway.

Guard the handshake in `agent/tools/mcp.py` with `_is_mcp_sdk_cancellation()` and only swallow that specific leak: an externally requested cancellation (`task.cancel()`) yields a `CancelledError` with an empty message and must be re-raised so `/stop` and shutdown still work.

Do not add a pre-flight HTTP auth probe to detect a bad token early. It duplicates the `initialize` request the server receives and changes the observable request sequence covered by the SSRF/redirect tests in `tests/tools/test_mcp_tool.py`. Detect it once, at the handshake.

## `CancelledError` Also Leaks Into the MCP Health Probe

The same cancel-scope teardown can land in `AgentLoop._mcp_health_check()`. `_probe_http_url` wraps `open_connection` in `asyncio.wait_for`, and its teardown re-raises *any* pending cancellation — including a leftover MCP-sdk/anyio scope — as `CancelledError("Cancelled via cancel scope ... by <Task ...>")`. That escaped `run()`'s `except TimeoutError` branch and crashed the gateway during shutdown.

So `except CancelledError: raise` is not automatically the right code. Discriminate with `_is_mcp_sdk_cancellation()` before deciding to propagate: a real `task.cancel()` yields an empty message and must still abort the loop, otherwise `/stop` and gateway shutdown stop working.

Note that `loop.py` binds MCP helpers at import time (`from nanobot.agent.tools.mcp import _probe_http_url`), so tests must patch `nanobot.agent.loop._probe_http_url`, not the definition site.

## MCP Work Must Run In Its Own Task

This is the root cause behind the "disabling MCP still crashes" reports, and the fix is structural rather than a series of `except` clauses.

anyio delivers a cancel scope's cancellation by calling `task.cancel()` on whatever task hosts it (`anyio/_backends/_asyncio.py` `_deliver_cancellation()`, re-scheduled via `call_soon`). When the MCP SDK's transport fails or the server rejects the handshake, the scope's host task is the **agent loop's** task — and the `uncancel()` compensation only runs on a clean scope exit, which a cross-task cleanup (`RuntimeError: Attempted to exit cancel scope in a different task`) never reaches. The cancellation is therefore sticky and re-delivered, so *every later* `await` in `AgentLoop.run()` raises again with the same scope id.

Catching it is not enough: the exception being caught does not undo the `task.cancel()`.

So all MCP connection work goes through `_run_mcp_isolated()` in `mcp.py`, which runs each server in a throwaway task. The leak dies with that task. Keep that pattern if you add new MCP calls into the loop — do not `await` an MCP coroutine directly from `AgentLoop.run()`.
