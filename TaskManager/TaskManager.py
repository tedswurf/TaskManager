# TaskManager.py V1.0 11/26/2016
# TODO: Write Task To file
# TODO: Read Task from file
# TODO: Define Task struct
# TODO: Create Task Orchestration (scheduling)
# TODO: Create Task dict data structure
# TODO: Construct Task Recycling bin
# TODO: Construct Task-XML File parser and constructor
# TODO: Windows 10 OS Async Service Integration
# TODO: Implement Observer Pattern for service end
# TODO: Add Rest Email SMTP notification
# TODO: If necessary, develop multithreading capabilities, and service semaphore
# TODO: Implement scripting front-end via powershell or python
# TODO: Add Web frontend via angular, implement MVC model
# TODO: Add Nano Python Package Deployment

from __future__ import print_function
from Configure import *
from ProgramHandler import *
from TaskLibrary import *
from Task import *
import sys, os

# GLOBAL CONSTANT DECLARATION
global VERSION_NUMBER_DATE
global TM_CONFIGURATION_FILE_NAME

# Global Variable Declaration
global taskLibrary

# GLOBAL VARIABLES INITIALIZATION
VERSION_NUMBER_DATE = "Task Manager V1.0"
TM_CONFIGURATION_FILE_NAME = "TMConfiguration.txt"

class TaskManager:
	@staticmethod
	def PopulateTaskLibrary():
		print("Populating Task Library")
		global taskLibrary
		taskLibrary = TaskLibrary()
		

# MAIN	
def main():
		print(VERSION_NUMBER_DATE)
		configuration = Configure()
		configuration.ReadTMConfiguration(TM_CONFIGURATION_FILE_NAME)
		
		taskManager = TaskManager()
		taskManager.PopulateTaskLibrary()
		
		here = os.path.dirname(os.path.realpath(__file__))
		subdir = "Tasks"
		filename = "TaskTestTarget.Task.xml"
		targetXmlFileName = os.path.join(here, subdir, filename)
		
		#task1 = Task("July", TaskPriority.HighPriority, "Get Job", "Apply Online for more information")
		#newTaskId = taskLibrary.AddTask(task1)
		#print(task1.TaskId, "Added")
		
		#task2 = Task("December", TaskPriority.MediumPriority, "Christmas Carol", "Have a very merry Christmas")
		#newTaskId = taskLibrary.AddTask(task2)
		#print(task2.TaskId, "Added")
		
		# TODO: figure out how to parse <string> to <uuid>
		#task3 = taskLibrary.GetTask(251fc861-b4e1-11e6-ba4f-84bf283094af)
		#taskLibrary.ModifyTask()
		#taskLibrary.RemoveTask(task2.TaskId)
		#taskLibrary.PrintTaskRecyclingBin()
		#taskLibrary.PrintTaskLibrary()		
		#taskLibrary.RestoreRecyclingBin()
		# ALWAYS SYNC LIBRARY AS TASK MANAGER STARTS AND BEFORE IT ENDS
		#taskLibrary.SyncTaskLibrary(targetXmlFileName)
		#taskLibrary.PrintTaskLibrary()
		

if __name__ == "__main__":
	main()