#!/usr/bin/env python3
"""
Todo CLI - 命令行待办事项管理工具

使用方法:
    python todo.py add "买牛奶"   # 添加任务
    python todo.py list           # 列出所有任务
    python todo.py done 1         # 标记第1个任务为完成
    python todo.py delete 1       # 删除第1个任务
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import TypedDict


# 数据文件路径
TODO_DIR = Path.home() / ".todo"
TASKS_FILE = TODO_DIR / "tasks.json"


class Task(TypedDict):
    """任务数据结构"""
    id: int
    title: str
    done: bool
    created_at: str
    done_at: str | None


def ensure_data_dir() -> None:
    """确保数据目录存在。"""
    TODO_DIR.mkdir(parents=True, exist_ok=True)


def load_tasks() -> list[Task]:
    """
    从 JSON 文件加载任务列表。

    Returns:
        任务列表，若文件不存在则返回空列表。
    """
    ensure_data_dir()
    if not TASKS_FILE.exists():
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️  读取任务文件失败: {e}", file=sys.stderr)
        return []


def save_tasks(tasks: list[Task]) -> None:
    """
    将任务列表保存到 JSON 文件。

    Args:
        tasks: 要保存的任务列表。

    Raises:
        IOError: 文件写入失败时抛出。
    """
    ensure_data_dir()
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"❌ 保存任务文件失败: {e}", file=sys.stderr)
        sys.exit(1)


def add_task(title: str) -> None:
    """
    添加一个新任务。

    Args:
        title: 任务标题。
    """
    title = title.strip()
    if not title:
        print("❌ 任务标题不能为空", file=sys.stderr)
        sys.exit(1)

    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    task: Task = {
        "id": new_id,
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat(),
        "done_at": None,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ 已添加任务: {title}")


def list_tasks() -> None:
    """列出所有任务，带序号和完成状态。"""
    tasks = load_tasks()
    if not tasks:
        print("📋 暂无任务")
        return

    print("📋 待办事项列表:")
    for idx, task in enumerate(tasks, start=1):
        status = "x" if task["done"] else " "
        print(f"  {idx}. [{status}] {task['title']}")


def mark_done(index: int) -> None:
    """
    将指定序号的任务标记为完成。

    Args:
        index: 任务序号（从1开始）。
    """
    tasks = load_tasks()
    if not tasks:
        print("📋 暂无任务", file=sys.stderr)
        sys.exit(1)

    if index < 1 or index > len(tasks):
        print(f"❌ 序号 {index} 超出范围（共 {len(tasks)} 个任务）", file=sys.stderr)
        sys.exit(1)

    task = tasks[index - 1]
    if task["done"]:
        print(f"ℹ️  任务 \"{task['title']}\" 已经是完成状态")
        return

    task["done"] = True
    task["done_at"] = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"✅ 已完成任务: {task['title']}")


def delete_task(index: int) -> None:
    """
    删除指定序号的任务。

    Args:
        index: 任务序号（从1开始）。
    """
    tasks = load_tasks()
    if not tasks:
        print("📋 暂无任务", file=sys.stderr)
        sys.exit(1)

    if index < 1 or index > len(tasks):
        print(f"❌ 序号 {index} 超出范围（共 {len(tasks)} 个任务）", file=sys.stderr)
        sys.exit(1)

    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f"🗑️  已删除任务: {removed['title']}")


def build_parser() -> argparse.ArgumentParser:
    """
    构建命令行参数解析器。

    Returns:
        配置好的 ArgumentParser 实例。
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="命令行待办事项管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python todo.py add "买牛奶"    添加新任务
  python todo.py list            列出所有任务
  python todo.py done 1          标记第1个任务为完成
  python todo.py delete 1        删除第1个任务
        """,
    )
    subparsers = parser.add_subparsers(dest="command", metavar="command")
    subparsers.required = True

    # add 子命令
    add_parser = subparsers.add_parser("add", help="添加新任务")
    add_parser.add_argument("title", type=str, help="任务标题")

    # list 子命令
    subparsers.add_parser("list", help="列出所有任务")

    # done 子命令
    done_parser = subparsers.add_parser("done", help="标记任务为完成")
    done_parser.add_argument("index", type=int, help="任务序号（从1开始）")

    # delete 子命令
    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("index", type=int, help="任务序号（从1开始）")

    return parser


def main() -> None:
    """程序入口，解析命令行参数并调用对应功能。"""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.index)
    elif args.command == "delete":
        delete_task(args.index)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
