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
    def __init__(self, pin, name, logger, weather_dependent=False, time_table=[]):
        self.weather_dependent = weather_dependent
        self.pin = pin
        self.name = name
        self.logger = logger
        self.time_table = time_table

    @classmethod
    def init_from_json(cls, logger, device):
        pin = device['pin']
        name = device['name']
        wd = bool(device['weather_dependent'])
        time_table = [DeviceTime.init_from_json(t) for t in device['time']]

        return Device(pin, name, logger, wd, time_table)


    def add_device_time(self, start_hour, start_minute, stop_hour, stop_minute):
        self.time_table.append(DeviceTime(start_hour, start_minute, stop_hour, stop_minute))
	
        
