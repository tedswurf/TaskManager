from __future__ import print_function
from ProgramHandler import *
import sys
import os.path

class Configure:
	def CheckFilePath(self, fname):
		if(os.path.isfile(fname) is False):
			ProgramHandler().eprint(ErrorTypes.InvalidFileNameError,"Configure","CheckFilePath", sep=":")
			exit
	
	def ReadTMConfiguration(self, TMConfigurationFileName):
		print("Reading TM Configuration")
		self.CheckFilePath(TMConfigurationFileName)