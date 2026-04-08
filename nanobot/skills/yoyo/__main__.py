#!/usr/bin/env python3
"""
yoyo 私人秘书 - 包入口点
支持 python3 -m nanobot.skills.yoyo 执行
"""
import sys
import asyncio
from pathlib import Path


async def run_handle(message: str):
    """Run the handle function with a minimal context."""
    from nanobot.config.loader import load_config
    from .main import handle

    config = load_config()

    # Minimal context for handle function
    skill_ctx = {
        'config': config,
        'send_message': lambda content: print(content),
        'loop': None
    }

    result = await handle(message, skill_ctx)
    if result:
        print(result)


def main():
    import argparse

    parser = argparse.ArgumentParser(prog="nanobot yoyo")
    parser.add_argument("--handle", help="处理用户消息", dest="handle")
    parser.set_defaults(handle=None)

    args = parser.parse_args()

    if args.handle:
        # Run handle function
        asyncio.run(run_handle(args.handle))
        return 0

    # Fall back to CLI mode
    from .cli import main as cli_main
    sys.argv = ["nanobot", *sys.argv[1:]]
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())
