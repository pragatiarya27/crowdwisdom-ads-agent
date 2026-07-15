from hermes.task import Task

class KanbanBoard:
    def __init__(self):
        self.todo = []
        self.in_progress = []
        self.done = []
        self.failed = []

    def add_task(self, task: Task):
        self.todo.append(task)
        print(f"📋 [KANBAN] Task added → {task}")

    def start_task(self, task: Task):
        self.todo.remove(task)
        task.status = "in_progress"
        self.in_progress.append(task)
        print(f"⚙️  [KANBAN] Task started → {task}")

    def complete_task(self, task: Task, result: dict):
        self.in_progress.remove(task)
        task.status = "done"
        task.result = result
        self.done.append(task)
        print(f"✅ [KANBAN] Task done → {task}")

    def fail_task(self, task: Task, error: str):
        if task in self.in_progress:
            self.in_progress.remove(task)
        task.status = "failed"
        task.result = {"error": error}
        self.failed.append(task)
        print(f"❌ [KANBAN] Task failed → {task} | Error: {error}")

    def get_next_task(self, task_type: str = None):
        # picks next todo task, optionally filtered by type
        for task in self.todo:
            if task_type is None or task.type == task_type:
                return task
        return None

    def summary(self):
        return (f"\n📊 KANBAN BOARD\n"
                f"  TODO       : {len(self.todo)}\n"
                f"  IN PROGRESS: {len(self.in_progress)}\n"
                f"  DONE       : {len(self.done)}\n"
                f"  FAILED     : {len(self.failed)}\n")

    def all_done(self):
        return len(self.todo) == 0 and len(self.in_progress) == 0