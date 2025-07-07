# Task Tracker CLI（任务跟踪器命令行工具）

Task Tracker 是一个基于命令行的待办事项管理工具，支持任务的添加、修改、删除、状态更新、搜索、导出等功能。所有任务数据保存在本地 JSON 文件中，轻量快速，便于扩展。

---

##  功能概览

- 添加、更新、删除任务
- 标记任务为 `todo`、`in-progress`、`done`
- 列出全部任务或按状态过滤
- 搜索关键词
- 导出任务为 CSV 文件（兼容 Excel）
- 任务重新排序（按状态 + 时间）
- 帮助命令查看使用方法

---

## 使用方法

###  安装环境

需安装 Python 3.x，无需额外依赖。

```bash
python --version
```

### 运行方式

在命令行中使用：

```bash
python task_cli.py <命令> [参数]
```

首次运行会自动创建 `tasks.json` 文件保存任务数据。

------

## 命令说明

| 功能               | 命令示例                                                     |
| ------------------ | ------------------------------------------------------------ |
| 添加任务           | `python task_cli.py add "Buy groceries"`                     |
| 更新任务描述       | `python task_cli.py update 1 "Buy groceries and cook dinner"` |
| 删除任务           | `python task_cli.py delete 1`                                |
| 标记为 in-progress | `python task_cli.py mark-in-progress 2`                      |
| 标记为 done        | `python task_cli.py mark-done 2`                             |
| 列出所有任务       | `python task_cli.py list`                                    |
| 按状态列出         | `python task_cli.py list done` `python task_cli.py list todo` `python task_cli.py list in-progress` |
| 搜索关键词         | `python task_cli.py search groceries`                        |
| 导出为 CSV         | `python task_cli.py export`（导出为 `tasks_export.csv`）     |
| 重新排序任务       | `python task_cli.py reorder`                                 |
| 查看帮助           | `python task_cli.py help`                                    |



------

## 文件说明

| 文件               | 说明                                     |
| ------------------ | ---------------------------------------- |
| `task_cli.py`      | 主程序文件                               |
| `tasks.json`       | 任务数据存储文件（自动生成）             |
| `tasks_export.csv` | 导出的任务 CSV 文件（可打开 Excel 查看） |



------

## 注意事项

- 时间格式为 `YYYY-MM-DD HH:MM:SS`，可在 `now()` 函数中修改。
- 如果在 Excel 中打开 CSV 时日期显示为 `########`，请调整列宽。
- 所有数据本地保存，无需联网。

------

## 示例演示

```bash
$ python task_cli.py add "wash dishes"
添加任务成功

$ python task_cli.py add "clean the house"
添加任务成功

$ python task_cli.py add "do homeword"
添加任务成功

D$ python task_cli.py list
[1] wash dishes - todo (Updated: 2025-07-07 21:55:32)
[2] clean the house - todo (Updated: 2025-07-07 21:55:42)
[3] do homeword - todo (Updated: 2025-07-07 21:55:53)

$ python task_cli.py search do
[3] do homeword - todo (Updated: 2025-07-07 21:55:53)

$ python task_cli.py update 3 "do homework"
更新任务成功

$ python task_cli.py list
[1] wash dishes - todo (Updated: 2025-07-07 21:55:32)
[2] clean the house - todo (Updated: 2025-07-07 21:55:42)
[3] do homework - todo (Updated: 2025-07-07 21:57:34)

$ python task_cli.py mark-done 1
任务 1 状态已更新为 done

$ python task_cli.py mark-in-progress 2
任务 2 状态已更新为 in-progress

$ python task_cli.py lsit
无效的命令，可以help查看帮助

$ python task_cli.py list
[1] wash dishes - done (Updated: 2025-07-07 21:58:55)
[2] clean the house - in-progress (Updated: 2025-07-07 21:59:05)
[3] do homework - todo (Updated: 2025-07-07 21:57:34)

$ python task_cli.py reorder
Tasks reordered successfully!

$ python task_cli.py list
[0] do homework - todo (Updated: 2025-07-07 21:57:34)
[1] clean the house - in-progress (Updated: 2025-07-07 21:59:05)
[2] wash dishes - done (Updated: 2025-07-07 21:58:55)

$ python task_cli.py export_csv
任务已导出到 tasks.csv
```

------

## License

MIT License - 自由使用、修改和分发。
