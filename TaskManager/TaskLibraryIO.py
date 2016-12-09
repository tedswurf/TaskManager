from __future__ import print_function
from ProgramHandler import *
from TaskLibrary import *
from Task import *
from xml.etree.ElementTree import Element, SubElement, tostring
import sys, glob, os, os.path
import xml.etree.ElementTree as ET

# TODO: Provide ability to deseralize single target Task.xml files
# * Currently collects all tasks from all Task.xml files and deseralizes them
# * Needs to deseralize target file and serialize back to target file.
# TODO: Needs to provide multi-threading support, Ex. locking
# * Should not be able to access file at the same time
# * Should be able to access multiple, seperate files asynchronously
# Performs all I/O for TaskLibrary.
# Currently provides Serialization/Deseralization of Tasks 
# to and from xml.
class TaskLibraryIO:
	# Matches innerXmlTag with a property of the Task object
	# args: innerXmlTag - <string>
	# returns: <bool>; True if a matching property is found
	# returns: <bool>; False if no matching properties are found
	@staticmethod
	def innerXmlTaskPropertyMatch(innerXmlTag):
		#for all properties of the Task class
		# TODO: see if the following line can be replaced by
		# Task.__dict__
		for property in dir(Task(emptyTask = True)):
			#check if they match innerXmlTag
			if property == innerXmlTag:
				#if match, return True
				return True
		#if we find no match, return False
		return False		

	# TODO: NEED A WAY TO PARSE NON-Primitive and NON-String objects
	# INNERXML STRUCTURES
	# Parses an XML node, "xmlNode", by matching Task properties, and
	# creates a new Task<Task> by settings all attributes
	# args: xmlNode - <xml.treeNode>
	# returns: <Task>
	@staticmethod
	def ParseXmlTask(xmlNode):
		task = Task(emptyTask = True)
		for xmlTag in xmlNode: # innerxml
			if(TaskLibraryIO.innerXmlTaskPropertyMatch(xmlTag.tag)):
				#print("found common attribute", xmlTag.tag)
				try:
					setattr(task, xmlTag.tag, xmlTag.text)
				except:
					ProgramHandler().eprint(ErrorTypes.InvalidAttributeSetterError,"TaskLibraryIO","ParseXmlTask", sep=":")
			else:
				ProgramHandler().eprint(ErrorTypes.InvalidInnerXmlTagError,"TaskLibraryIO","ParseXmlTask", sep=":")
		return task

	# For all files, with extension "*.Task.xml" in "/Tasks/" directory,
	# retrieves dictionary of all Tasks by calling TaskLibrary.ParseXmlTask
	# # returns: Python dict<uuid,Task> {}
	@staticmethod
	def Walk():
		#currently takes all TaskNames
		dictionary = {}
		for dirpath, dirnames, filenames in os.walk("."):
			for filename in [f for f in filenames if f.endswith("Task.xml")]:
				file = os.path.join(dirpath, filename)
				fileObject = open(file, 'r')
				taskObjects = fileObject.readlines()
				tree = ET.parse(file)
				xmlTaskLibrary = tree.getroot()
				for xmlTask in xmlTaskLibrary:
					task = TaskLibraryIO.ParseXmlTask(xmlTask)
					dictionary[task.TaskId] = task
				fileObject.close()
		return dictionary
		
	# populates an xmlNode, "root", with all properties of the 
	# given Task, "task". Each property is a subelement
	# args: root - xmlNode
	# args: task - <Task>
	@staticmethod
	def ConstructXmlNode(root, task):
		#Task.PrintTask(task)
		#Take task and construct xmlNode
		#Gather Node properties
		xmlTaskNode = SubElement(root, "Task")
		#for property in taskProperties:
		for attr, value in task.__dict__.iteritems():
			propertyBody = SubElement(xmlTaskNode, attr)
			propertyBody.text = str(value)
		#return list of InnerXmlNodes for a task
		return root
	
	# Construct an ElementTree by populating it with Xml Nodes
	# constructed by TaskLibraryIO.ConstructXmlNode()
	# args: taskLibraryDictOnFile - Python Dict<uuid,Task> {}
	# args: targetFileName - <string>
	@staticmethod
	def ConstructXmlDocument(taskLibraryDictOnFile, targetFileName):
		# for every element in taskLibraryDictOnFile
		root = Element('TaskLibrary')
		
		for task in taskLibraryDictOnFile:
			TaskLibraryIO.ConstructXmlNode(root, taskLibraryDictOnFile[task])
		
		# Create Tree and Write to the targetFileName	
		tree = ET.ElementTree(root)
		tree.write(targetFileName,
           xml_declaration=True,encoding='utf-8',
           method="xml")
		return tree
	
	# proceed to overwrite the the task file
	# by constructing a new xml document via TaskLibrary.ConstructXmlDocument()
	# args: taskLibraryDictOnFile - Python Dict<uuid,Task> {}
	# args: targetFileName - <string>
	@staticmethod
	def OverwriteTaskLibrary(taskLibraryDictOnFile, targetFileName):
		print("Overwriting Task Library on File:", targetFileName)
		treeDocument = TaskLibraryIO.ConstructXmlDocument(taskLibraryDictOnFile, targetFileName)


	# Takes all Tasks In memory, and writes them to file specified by
	# targetXmlFileName
	# args: taskLibrary - Python Dict<uuid,Task> {} 
	# args: targetXmlFileName - <string>
	@staticmethod
	def SyncTaskLibrary(taskLibrary, targetXmlFileName):
		modifiedTasks = []
		newTasks = []
		removedTasks = []
		nonModifiedTasks = []
		tasksOnDiskNotOnMemory = []
		newTaskLibrary = {}
		
		# Read all elements from Task File Directory in temp Task Library
		dictionary = TaskLibraryIO.Walk()
		
		# Get list of removed tasks
		# removed tasks are tasks in TaskLibrary.TaskRecyclingBin
		tasksRemoved = taskLibrary.TaskRecyclingBin.GetRecycledTasks()
		for task in tasksRemoved:
			if task.TaskId in dictionary:
				removedTasks.append(task)
		print("TaskRecyclingBin Dumped")
		taskLibrary.TaskRecyclingBin.DumpRecyclingBin()
		
		# Get list of new tasks
		# new tasks are tasks in tasks in memory but not in tasks in file
		taskIdsInMemory = taskLibrary.GetAllTaskIds()
		print("Tasks in memory:", len(taskIdsInMemory), "\n")
		print("Tasks on disk:", len(dictionary), "\n")
		
		for key in dictionary.keys():
			if key not in taskIdsInMemory:
				tasksOnDiskNotOnMemory.append(key)
		
		for key in taskIdsInMemory:
			# Existing Tasks
			if key in dictionary.keys():
				# Modified Tasks
				task = taskLibrary.dict[key]
				if task.TaskDirty == True:
					modifiedTasks.append(task)
					newTaskLibrary[key] = task
				# Existing, Non-dirty Tasks
				else:
					nonModifiedTasks.append(task)
					newTaskLibrary[key] = task
			# New Tasks
			else:
				newTasks.append(taskLibrary.dict[key])
				newTaskLibrary[key] = taskLibrary.dict[key]
		
		# Print list of Tasks on disk but not on Memory
		print("Tasks on Disk, Not in Memory:", len(tasksOnDiskNotOnMemory))
		for taskId in tasksOnDiskNotOnMemory:
			#Task.PrintTask(task)
			print(taskId)
		
		# Print list of NonModified Tasks
		print("nonModified Tasks:", len(nonModifiedTasks))
		for task in nonModifiedTasks:
			#Task.PrintTask(task)
			print(task.TaskId)
		
		# Print list of updated Tasks
		print("Modified Tasks:", len(modifiedTasks))
		for task in modifiedTasks:
			#Task.PrintTask(task)
			print(task.TaskId)
		
		# Print list of removed Tasks
		print("Removed Tasks:", len(removedTasks))
		for task in removedTasks:
			#Task.PrintTask(task)
			print(task.TaskId)
		
		# Print list of new Tasks
		print("New Tasks:", len(newTasks))
		for task in newTasks:
			#Task.PrintTask(task)
			print(task.TaskId)
			
		# Mark all tasks Clean
		for key in newTaskLibrary:
			newTaskLibrary[key].TaskDirty = False
		
		# Write over all Tasks that were updated
		TaskLibraryIO.OverwriteTaskLibrary(taskLibraryDictOnFile = newTaskLibrary, targetFileName = targetXmlFileName)
		
		# Replace taskLibrary.dict with newTaskLibrary
		taskLibrary.dict = newTaskLibrary
		
		# print all tasks in taskLibrary
		print("All Tasks in SyncedLibrary:", len(taskLibrary.dict))
		for key in taskLibrary.dict:
			print(key)
		
		# Clean all TaskDirty flags in taskLibrary
		taskLibrary.MarkAllTasksClean()
		
		return taskLibrary
				
	@staticmethod
	def PushToTaskLibrary(taskLibrary):
		ProgramHandler().eprint(ErrorTypes.NotImplementedError,"TaskLibraryIO","PushToTaskLibrary", sep=":")
		