import RPi.GPIO as GPIO
import sys
import apscheduler
import datetime

from sch_reader import ScheduleReader
from notifier import Notifier
from device import Device
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from weather.weather_report_current import WeatherReportCurrent
from weather.weather_report_historical import WeatherReportHistorical

#init stuff

GPIO.setmode(GPIO.BCM)

_notifier = Notifier()
_currentWeatherReporter = WeatherReportCurrent(None, _notifier)
_weatherReporter = WeatherReportHistorical(_currentWeatherReporter, _notifier)

_scheduler = BackgroundScheduler()

rained_at =[None]*36

#utility functions
def load_schedule():
    try:
        data = ScheduleReader.get_devices()
        return [Device.init_from_json(_notifier, x) for x in data]
    except IOError:
        _notifier.notify('Error reading data schedule', 'ScheduleRead')
        raise

def shift(seq, el):
    return [el] + seq[:len(seq)-1]

def start_device(device):
    global rained_at
    
    if device.weather_dependent:
        waterDecision = _weatherReporter.get_watering_response(rained_at)
        if waterDecision.should_water:
            device.start_device()
        else:
            _notifier.notify(f'Skipping watering for {device.name} because of the rainy weather', 'Watering skipped')
    else:
        device.start_device()

def add_to_scheduler(scheduler, device):
    for dTime in device.time_table:
        scheduler.add_job(lambda: start_device(device), 'cron', hour=dTime.start_hour, minute=dTime.start_minute, misfire_grace_time=None)
        scheduler.add_job(lambda: device.stop_device(), 'cron', hour=dTime.stop_hour, minute=dTime.stop_minute, misfire_grace_time=None)

def bootstrap():
    try:		
        #daemon mode
        for d in load_schedule():
            add_to_scheduler(_scheduler, d)

        _scheduler.start()
        _notifier.log('Starting app..')
    except Exception as e:
        _notifier.notify('Error {0}'.format(str(e)), "Error scheduling things")

if (__name__ == '__main__'):
    bootstrap()
    try:
        while(True):
            sleep(900)
            waterDecision = _currentWeatherReporter.get_watering_response([])
            if waterDecision.rained_at is not None:
                _notifier.log('Rained at {0}'.format(waterDecision.rained_at))
            rained_at = shift(rained_at, waterDecision.rained_at)
            _notifier.log(rained_at)

    finally:
        _scheduler.shutdown()
        _notifier.notify('Shutting down all stop', 'App stopped')
        GPIO.cleanup()
