# Created by qdljerry
# 2022/8
# The standard unit is meter(m) or feet(ft)
# The unit of QNH is hPa
# WARNING: This library only work when MSL under 11km

from objc_util import ObjCInstance, ObjCClass, ObjCBlock, c_void_p
import ctypes

class altimeter:
	def __init__(self, QNH = 1013.25, unit = 'm'):
		self.qnh = QNH / 10
		self.unit = unit
		self.alt = None
		self.unitDict = {'m':1.0,'ft':0.3048}
		handler_block = ObjCBlock(self.handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])
		CMAltimeter = ObjCClass('CMAltimeter')
		NSOperationQueue = ObjCClass('NSOperationQueue')
		if not CMAltimeter.isRelativeAltitudeAvailable():
			raise RuntimeError('NoAltimeterAvailable')
		altimeter = CMAltimeter.new()
		main_q = NSOperationQueue.mainQueue()
	
	def start_update(self):
		altimeter.startRelativeAltitudeUpdatesToQueue_withHandler_(main_q, handler_block)
	
	def stop_update(self):
		altimeter.stopRelativeAltitudeUpdates()
	
	def get_altitude(self):
		try:
			return self.alt / self.unitDict[self.unit]
		except:
			raise RuntimeError('UnSupportedUnit') if self.alt != None else RuntimeError('AltimeterNotReady')
	
	def handler(self, _cmd, _data, _error):
		self.pressure = ObjCInstance(_data).pressure().floatValue()
		self.alt = (273+15)/-6.5e-3 * ((self.pressure/self.qnh)**((8.3144598*-6.5e-3)/(-9.80665*0.0289644))-1)
