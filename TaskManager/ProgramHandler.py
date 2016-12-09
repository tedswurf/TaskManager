from __future__ import print_function
import sys

class ProgramHandler:
	@staticmethod
	def eprint(*args, **kwargs):
		print(*args, file=sys.stderr, **kwargs)
		
class ErrorTypes:
	InvalidFileNameError = "InvalidFileNameError"
	UnknownCriticalError = "UnknownCriticalError"
	ArgumentNullError = "ArgumentNullError"
	NotImplementedError = "NotImplementedError"
	InvalidInnerXmlTagError = "InvalidInnerXmlTagError"
	InvalidAttributeSetterError = "InvalidAttributeSetterError"
	DictionaryCollisionError = "DictionaryCollisionError"
	DictionaryIndexDoesNotExistError = "DictionaryIndexDoesNotExistError"