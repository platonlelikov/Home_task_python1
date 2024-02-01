import dataclasses
from dataclasses import dataclass
import enum
import json
import os.path as osp
from datetime import datetime


@dataclass
class Status(int, enum.Enum):
    new = 1
    solving = 2
    review = 3
    solved = 4
    declined = 5


@dataclass
class Task:
    name: str
    create_date: str
    change_date: str
    status: Status = 1


@dataclass
class Task_manager:
    tasks: list
    history: dict

    def add_task(self, task_to_list):
        self.tasks.append(task_to_list)

    def add_action(self, history_time, history_action):
        self.history[history_time] = history_action

    def load_from_file(self, file_name):
        if osp.exists("./" + file_name):
            with open(file_name) as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data["tasks"]]
                self.history = data["history"]
        else:
            print("File doesn't exist")


task_manager = Task_manager([], {})


def unpack():
    with open("file.json", "r+") as json_file_r:
        json.load(json_file_r)
        task_manager.load_from_file("file.json")


def pack(dump):
    with open("file.json", "w+") as json_file_w:
        json.dump(dump, json_file_w, indent=4)


i = 1
while i == 1:
    button = input("Enter the number you need \n 1 - Create the task \n 2 - Change the status of task \n 3 - View the list of tasks \n 4 - Show the history \n 5 - Close the program \n")
    if button == "1":
        unpack()
        name_cycle = input("Enter the task's name: ")
        task = Task(name_cycle, str(datetime.now()), str(datetime.now()))
        task_manager.add_task(task)
        task_manager.add_action(str(datetime.now()), "New task was created: " + task.name)
        dump = {"tasks": [dataclasses.asdict(task) for task in task_manager.tasks], "history": task_manager.history}
        pack(dump)
    if button == "2":
        unpack()
        choose_task = input("Enter the tasks's name\n")
        task_name = [(idx,i) for idx,i in enumerate(task_manager.tasks) if i.name == choose_task]
        if not task_name:
            print("Wrong task name, try again, I'm sure you can")
            continue
        change_status = int(input("""If you want to: 
         Move to the next status - enter 1 
         Move to the previous status - enter 2
         Decline - enter 3\n"""))
        if change_status == 1:
            old_status_value = task_name[0][1].status
            task_name[0][1].status += 1
            task_manager.tasks[task_name[0][0]] = task_name[0][1]
            task_manager.add_action(str(datetime.now()),
                                    "Task " + choose_task + ": status was changed from " + str(Status(task_name[0][1].status - 1).name) + " to " +
                                    str(Status(task_name[0][1].status).name))
        if change_status == 2:
            if task_name[0][1].status == 1:
                print("You can't move this status, because this is a new task")
                continue
            old_status_value = task_name[0][1].status
            task_name[0][1].status -= 1
            task_manager.add_action(str(datetime.now()),
                                    "Task " + choose_task + ": status was changed from " + str(Status(task_name[0][1].status + 1).name) + " to " +
                                    str(Status(task_name[0][1].status).name))
        if change_status == 3:
            old_status_value = task_name[0][1].status
            task_name[0][1].status = 5
            task_manager.add_action(str(datetime.now()),
                                    "Task " + choose_task + ": status was changed from " + str(Status(task_name[0][1].status - 4).name) + " to declined")

    dump = {"tasks": [dataclasses.asdict(task) for task in task_manager.tasks], "history": task_manager.history}
    pack(dump)

    if button == "3":
        unpack()
        print(task_manager.tasks)
        dump = {"tasks": [dataclasses.asdict(task) for task in task_manager.tasks], "history": task_manager.history}
        pack(dump)

    if button == "4":
        unpack()
        print(task_manager.history)
        dump = {"tasks": [dataclasses.asdict(task) for task in task_manager.tasks], "history": task_manager.history}
        pack(dump)

    if button == "5":
        break




