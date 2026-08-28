import json
import os
import sys
from collections import Counter
from datetime import datetime

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


# ==========================================
# ZONE 1: DATA ENGINES
# ==========================================

def load_configs() -> dict:
    with open(os.path.join(DATA_DIR, 'configs.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

def read_tsv(path: str) -> list[tuple[int, str]]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            rows = []
            for line in f:
                line = line.rstrip('\n')
                if not line:
                    continue
                ts, _, value = line.partition('\t')
                if ts.isdigit():
                    rows.append((int(ts), value))
            return rows
    except FileNotFoundError:
        return []

def read_tracking_started(path: str) -> int | None:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return int(content) if content.isdigit() else None
    except FileNotFoundError:
        return None


# ==========================================
# ZONE 2: ORCHESTRATION
# ==========================================

def top_counts(rows: list[tuple[int, str]], top_n: int) -> list[tuple[str, int]]:
    return Counter(value for _, value in rows).most_common(top_n)

def last_seen(rows: list[tuple[int, str]]) -> dict[str, int]:
    seen: dict[str, int] = {}
    for ts, value in rows:
        if value not in seen or ts > seen[value]:
            seen[value] = ts
    return seen

def stale_entries(rows: list[tuple[int, str]], stale_days: int, now: int) -> list[tuple[str, int]]:
    threshold = now - stale_days * 86400
    stale = [(value, ts) for value, ts in last_seen(rows).items() if ts < threshold]
    return sorted(stale, key=lambda item: item[1])

def days_tracked(tracking_started: int | None, now: int) -> int:
    if tracking_started is None:
        return 0
    return max(0, (now - tracking_started) // 86400)


# ==========================================
# ZONE 3: INTERFACE
# ==========================================

def format_top(title: str, counts: list[tuple[str, int]]) -> str:
    if not counts:
        return f"{title}: sem dados ainda."
    lines = [title + ":"]
    width = max(len(name) for name, _ in counts)
    for name, count in counts:
        lines.append(f"  {name.ljust(width)}  {count}")
    return "\n".join(lines)

def format_stale(title: str, stale: list[tuple[str, int]], now: int) -> str:
    if not stale:
        return f"{title}: nada parado."
    lines = [title + ":"]
    for name, ts in stale:
        days = (now - ts) // 86400
        lines.append(f"  {name}  (há {days}d, último uso {datetime.fromtimestamp(ts):%d/%m/%Y})")
    return "\n".join(lines)

def print_report(configs: dict) -> None:
    log_dir = os.path.expanduser(configs['log_dir'])
    top_n = configs['top_n']
    stale_days = configs['stale_days']
    now = int(datetime.now().timestamp())

    cmd_rows = read_tsv(os.path.join(log_dir, 'cmd_log.tsv'))
    bind_rows = read_tsv(os.path.join(log_dir, 'bind_log.tsv'))
    tracking_started = read_tracking_started(os.path.join(log_dir, 'tracking_started'))

    print(f"📊 usage-report — {days_tracked(tracking_started, now)} dias rastreados")
    print()
    print(format_top(f"Top {top_n} comandos", top_counts(cmd_rows, top_n)))
    print()
    print(format_top(f"Top {top_n} binds", top_counts(bind_rows, top_n)))
    print()
    print(format_stale(f"Binds parados (>{stale_days}d sem uso)", stale_entries(bind_rows, stale_days, now), now))


def main() -> None:
    configs = load_configs()
    print_report(configs)


if __name__ == '__main__':
    sys.exit(main())
