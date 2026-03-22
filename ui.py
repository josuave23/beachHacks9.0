import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        self.tasks = []
        self.timeline = []
        self.unscheduled = []

        self.title("Timestop")
        self.geometry("1360x768") #WINDOW SIZE (1360x768)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(1, weight=1)

        #sidebar shortcuts--------------------------------------
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="red")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        #main area in application-----------------------------
        self.mainArea = ctk.CTkFrame(self, width=200)
        self.mainArea.grid(row=0, column=1, sticky="nsew")
        self.mainArea.grid_rowconfigure(0, weight=0)  # topbar — fixed height
        self.mainArea.grid_rowconfigure(1, weight=1)  # content — stretches
        self.mainArea.grid_columnconfigure(0, weight=1)
        
        #topbar with labels (inside mainArea)-----------------------
        self.topbar = ctk.CTkFrame(self.mainArea, height=60, fg_color="green")
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)

        #scrolling area inside mainArea to hold list of tasks)-------------
        self.contentFrame = ctk.CTkScrollableFrame(self.mainArea)
        self.contentFrame.grid(row=1, column=0, sticky="nsew")

        #labels and buttons
        self.titleLabel = ctk.CTkLabel(self.topbar, text="Today's Schedule", font=("Arial", 16))
        self.titleLabel.pack(side="left", padx=16)

        self.addTaskBtn = ctk.CTkButton(self.topbar, text="+ Add Task", command=self.openAddTask)
        self.addTaskBtn.pack(side="right", padx=16)
        
        self.appName = ctk.CTkLabel(self.sidebar, text="Timestop").grid(row=0, column=0, padx=10, pady=10)

        self.genButton = ctk.CTkButton(self.topbar, text="Generate Schedule", command=self.generateSchedule)
        self.genButton.pack(side="right", padx=8)

    def addTaskCard(self, name, duration, importance, deadType, deadline):
        card = ctk.CTkFrame(self.contentFrame)
        card.pack(fill="x", padx=10, pady=5)

        nameLabel = ctk.CTkLabel(card, text=name, font=("Arial", 13))
        nameLabel.pack(side="left", padx=12, pady=10)

        badgeColor = "#FCEBEB" if deadType == "hard" else "#EEEDFE"
        badgeText  = "#A32D2D" if deadType == "hard" else "#3C3489"
        badge = ctk.CTkLabel(card, text=deadType, fg_color=badgeColor,
                            text_color=badgeText, corner_radius=8,
                            font=("Arial", 11))
        badge.pack(side="right", padx=12)

        metaLabel = ctk.CTkLabel(card, text=f"{duration} min · importance {importance}",
                                font=("Arial", 11), text_color="gray")
        metaLabel.pack(side="right", padx=8)

    def openAddTask(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Task")
        popup.geometry("400x500")
        popup.after(100, popup.lift)

        # name
        ctk.CTkLabel(popup, text="Task name").pack(pady=(16, 0))
        nameEntry = ctk.CTkEntry(popup, placeholder_text="e.g. Finish assignment")
        nameEntry.pack(pady=(4, 0), padx=20, fill="x")

        # duration
        ctk.CTkLabel(popup, text="Duration (minutes)").pack(pady=(12, 0))
        durationEntry = ctk.CTkEntry(popup, placeholder_text="e.g. 60")
        durationEntry.pack(pady=(4, 0), padx=20, fill="x")

        # importance
        ctk.CTkLabel(popup, text="Importance (1-10)").pack(pady=(12, 0))
        importanceEntry = ctk.CTkEntry(popup, placeholder_text="e.g. 5")
        importanceEntry.pack(pady=(4, 0), padx=20, fill="x")

        # deadline type
        ctk.CTkLabel(popup, text="Deadline type").pack(pady=(12, 0))
        deadTypeMenu = ctk.CTkOptionMenu(popup, values=["soft", "hard", "none"])
        deadTypeMenu.pack(pady=(4, 0), padx=20, fill="x")

        # deadline
        ctk.CTkLabel(popup, text="Deadline (days from now)").pack(pady=(12, 0))
        deadlineEntry = ctk.CTkEntry(popup, placeholder_text="e.g. 3")
        deadlineEntry.pack(pady=(4, 0), padx=20, fill="x")

        # confirm button
        def confirm():
            from datetime import datetime, timedelta
            name       = nameEntry.get()
            duration   = int(durationEntry.get())
            importance = int(importanceEntry.get())
            deadType   = deadTypeMenu.get()
            daysAway   = deadlineEntry.get()
            deadline   = datetime.now() + timedelta(days=int(daysAway)) if daysAway else None

            from task import Task
            newTask = Task(name, duration, importance, deadType, deadline=deadline)
            self.tasks.append(newTask)
            self.addTaskCard(name, duration, importance, deadType, deadline)
            popup.destroy()

        ctk.CTkButton(popup, text="Add Task", command=confirm).pack(pady=16)
    
    def generateSchedule(self):
        from schedule import Schedule
        from datetime import time

        if not self.tasks:
            return  # do nothing if no tasks added yet

        s = Schedule(
            tasks=self.tasks,
            dayStart=time(8, 0),
            dayEnd=time(22, 0),
            slotSize=30
        )

        self.timeline, self.unscheduled = s.genSchedule([])
        self.displaySchedule()
    
    def isFirstSlot(self, slot):
        idx = self.timeline.index(slot)
        if idx == 0:
            return True
        return self.timeline[idx - 1][2] != slot[2]

    def displaySchedule(self):
        # clear existing content first
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        # section label
        ctk.CTkLabel(self.contentFrame, text="GENERATED SCHEDULE", 
                    font=("Arial", 11), text_color="gray").pack(anchor="w", padx=12, pady=(10, 4))

        # render each occupied slot
        for slot in self.timeline:
            if slot[2] is not None and self.isFirstSlot(slot):
                timeStr = slot[0].strftime("%I:%M %p")
                row = ctk.CTkFrame(self.contentFrame)
                row.pack(fill="x", padx=10, pady=2)

                ctk.CTkLabel(row, text=timeStr, width=80, 
                            font=("Arial", 11), text_color="gray").pack(side="left", padx=8)
                ctk.CTkLabel(row, text=slot[2].n, 
                            font=("Arial", 13)).pack(side="left", padx=4)

        # unscheduled warning
        if self.unscheduled:
            names = ", ".join([t.n for t in self.unscheduled])
            ctk.CTkLabel(self.contentFrame, 
                        text=f"Could not schedule: {names}",
                        text_color="#A32D2D").pack(anchor="w", padx=12, pady=8)

app = App()
app.mainloop()