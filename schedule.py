from datetime import datetime, time, date, timedelta
import math

class Schedule():
    def __init__(self, tasks, dayStart, dayEnd, slotSize, urgencyWeight=0.5, impWeight=0.5): #weight values need to be variable in the end
        self.tasks = tasks #list; list of all tasks in this schedule
        self.start = dayStart #time; time that each day will start
        self.end = dayEnd #time; time that each day ends
        self.slotSize = slotSize #int; the size of each time "block" (in this case likely 5 minutes)
        self.timeline = [] #list; each entry is a timeslot (basically this is the full schedule)
        self.urgencyWeight = urgencyWeight #float; user preference
        self.impWeight = impWeight #float; user preference
        self.unscheduled = []

    def buildTimeline(self):
        current = self.start
        while current < self.end:
            self.timeline.append((current, True, None)) #contains the time that each slot is associated with and the task that will be scheduled for this slot
            dt = datetime.combine(date.today(), current)
            dtUpdated = dt + timedelta(minutes=self.slotSize)
            current = dtUpdated.time()
    
    def blockEvents(self, events):
        for event in events:
            for slot in self.timeline:
                if slot[0] >= event.start and slot[0] < event.end:
                    slot[1] = False

    def scoreTasks(self):
        h = []
        nh = []
        for task in self.tasks:
            task.score = task.findScore(self.urgencyWeight, self.impWeight)
            if task.type == "hard":
                h.append(task)
            elif task.type == "soft":
                nh.append(task)
        return h+nh
    
    def findEarliestSlot(self, slotsNeeded):
        for i in range(len(self.timeline)):
            if i+slotsNeeded >= len(self.timeline):
                break
            for j in range(len(self.timeline[i:i+slotsNeeded])):
                if self.timeline[j][1] == False:
                    i = j + 1
                    break
                if j == i + slotsNeeded and self.timeline[j][1] == True:
                    return i
        return None #Return not enough slots available

    def findLatestSlot(self, slotsNeeded, deadline):
        deadlineIdx = len(self.timeline)/2
        while self.timeline[deadlineIdx][0] != deadline:
            if self.timeline[deadlineIdx][0] > deadline:
                deadlineIdx = deadlineIdx/2
            elif self.timeline[deadlineIdx][0] < deadline:
                toAdd = len(self.timeline[deadlineIdx:])/2
                deadlineIdx += toAdd
        for i in range(deadlineIdx - slotsNeeded, 0, -1):
            if j-slotsNeeded < 0:
                break
            for j in range(slotsNeeded, j-slotsNeeded):
                if self.timeline[j][1] == False:
                    i = j - 1
                    break
                if j == i - slotsNeeded and self.timeline[j][1] == True:
                    return i - slotsNeeded
        return None
    
    def assignSlot(self, task, startIdx, slotsNeeded):
        for i in range(startIdx, startIdx + slotsNeeded):
            self.timeline[i][1] = False
            self.timeline[i][2] = task

    def genSchedule(self, calendarEvents):
        self.buildTimeline()
        self.blockEvents(calendarEvents)
        scored = self.scoreTasks()

        for task in scored:
            slotsNeeded = math.ceil(task.duration / self.slotSize)
            if task.deadType == "hard":
                idx = self.findLatestSlot(slotsNeeded, task.deadline)
            else:
                idk = self.findEarliestSlot(slotsNeeded)
            
            if idx is not None:
                self.assignSlot(task, idx, slotsNeeded)
            else:
                self.unscheduled.append(task)

        return self.timeline, self.unscheduled
