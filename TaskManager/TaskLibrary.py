from __future__ import print_function
from ProgramHandler import *
from TaskLibraryIO import *
from TaskRecyclingBin import *
from Task import *
import sys

# Defines the hashtable of tasks
class TaskLibrary:

	# Defines Empty TaskLibrary
	# arg: dictionary - Python dictionary
	def __init__(self, dictionary = None):
		if(dictionary == None):
			self.dict = {}
		else:
			self.dict = dictionary
		self.TaskRecyclingBin = TaskRecyclingBin()
	
	# Pass in filter of dictionary<taskProperty, taskValue>
	# Return list of tasks where, for all tasks with property taskProperties,
	# task.taskProperty = taskValue
	# arg: argDict - Python dictionary<string, string>; a filter
	# returns: List<Task>
	def GetBulkTasks(self, argDict):
		if argDict == None:
			return None
		listOfTasks = []
		numberOfExpectedValuesMatched = len(argDict)
		for task in self.dict:
			numberOfMatchedValues = 0
			for key,value in argDict.iteritems():
				#print(getattr(task,key),value)
				if str(getattr(task, key)) == str(value):
					numberOfMatchedValues += 1
			#print(numberOfExpectedValuesMatched,numberOfMatchedValues)
			if numberOfExpectedValuesMatched == numberOfMatchedValues:
				listOfTasks.append(task)
		return listOfTasks
		
	# Retrieves all ids of all tasks in task library
	# returns: List<uuids>
	def GetAllTaskIds(self):
		listOfTaskIds = []
		for key in self.dict:
			listOfTaskIds.append(self.dict[key].TaskId)
		return listOfTaskIds
	
	# Retrieves list of all dirty tasks 
	# returns: List<Task>
	def GetDirtyTasks(self):
		dirtyTasks = []
		for key in self.dict:
			if self.dict[key].TaskDirty:
				#print("found dirty task")
				dirtyTasks.append(self.dict[key])
		return dirtyTasks
	
	# Sets all Task.TaskDirty fields False in TaskLibrary
	def MarkAllTasksClean(self):
		for key in self.dict:
			self.dict[key].TaskDirty = False
		
	# Returns a Task from the TaskLibrary
	# returns: <Task>
	def GetTask(self,taskId):
		return self.dict[taskId]
	
	# Creates a new Task and adds it to the TaskLibrary
	# arg: task - <Task>
	# returns: Task.TaskId <string>
	def AddTask(self,task):
		print("Adding Task")
		newTaskID = Task(task = task)
		self.dict[newTaskID.TaskId] = task
		return newTaskID
		
	# Removes the task with the TaskId passed
	# args: taskIds - <uuid>
	def RemoveTask(self,taskId):
		if self.dict[taskId] == None:
			return False
		self.TaskRecyclingBin.dict[taskId] = self.dict[taskId]
		del self.dict[taskId]
		print("Task with TaskId:", taskId, "deleted")
		return True
	
	# Looks for the task in the TaskLibrary, overwrites the task
	# and sets the TaskDirty flag to True prior to.
	# args: taskId - <uuid> 
	# args: task - <Task>
	def ModifyTask(self, taskId, task):
		if task == None or taskId == None:
			ProgramHandler().eprint(ErrorTypes.ArgumentNullError,"TaskLibrary","ModifyTask", sep=":")
			return False
		if self.dict[taskId] == None:
			ProgramHandler().eprint(ErrorTypes.DictionaryIndexDoesNotExistError,"TaskLibrary","ModifyTask", sep=":")
			return False
		
		try:
			task.TaskDirty = True
			self.dict[taskId] = task
			
		except:
			ProgramHandler().eprint(ErrorTypes.DictionaryCollisionError,"TaskLibrary","ModifyTask", sep=":")
			return False
			
		return True
		
	# Overwrites all Tasks in targetXmlFileName with Tasks in TaskLibrary
	# Sets all TaskDirty flags to False.
	# Wipes out TaskRecyclingBin
	# args: targetXmlFileName - <string>
	def SyncTaskLibrary(self, targetXmlFileName):
		print("Syncing Task Library")
		TaskLibraryIO.SyncTaskLibrary(self, targetXmlFileName)
		
	# Prints the Entire Task Library
	def PrintTaskLibrary(self):
		print("\nPrinting Task Library\n")
		for key in self.dict:
			task = self.dict[key]
			Task.PrintTask(task)
			print()
		print()
		
	# Takes all Tasks in TaskRecyclingBin and re-adds them to 
	# TaskLibrary.
	# Wipes TaskRecyclingBin
	# args: taskIds - List<uuid>
	def RestoreRecyclingBin(self, taskIds = None):
		print("\nRestoring Task Recycling Bin to Task Library\n")
		if taskIds != None:
			listOfRestorableTasks = self.TaskRecyclingBin.ReturnRecycledTasks(taskIds)
		else:
			listOfRestorableTasks = self.TaskRecyclingBin.ReturnAllRecycledTasks()
		listOfRestoredTasks = []
		listOfRestoredTasksFailed = []
		if len(listOfRestorableTasks) == 0:
			print("No Tasks in Task Recycling Bin\n")
			return
		
		for restorableTask in listOfRestorableTasks:
			if self.dict.get(restorableTask.TaskId) == None:
				self.dict[restorableTask.TaskId] = restorableTask
				listOfRestoredTasks.append(self.dict[restorableTask.TaskId])
			else:
				listOfRestoredTasksFailed.append(restorableTask)
				ProgramHandler().eprint(ErrorTypes.DictionaryCollisionError,"TaskLibrary","RestoreRecyclingBin", sep=":")
				print("Failed to add task with TaskId:", restorableTask.TaskId)
		
		if len(listOfRestoredTasks) == len(listOfRestorableTasks):
			print("Fully restored Task Library - number of Tasks restored:", len(listOfRestoredTasks))
		else:
			print("Partially restored Task Library\n")
			for restoredTaskFailed in listOfRestoredTasksFailed:
				Task.PrintTask(restoredTaskFailed)
		print("Tasks Successfully Restored:\n")
		for restoredTask in listOfRestoredTasks:
			Task.PrintTask(restoredTask)
			print()
			
	# Print All Tasks in Task Library
	def PrintTaskRecyclingBin(self):
		print("\nPrinting Task Recycling Bin\n")
		if self.TaskRecyclingBin == None:
			print("TaskRecyclingBin does not exist for this Library\n")
			return
		if len(self.TaskRecyclingBin.dict) == 0:
			print("Empty Recycling Bin\n")
			return
		for key in self.TaskRecyclingBin.dict:
			Task.PrintTask(self.TaskRecyclingBin.dict[key])
		print()
	
	# Wipes out all Tasks in TaskLibrary
	# args: confirm - <bool>
	# returns: True - <bool>; if wipe confirmed
	# returns: False - <bool>; if wipe disallowed
	def WipeTaskLibrary(confirm):
		if confirm:
			self.dict = {}
		else:
			return