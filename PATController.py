"""
PAT Experiment Controller
"""
from UTBus1 import AnalogOutput, DigitalOutput, DDS
from UTBus1 import Recipe
from UTBus1.Globals import MHz
from UTBus1_Globals import lock_DDS_params
from UTBus1.Exceptions import *	# Make this explicit
import math as mth
from Database import experiment_devices

from DefaultSettings.Settings import Settings
from DeviceMediators.DummyCameraMediator import CameraMediator
from DeviceMediators.DummyScopeMediator import ScopeMediator
from SaveController import SaveController

class PATController(Recipe):

    def __init__(self, controllerName, settingsDict, **kw):        
        Recipe.__init__(self,controllerName,**kw)
        self.start()
        _D = experiment_devices['PAT']	# PAT Database Settings
        self.__devices = {}
        for (name,addr) in _D['DDS'].items():	# Creates DDS Functions
            self.__devices[addr] = d = DDS(address=addr)
            setattr(self,name,d)

        for (name,addr) in _D['AO'].items():	# Create AO Functions
            self.__devices[addr] = d = AnalogOutput(address=addr)
            setattr(self,name,d)

        for (name,data) in _D['DO'].items():	# Creates DO Functions
            (addr,port) = data
            if not addr in self.__devices:
                self.__devices[addr] = d = DigitalOutput(address=addr)
            setattr(self,name,self.__build_DO_method(name,addr,port))

        self.deviceDict = {}
        deviceSettings  = settingsDict['deviceSettings']
        generalSettings = settingsDict['generalSettings']

        # Create device mediators using device settings.
        for (key, deviceData) in deviceSettings.items():
            constructor = globals()[deviceData[0]]
            self.deviceDict[key] = constructor(deviceData[1])

        # Create settings objects from general settings.
        for (key, deviceData) in generalSettings.items():
            constructor = globals()[deviceData[0]]
            setattr(self, key, constructor(deviceData[1]))

        settingsDict.save(self.SaveController.expPath)
		
        self.__camera_triggers = 0

    def __build_DO_method(self,name,addr,port):
    	'''Constructs Digital Output functions dynamically'''
        def DO_method(v):
            self.__devices[addr].set_bit(port,v)
        DO_method.func_name = name
        return DO_method

    def start(self):
        self.__camera_triggers = 0
        Recipe.start(self)
        
    def startDevices(self):
    	for device in self.deviceDict.values():
    		device.start()

    def save(self):
		path = self.SaveController.dataPath
		for dev in self.deviceDict.values():
			if dev.takeData: 
				dev.save(path)

    def cable3_ttl(self,value=0):
        self.testcable3(value)

## ========================================================================
# PAT coil controls

