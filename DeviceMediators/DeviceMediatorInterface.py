
class DeviceMediatorInterface(object):
	'''
	Interface for device controllers. All devices used in the PAT apparatus
	should implement its methods, and settings dictionaries for mediators should
	include the field within __init__
	'''
	
	def __init__(self):
		self.takeData = True	
		self.dataFolderName = "DatafolderUnspecified"
	
	def save(self, path):
		'''Save the data associated with the device to the path given.'''
		raise NotImplementedError()
		
	def start(self):
		'''Initialise the device for an experimental run.'''
		raise NotImplementedError()
		
	def stop(self):
		'''Stop a device after an experimental run.'''
		raise NotImplementedError()	
 