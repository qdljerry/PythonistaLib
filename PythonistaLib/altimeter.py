# Created by qdljerry
# 2022/8
# The standard unit is meter(m) or feet(ft)
# The unit of QNH is hPa

from objc_util import ObjCInstance, ObjCClass, ObjCBlock, c_void_p
import time
import ctypes

class altimeter:
	def __init__(self, QNH = 1005, unit = 'm'):
		self.qnh = QNH / 10
		if unit == 'm':
			self.unit = True
		else:
			self.unit = False
	
	def altitude(self):
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
		alt = 44300*(1-((self.pressure/self.qnh)**(1/5.256)))
		if self.unit:
			return alt
		else:
			return alt/0.3048
	
	def handler(self, _cmd, _data, _error):
		self.pressure = ObjCInstance(_data).pressure().floatValue()
		self.flag = True
