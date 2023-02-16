# Created by qdljerry
# 2022/8
# The standard unit is meter(m) or feet(ft)
# The unit of QNH is hPa
# WARNING: This library only work when MSL under 11km

from objc_util import ObjCInstance, ObjCClass, ObjCBlock, c_void_p
import time
import ctypes

class altimeter:
	def __init__(self, QNH = 1013.25, unit = 'm'):
		self.qnh = QNH / 10
		self.unit = unit
	
	def start_update(self):
		pass
	
	def stop_update(self):
		pass
	
	def get_altitude(self):
		self.flag = False
		handler_block = ObjCBlock(self.handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])
		CMAltimeter = ObjCClass('CMAltimeter')
		NSOperationQueue = ObjCClass('NSOperationQueue')
		if not CMAltimeter.isRelativeAltitudeAvailable():
			raise NoAltimeterAvailable
			return -1
		altimeter = CMAltimeter.new()
		main_q = NSOperationQueue.mainQueue()
		altimeter.startRelativeAltitudeUpdatesToQueue_withHandler_(main_q, handler_block)
		while not self.flag:
			pass
		altimeter.stopRelativeAltitudeUpdates()
		alt = (273+15)/-6.5e-3 * ((self.pressure/self.qnh)**((8.3144598*-6.5e-3)/(-9.80665*0.0289644))-1)
		if self.unit == 'm':
			return alt
		elif self.unit == 'ft':
			return alt/0.3048
		else:
			raise RuntimeError('UnSupportedUnit')
	
	def handler(self, _cmd, _data, _error):
		self.pressure = ObjCInstance(_data).pressure().floatValue()
		self.flag = True
