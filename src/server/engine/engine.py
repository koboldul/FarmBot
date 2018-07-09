try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print('Not on a Pi')

import os 
import sys

from engine.device import Device
from engine.sch_reader import ScheduleReader
from engine.notifier import Notifier

class Engine(object):
    def __init__(self):
        self.notifier = Notifier()
        try:
            GPIO.setmode(GPIO.BCM)
        except Exception:
            print ('Not on a Pi')

        try:
            data = ScheduleReader.get_devices()
            self.devices = [Device.init_from_json(self.notifier, d) for d in data]
        except IOError:
            self.notifier.notify('Error reading data schedule', 'ScheduleRead')
            raise

    def start_device(self, id):
        device = self._get_device_by_id(id)

        if device != None:
            print(f'Starting device {id}')
            device.start_device()
        else:
            print('Unknown device!')

    def stop_device(self, id):
        device = self._get_device_by_id(id)

        if device != None:
            print(f'Stopping device {id}')
            device.start_device()
        else:
            print('Unknown device!')
    
    def stop_all(self):
        print('Stopping all ...')
        for d in self.devices():
            d.stop_device()    
        print('Stopped all.')
        

    @staticmethod
    def get_logs(date=None):
        log = ''
        script_path = os.path.abspath(os.path.dirname(__file__))
        f = os.path.join(script_path, './logs/farming.log')
        if os.path.exists(f):
            try:
                file = open(f, 'r') 
                log = file.read()
            except IOError:
                print ('Cant read farming log!') 
        
        return log
    
    def _get_device_by_id(self, id):
        return next((d for d in self.devices if d.id == id), None)

    @staticmethod
    def dispose():
        try:
            GPIO.cleanup()
        except RuntimeError:
            print ('Not on a Pi')

if (__name__ == '__main__'):
    engine = Engine()

    if sys.argv[1] == 's':
        engine.stop_all()
    else:
        try:
            for i in range(1,len(sys.argv)):
                print ('Starting', str(sys.argv[i]))
                engine.start_device(sys.argv[i])
        except Exception as e:
            print (e)
            print ('Cleaning on error')
            engine.dispose()

