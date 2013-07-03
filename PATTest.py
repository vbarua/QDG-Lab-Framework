from DefaultSettings.SettingsConsolidator import defaultSettings, overwriteSettings
from OverwriteSettings import MOTLoadDataCap
from PATController import PATController
from time import sleep

#updatedSettings = overwriteSettings(defaulttettings, MOTLoadCap



PATCtrl = PATController('testApparatus', defaultSettings)
PATCtrl.start()


# PATCtrl.set_2D_I_1(3.9)
# PATCtrl.set_2D_I_2(5.0)
# PATCtrl.set_2D_I_3(-5.0)
# PATCtrl.set_2D_I_4(4.4)

PATCtrl.close_all_shutters()

# PATCtrl.set_3D_coils_I(1.2)

# PATCtrl.set_3DRb_pump_amplitude(0.8)
# PATCtrl.set_3DRb_pump_detuning(12)

# PATCtrl.set_2DRb_pump_amplitude(0.5)
# PATCtrl.set_2DRb_pump_detuning(12)

# PATCtrl.set_Rb_repump_amplitude(0.8)
# PATCtrl.set_Rb_repump_detuning(5)

# PATCtrl.set_Rb_push_amplitude(0.6)
# PATCtrl.set_Rb_push_detuning(12)
# PATCtrl.wait_s(300)
# PATCtrl.pat_2DMOT_off()

PATCtrl.open_all_shutters()


PATCtrl.startDevices()
PATCtrl.end()
PATCtrl.stopDevices()
PATCtrl.save()
PATCtrl.stopDevices()
PATCtrl.save()
