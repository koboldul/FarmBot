import json
import requests
import datetime
from weather_report_base import WeatherReportBase
from engine.private_data import PrivateData
from watering_response import WateringResponse

class WeatherReportForecast(WeatherReportBase):
    def __init__(self, successor, logger):
            super(WeatherReportForecast, self).__init__(successor, logger)
            pv = PrivateData()
            self.url = ('http://api.openweathermap.org/data/2.5/forecast/city?id={0}&APPID={1}'.
                     format(pv.CITY_ID, pv.APP_KEY))

    def should_start_water(self):
        return WateringResponse()
