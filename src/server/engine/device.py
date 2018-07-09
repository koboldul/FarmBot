try:
	import RPi.GPIO as io
except RuntimeError:
	print('Not on a pi')
import logging 

class DeviceTime(object):
    def __init__(self, start_hour=0, start_minute=0, stop_hour=0, stop_minute=0, fq=1):
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.stop_hour = stop_hour
        self.stop_minute = stop_minute
        self.frequency = fq
    
    @classmethod
    def init_from_json(cls, time_entry):
        start = time_entry['start']
        stop = time_entry['stop']

        if not (':' in start) or not (':' in stop):
            raise ValueError('Argument not good!')

        return cls(
            int(start.split(':')[0]),
            int(start.split(':')[1]),
            int(stop.split(':')[0]),
            int(stop.split(':')[1]),
            int(time_entry['skip_days']))
	
class Device(object):
	def __init__(self, pin, name, id, logger, weather_dependent=False, time_table=[]):
		self.weather_dependent = weather_dependent
		self.pin = pin
		self.name = name
		self.logger = logger
		self.time_table = time_table
		self.id = id

	@classmethod
	def init_from_json(cls, logger, device):
		pin = device['pin']
		name = device['name']
		wd = bool(device['weather_dependent'])
		id = device['id']
		time_table = [DeviceTime.init_from_json(t) for t in device['time']]		
		return cls(pin, name, id, logger, wd, time_table)

	def add_device_time(self, start_hour, start_minute, stop_hour, stop_minute):
			self.time_table.append(DeviceTime(start_hour, start_minute, stop_hour, stop_minute))

	def start_device(self):
		try:
			self.logger.log('Starting device ' + self.name + ' on pin ' + str(self.pin))
			io.setup(self.pin, io.OUT)
			io.output(self.pin, io.LOW)
			self.logger.notify('Started ' + self.name + ' on pin ' + str(self.pin), 'Device {0} started'.format(self.name))
		except Exception as e:
			self.logger.notify('Error on starting ' + self.name + ' on pin ' + str(self.pin) + ' ERROR: ' + str(e), \
                'Error')
			return False
		
		return True
	def stop_device(self):
		self.logger.log('Stopping device ' + self.name + ' on pin ' + str(self.pin))
		io.setup(self.pin, io.OUT)
		io.output(self.pin, io.HIGH)
		self.logger.notify('Stopped device ' + self.name + ' on pin ' + str(self.pin), 'Device {0} stopped'.format(self.name))
		
			
		
	
