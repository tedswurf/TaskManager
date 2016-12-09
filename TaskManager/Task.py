from __future__ import print_function
from ProgramHandler import *
import sys
import uuid
import time

class Task:

	def __init__(self, taskDate = None, taskPriority = None, taskTitle = None,
			taskBody = None, task = None, emptyTask = False):
		if(emptyTask):
			self.TaskId = uuid.uuid1()
			self.TaskPriority = TaskPriority.NoPriority
			self.TaskDate = ""
			self.TaskTitle = ""
			self.TaskBody = ""
			self.TaskCreated = time.strftime("%d/%m/%Y-%H:%M:%S")
			self.TaskLastUpdated = time.strftime("%d/%m/%Y-%H:%M:%S")
			self.TaskDirty = False
		else:
			if(taskDate is None and taskTitle is None and taskBody is None
				and task is None):
				ProgramHandler().eprint(ErrorTypes.ArgumentNullError,"Task","init", sep=":")
				exit
			
			if(task is not None):
				self.TaskId = task.TaskId
				self.TaskPriority = task.TaskPriority
				self.TaskDate = task.TaskDate
				self.TaskTitle = task.TaskTitle
				self.TaskBody = task.TaskBody
			else:
				self.TaskId = uuid.uuid1()
				self.TaskPriority = taskPriority
				self.TaskDate = taskDate
				self.TaskTitle = taskTitle
				self.TaskBody = taskBody		
			self.TaskCreated = time.strftime("%d/%m/%Y-%H:%M:%S")
			self.TaskLastUpdated = time.strftime("%d/%m/%Y-%H:%M:%S")
			self.TaskDirty = True
		
	def UpdateTask(taskId, task):
		ProgramHandler().eprint(ErrorTypes.ArgumentNullError,"Task","ModifyTask", sep=":")
		# Check in Task Library if task with TaskId	exists
		# update new task, update TaskLastUpdated
		# turn TaskDirty True
		
	@staticmethod
	def PrintTask(self):
		print("TaskID:{}".format(self.TaskId))
		print("Priority:{}".format(self.TaskPriority))
		print("Title:{}".format(self.TaskTitle))
		print("Date:{}".format(self.TaskDate))
		print("Body:{}".format(self.TaskBody))
		print("DateCreated:{}".format(self.TaskCreated))
		print("LastUpdated:{}".format(self.TaskLastUpdated))
		
class TaskPriority:
	HighPriority = "HighPriority"
	MediumPriority = "MediumPriority"
	LowPriority = "LowPriority"
	NoPriority = "NoPriority"