# PAT Coils
    def set_2D_I_1(self, A = None): # Set the coil current in amperes
        if A is None: A = self.PATSettings['2D_I_1']
        print "Setting the 2D Coil 1 on to: %.6f" %A
        if mth.fabs(A) > 5.0:
            print "Current setting too high (> 5.0A). Current not set."
        else:
            self.MOT_2Dcoil_1.set_scaled_value(A/0.5) # current = 0.5 A/V

    def set_2D_I_2(self, A = None): # Set the coil current in amperes
        if A is None: A = self.PATSettings['2D_I_2']
        print "Setting the 2D Coil 1 on to: %.6f" %A
        if mth.fabs(A) > 5.0:
            print "Current setting too high (> 5.0A). Current not set."
        else:
            self.MOT_2Dcoil_2.set_scaled_value(A/0.5) # current = 0.5 A/V

    def set_2D_I_3(self, A = None): # Set the coil current in amperes
        if A is None: A = self.PATSettings['2D_I_3']
        print "Setting the 2D Coil 1 on to: %.6f" %A
        if mth.fabs(A) > 5.0:
            print "Current setting too high (> 5.0A). Current not set."
        else:
            self.MOT_2Dcoil_3.set_scaled_value(A/0.5) # current = 0.5 A/V

    def set_2D_I_4(self, A = None): # Set the coil current in amperes
        if A is None: A = self.PATSettings['2D_I_4']
        print "Setting the 2D Coil 1 on to: %.6f" %A
        if mth.fabs(A) > 5.0:
            print "Current setting too high (> 5.0A). Current not set."
        else:
            self.MOT_2Dcoil_4.set_scaled_value(A/0.5) # current = 0.5 A/V

    def set_3D_coils_I(self, A = None): # Set the coil current in amperes
        if A is None: A = self.PATSettings['3D_coils_I']
        print "Setting the PAT Coils on to: %.6f" %A
        if mth.fabs(A) > 5.0:
            print "Current setting too high (> 5.0A). Current not set."
        else:
            self.MOT_3Dcoils.set_scaled_value(A/0.5) # current = 0.5 A/V

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PAT Laser controls

    def set_2DRb_pump_detuning(self, detuning = None):  # The usual detuning is -12 MHz
        if detuning is None: detuning = self.PATSettings['2DRb_pump_detuning']
        if mth.fabs(detuning) < 66.0:
            DDS_freq = 90.0 - detuning/2.0
            self.Rb_2Dpump.single_tone(DDS_freq*MHz)
            print 'setting 2D pump AOM to %.6f'%detuning
        else:
            print 'Error: 2D Pump detuning frequency greater than 60 MHz.'

    def set_3DRb_pump_detuning(self, detuning = None):  # The usual detuning is -12 MHz
        if detuning is None: detuning = self.PATSettings['3DRb_pump_detuning']
        if mth.fabs(detuning) < 66.0:
            DDS_freq = 90.0 - detuning/2.0
            self.Rb_3Dpump.single_tone(DDS_freq*MHz)
            print 'setting 3D pump AOM to %.6f'%detuning
        else:
            print 'Error: 3D Pump detuning frequency greater than 60 MHz.'

    def set_Rb_repump_detuning(self, detuning = None):
        if detuning is None: detuning = self.PATSettings['Rb_repump_detuning']
        if mth.fabs(detuning) < 64.0:
            DDS_freq = 90.0 - detuning/2.0
            self.Rb_repump.single_tone(DDS_freq*MHz)
            print 'setting repump AOM to %.6f'%detuning
        else:
            print 'Error: Repump detuning frequency greater than 60 MHz.'

    def set_Rb_push_detuning(self, detuning = None):
        if detuning is None: detuning = self.PATSettings['Rb_push_detuning']
        if mth.fabs(detuning) < 64.0:
            DDS_freq = 90.0 + detuning/2.0
            self.Rb_push.single_tone(DDS_freq*MHz)
            print 'setting push AOM to %.6f'%detuning
        else:
            print 'Error: Push detuning frequency greater than 60 MHz.'

    def set_2DRb_pump_amplitude(self, amplitude = None):
    	if amplitude is None: amplitude = self.PATSettings['2DRb_pump_amplitude']
        if amplitude > 1.0:
            print "AOM amplitude too high (>1.0). Setting amplitude to 1.0"
            amplitude = 1.0
        self.Rb_2Dpump.set_amplitude(amplitude)
        print "2D Rb Pump amplitude set to %.3f" %amplitude

    def set_3DRb_pump_amplitude(self, amplitude = None):
        if amplitude is None: amplitude = self.PATSettings['3DRb_pump_amplitude']
        if amplitude > 1.0:
            print "3D Pump amplitude too high (> 1.0). Setting amplitude to 1.0"
            amplitude = 1.0
        print 'setting 3D pump amplitude to %.3f'%amplitude
        self.Rb_3Dpump.set_amplitude(amplitude)

    def set_Rb_repump_amplitude(self, amplitude = None):
        if amplitude is None: amplitude = self.PATSettings['Rb_repump_amplitude']
        if amplitude > 1.0:
            print "Repump amplitude too high (> 1.0). Setting repump amplitude to 1.0"
            amplitude = 1.0
        print 'setting repump amplitude to %.3f'%amplitude
        self.Rb_repump.set_amplitude(amplitude)

    def set_Rb_push_amplitude(self, amplitude = None):
        if amplitude is None: amplitude = self.PATSettings['Rb_push_amplitude']
        if amplitude > 1.0:
            print "Push amplitude too high (> 1.0). Setting repump amplitude to 1.0"
            amplitude = 1.0
        print 'setting push amplitude to %.3f'%amplitude
        self.Rb_push.set_amplitude(amplitude)

    def pat_lasers_on(self):
       # self.set_2DRb_pump_amplitude(0.5)
        self.set_3DRb_pump_amplitude(0.8)
        self.set_Rb_repump_amplitude(0.8)
       # self.set_Rb_push_amplitude(0.6)
        print 'lasers on'

    def pat_3DMOT_lasers_on(self):
        self.set_3DRb_pump_amplitude(0.8)
        self.set_Rb_repump_amplitude(0.8)
        print 'lasers on'

    def pat_3DMOT_lasers_off(self):
        self.set_3DRb_pump_amplitude(0.0)
        self.set_Rb_repump_amplitude(0.0)
        print 'lasers on'

    def pat_lasers_off(self):
        self.set_2DRb_pump_amplitude(0.0)
        self.set_3DRb_pump_amplitude(0.0)
        self.set_Rb_repump_amplitude(0.0)
        self.set_Rb_push_amplitude(0.0)

    def pat_2DMOT_off(self):
        self.set_2DRb_pump_amplitude(0.0)
        self.set_Rb_push_amplitude(0.0)
        self.set_2D_I_1(0.0)
        self.set_2D_I_2(0.0)
        self.set_2D_I_3(0.0)
        self.set_2D_I_4(0.0)

    def pat_2DMOT_all_off(self):
        self.set_2DRb_pump_amplitude(0.0)
        self.set_Rb_push_amplitude(0.0)
        self.set_2D_I_1(0.0)
        self.set_2D_I_2(0.0)
        self.set_2D_I_3(0.0)
        self.set_2D_I_4(0.0)

    def pat_2DMOT_lasers_off(self):
        self.set_2DRb_pump_amplitude(0.0)
        self.set_Rb_push_amplitude(0.0)

    def pat_2DMOT_lasers_on(self):
        self.set_2DRb_pump_amplitude(0.5)
        self.set_Rb_push_amplitude(0.6)

    def pat_2DMOT_Bfield_off(self):
        self.set_2D_I_1(0.0)
        self.set_2D_I_2(0.0)
        self.set_2D_I_3(0.0)
        self.set_2D_I_4(0.0)

    def pat_2DMOT_on(self):
        self.set_2DRb_pump_amplitude(0.5)
        self.set_Rb_push_amplitude(0.6)
        self.set_2D_I_1(3.9)
        self.set_2D_I_2(5.0)
        self.set_2D_I_3(-5.0)
        self.set_2D_I_4(4.4)

    def pat_2DMOT_Bfield_on(self):
        self.set_2D_I_1(3.9)
        self.set_2D_I_2(5.0)
        self.set_2D_I_3(-5.0)
        self.set_2D_I_4(4.4)
# #------------------------------------------------------------------------
# #Shutter controls and trigger controls
    def trig_scope_on(self):
        print 'Triggering scope'
        self.pat_scope_trig(1)

    def trig_scope_off(self):
        self.pat_scope_trig(0)
