# Created by qdljerry
# 2022/8
# The standard unit is kPa

from objc_util import ObjCInstance, ObjCClass, ObjCBlock, c_void_p
import time
import ctypes

class pressure:
	def pressure(self):
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
		return self.pressure
	
	def handler(self, _cmd, _data, _error):
		self.pressure = ObjCInstance(_data).pressure().floatValue()
		self.flag = True
