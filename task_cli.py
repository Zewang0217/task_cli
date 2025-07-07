import sys
import os
import json
from datetime import datetime
import csv

TASK_FILE = 'tasks.json'

# 初始化 JSON 文件
def init_storage():
  if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, "w") as f:
      json.dump([], f)
      print("初始化完成")

# 清空
def clean_all_tasks():
  save_tasks([])
  print("清空完成")

# 保存任务列表
def save_tasks(tasks):
  with open(TASK_FILE, "w") as f:
    json.dump(tasks, f, indent=4)

# 加载任务列表
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# 获取当前时间
def now():
  return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 添加任务
def add_task(description):
  tasks = load_tasks()
  new_id = max([task["id"] for task in tasks], default=0) + 1
  task = {
    "id" : new_id,
    "description" : description,
    "status" : "todo",
    "createAt" : now(),
    "updateAt" : now()
  }
  tasks.append(task)
  save_tasks(tasks)
  print("添加任务成功")

# 更改
def update_task(id, new_description):
  tasks = load_tasks()
  found = False
  for task in tasks:
    if task["id"] == id:
      task["description"] = new_description
      task["updateAt"] = now()
      found = True
      break
  if found:
    save_tasks(tasks)
    print("更新任务成功")
  else:
    print("未找到该任务")

# 删除
def delete_task(id):
  tasks = load_tasks()
  found = False
  for task in tasks:
    if task["id"] == id:
      tasks.remove(task)
      found = True
      break
  if found:
    save_tasks(tasks)
    print("删除任务成功")
  else:
    print("未找到该任务")
  """ 或
  tasks == load_tasks()
  new_tasks = [task for task in tasks
  if task["id"] != id]
  if len(tasks) == len(new_tasks):
    save_tasks(new_tasks)
    print("删除任务成功")
  else:
    print("未找到该任务")
  """

# 状态管理
def mark_status(id, status):
  tasks = load_tasks()
  found = False
  for task in tasks:
    if task["id"] == id:
      task["status"] = status
      task["updateAt"] = now()
      found = True
      break
  if found:
    save_tasks(tasks)
    print(f"任务 {id} 状态已更新为 {status}")
  else:
    print("未找到该任务")

# 查看某条任务
def view_task(id):
  tasks = load_tasks()
  found = False
  for task in tasks:
    if task["id"] == id:
      print(
        f"[{task['id']}] {task['description']} - {task['status']} (Updated: {task['updatedAt']})")
      found = True
      break

# 列出全部任务/按状态列出
def list_tasks(filter_status=None):
  tasks = load_tasks()
  filtered = tasks if not filter_status else [t for t in tasks if t["status"] == filter_status]
  if not filtered:
    print("没有任务")
  else:
    for task in filtered:
      print(
        f"[{task['id']}] {task['description']} - {task['status']} (Updated: {task['updateAt']})")

# 导出为 CSV 文件
def export_csv(filename="tasks.csv"):
  tasks = load_tasks()
  if not tasks:
    print("没有任务可导出")
    return
  with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["id",
    "description", "status", "createAt", "updateAt"])
    writer.writeheader()
    for task in tasks:
      writer.writerow(task)
  print(f"任务已导出到 {filename}")

# 关键词搜索
def search_tasks(keyword):
  tasks = load_tasks()
  result = [task for task in tasks if keyword.lower() in task["description"].lower()]
  if not result:
    print("没有找到匹配的任务")
  else:
    for task in result:
      print(
        f"[{task['id']}] {task['description']} - {task['status']} (Updated: {task['updateAt']})")

# help
def print_help():
    print("""
Task Tracker CLI - Usage Guide

Commands:
  add "description"               Add a new task
  update <id> "description"       Update task description
  delete <id>                     Delete a task by ID
  mark-in-progress <id>           Mark a task as in progress
  mark-done <id>                  Mark a task as done
  list                            List all tasks
  list done|todo|in-progress      List tasks by status
  search <keyword>                Search tasks by description keyword
  export_csv                      Export all tasks to tasks_export.csv
  reorder                         Reorder tasks: todo -> in-progress -> done
  help                            Show this help message
  clean                           Clean up completed tasks
  clean_all                       Clean up all tasks
""")

# 重排序
def reorder_tasks():
  tasks = load_tasks()
  status_order = {
        "todo": 0,
        "in-progress": 1,
        "done": 2
    }

  tasks.sort(key=lambda task: (
    status_order.get(task['status'], 3), 
    task["createAt"]
  ))

  for idx, task in enumerate(tasks):
    task["id"] = idx
  
  save_tasks(tasks)
  print("Tasks reordered successfully!")

# clean tasks
def clean_tasks():
    tasks = load_tasks()

    # 保留未完成的任务
    remaining = [task for task in tasks if task["status"] != "done"]

    # 重新编号 id
    for idx, task in enumerate(remaining, start=1):
        task["id"] = idx

    save_tasks(remaining)
    print(f"Cleaned done tasks. {len(tasks) - len(remaining)} removed, {len(remaining)} remaining.")



def main():
  init_storage()
  if len(sys.argv) < 2:
    print("请输入命令")
    return

  cmd = sys.argv[1]
  args = sys.argv[2:]

  if cmd == "add" and args:
    add_task(" ".join(args))
  elif cmd == "update" and len(args) >= 2:
    update_task(int(args[0]), " ".join(args[1:]))
  elif cmd == "delete" and len(args) == 1:
    delete_task(int(args[0]))
  elif cmd == "mark-in-progress" and len(args) == 1:
    mark_status(int(args[0]), "in-progress")
  elif cmd == "mark-done" and len(args) == 1:
    mark_status(int(args[0]), "done")
  elif cmd == "view_task" and len(args) == 1:
    view_task(int(args[0]))
  elif cmd == "list":
    if len(args) == 0:
      list_tasks()
    elif args[0] in ["todo", "done", "in-progress"]:
      list_tasks(args[0])
    else:
      print("无效的参数")
  elif cmd == "export_csv":
    export_csv()
  elif cmd == "search" and len(args) == 1:
    search_tasks(args[0])
  elif cmd == "help":
    print_help()
  elif cmd == "reorder":
    reorder_tasks()
  elif cmd == "clean":
    clean_tasks()
  elif cmd == "clean_all":
    clean_all_tasks()
  else:
    print("无效的命令，可以help查看帮助")

if __name__ == "__main__":
    main()
