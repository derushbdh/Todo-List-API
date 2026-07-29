import sys
import os
from task_manager import Task, TaskTracker

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data", "tasks.db")

tracker = TaskTracker(FILE_PATH)
args = sys.argv[1:]

if not args:
    print("Usage: python main.py <command> [arguments]")
    sys.exit()
command = args[0]

try:
    if command == "add":
        task = Task(args[1])
        tracker.add(task)
        print(f"Task added successfully (ID: {task.id})")
        
    elif command == "update-description":
        success = tracker.update_description(int(args[1]), args[2])
        if success:
            print("Task updated")
        else:
            print("Task not found!")
    
    elif command == "update-priority":
        success = tracker.update_priority(int(args[1]), args[2])
        if success:
            print("Task updated")
        else:
            print("Task not found!")
            
    elif command == "delete":
        tracker.delete(int(args[1]))
        print("Task deleted")

    elif command == "mark-in-progress":
        success = tracker.set_status(int(args[1]), "in-progress")
        if success:
            print("Task status updated")
        else:
            print("Task not found")

    elif command == "mark-done":
        success = tracker.set_status(args[1], "done")
        if success:
            print("Task status updated")
        else:
            print("Task not found")
        
    elif command == "list":
        status = args[1] if len(args) > 1 else ""
        tasks = tracker.list_tasks(status)
        if not tasks:
            print("No data")
        else:
            for t in tasks:
                updated = t.get("updated", "-")
                print(f"{t['id']} - {t['description']} [{t['status']}] (Created: {t['created']}, Updated: {updated})")
                
    else:
        print(f"Unknown command: {command}")
except RuntimeError as e:
    print(f"Unkown DB error: {e}")