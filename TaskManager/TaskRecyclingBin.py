from __future__ import print_function
from ProgramHandler import *
from TaskLibraryIO import *
from TaskLibrary import *
from Task import *
import sys

# TaskRecyclingBin is a property of the TaskLibrary class. 
# All tasks inside the TaskRecyclingBin SHOULD NOT be found in 
# the TaskLibrary.
class TaskRecyclingBin:
	def __init__(self):
		self.dict = {}
		
	# Resets Recycling Bin	
	def DumpRecyclingBin(self):
		self.dict = {}
		
	# Retrieves list of all Tasks in TaskRecyclingBin
	# returns: List<Task>
	def GetRecycledTasks(self):
		listOfRecycledTasks = []
		for key in self.dict:
			listOfRecycledTasks.append(self.dict[key])
		return listOfRecycledTasks
		
	# Retrieves list of all Tasks in TaskRecyclingBin,
	# Wipes TaskRecyclingBin
	# returns: List<Task>
	def ReturnAllRecycledTasks(self):
		listOfRestorableTasks = []
		for key in self.dict:
			listOfRestorableTasks.append(self.dict[key])
		self.dict = {}
		return listOfRestorableTasks
		
	# Retrieves Tasks specified by taskIds, from TaskRecyclingBin
	# Wipes Tasks specified by taskIds, from TaskRecyclingBin
	# args: taskids - List<uuid>
	# returns: List<Tasks>
	def ReturnRecycledTasks(self, taskIds):
		listOfRestorableTasks = []
		for key in self.dict:
			for taskId in taskIds:
				if self.dict[key].TaskId == taskId:
					listOfRestorableTasks.append(self.dict[key])
		
		for key in self.dict.keys():
			for task in listOfRestorableTasks:
				if task.TaskId == key:
					del self.dict[key]
					
		return listOfRestorableTasks