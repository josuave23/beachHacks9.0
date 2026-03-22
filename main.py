"""
Concept: Program that will give you a schedule of everything you need to do (i.e. chores, work, assignments, study, ect)

Features:
- Priorizing more important tasks in a way set by the user
- Sending notifications to the user via phone/other preferred method
- API's with canvas and google calendar

Hopefully: Implement basic UI

"""
from datetime import datetime, timedelta, time
from schedule import Schedule
from task import Task

task1 = Task("test1", 120, 3, "soft", "do 2 loads of laundry", datetime.now() + timedelta(days=3))
task2 = Task("test2", 180, 10, "hard", "do 2 loads of laundry", datetime.now() + timedelta(days=2))
task3 = Task("test3", 320, 7, "soft", "do 2 loads of laundry", datetime.now() + timedelta(days=3))
tasks = [task1, task2, task3]

newSchedule = Schedule(tasks, time(8, 0), time(22, 0), 5)
events = []
newSchedule.genSchedule(events)
