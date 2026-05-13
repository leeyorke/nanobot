"""
习惯执行记录持久化模块
使用 SQLite 记录每条习惯的每日执行状态，保留历史数据以便统计。
"""
import sqlite3
from datetime import date, timedelta
from pathlib import Path


class HabitTracker:
    def __init__(self, data_dir: Path):
        self.db_path = Path(data_dir) / '.metadata' / 'habits.db'
        self._init_db()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS habit_log (
                date       TEXT NOT NULL,
                name       TEXT NOT NULL,
                status     TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (date, name)
            )
        """)
        conn.commit()
        conn.close()

    def _get_conn(self):
        return sqlite3.connect(str(self.db_path))

    def log_done(self, date_str: str, habit_name: str, timestamp: str):
        """记录习惯已完成"""
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO habit_log (date, name, status, updated_at) VALUES (?, ?, 'done', ?)",
            (date_str, habit_name, timestamp),
        )
        conn.commit()
        conn.close()

    def log_skipped(self, date_str: str, habit_name: str, timestamp: str):
        """记录习惯未完成"""
        conn = self._get_conn()
        conn.execute(
            "INSERT OR REPLACE INTO habit_log (date, name, status, updated_at) VALUES (?, ?, 'skipped', ?)",
            (date_str, habit_name, timestamp),
        )
        conn.commit()
        conn.close()

    def get_done_today(self, date_str: str) -> set[str]:
        """获取某天已完成的习惯名称集合"""
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT name FROM habit_log WHERE date = ? AND status = 'done'",
            (date_str,),
        ).fetchall()
        conn.close()
        return {row[0] for row in rows}

    def get_stats(self, days: int = 30):
        """获取最近 N 天的习惯执行统计

        返回: {习惯名: {total, done, rate, streak}}
        """
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT date, name, status FROM habit_log "
            "WHERE date >= date('now', ?) ORDER BY date",
            (f'-{days} days',),
        ).fetchall()
        conn.close()

        # 按习惯名分组
        habits: dict[str, dict] = {}
        for date_str, name, status in rows:
            h = habits.setdefault(name, {'done_dates': set(), 'skipped_dates': set()})
            if status == 'done':
                h['done_dates'].add(date_str)
            else:
                h['skipped_dates'].add(date_str)

        today = date.today()
        result = {}
        for name, data in habits.items():
            total = len(data['done_dates'] | data['skipped_dates'])
            done = len(data['done_dates'])
            # 连续打卡天数（从今天往回数）
            streak = 0
            check = today
            while check.isoformat() in data['done_dates']:
                streak += 1
                check -= timedelta(days=1)

            result[name] = {
                'total': total,
                'done': done,
                'rate': round(done / total, 2) if total > 0 else 0.0,
                'streak': streak,
            }

        return result
