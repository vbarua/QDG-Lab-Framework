from serial import Serial
from time import sleep, time
import csv

class Stabil_Ion_Controller(Serial):
	
	def __init__(self, port = 0):
		super(Stabil_Ion_Controller, self).__init__(port = port, timeout = 0)
		self.flushInput()
		
	def read(self, size = 32):
		data = super(Stabil_Ion_Controller, self).read(size)
		data = data[:-2]
		return data
		
	def IG1On(self):
		self.write("IG1 ON \r\n")
		sleep(0.5)
		self.flushInput()
	
	def IG1Off(self):
		self.write("IG1 OFF \r\n")
		sleep(0.5)
		self.flushInput()
		
	def IG2On(self):
		self.write("IG2 ON \r\n")
		sleep(0.5)
		self.flushInput()
		
	def IG2ff(self):
		self.write("IG2 OFF \r\n")
		sleep(0.5)
		self.flushInput()
	
	def degasOn(self):
		self.write("DG ON \r\n")
		sleep(0.5)
		self.flushInput()
				
	def getIG1Pressure(self):
		self.write("DS IG1 \r\n")
		sleep(0.1)
		data = self.read()
		value = float(data)
		return value
	
	def getIG2Pressure(self):
		self.write("DS IG2 \r\n")
		data = self.read()
		sleep(0.1)
		value = float(data)
		return value

	def collectData(self, duration_s, secondsPerSample):
		tDat = []
		pDat= []
		tStart = time()
		tEnd = tStart + duration_s
		while (time() < tEnd):
			p = self.getIG1Pressure()
			tDat.append(time())
			pDat.append(p)
			sleep(secondsPerSample - 0.1)
		
		for i in range(len(tDat)):
			tDat[i] = tDat[i] - tStart
		
		csvFile = open('test.csv', 'wb')
		filewriter = csv.writer(csvFile, delimiter = ',')
		filewriter.writerow(['Time (s)', 'Pressures (???)'])
		for i in range(len(tDat)):
			output = [tDat[i], pDat[i]]
			filewriter.writerow(output)
		csvFile.close()
		
		
SIC = Stabil_Ion_Controller(7)
SIC.collectData(25*60, 1)	