import json
import requests
import datetime

from weather_report_base import WeatherReportBase
from watering_response import WateringResponse

class WeatherReportHistorical(WeatherReportBase):
	def __init__(self, successor, logger):
        	super(WeatherReportHistorical, self).__init__(successor, logger)

	def can_handle(self, input):
        	return input is not None and len(input) > 0

	def handle_query(self, input):
		resp = WateringResponse()
		try:
			lastRain = next ((i for i in input if i is not None), None)
			trashold = 360 * 60
			passedSinceLastRain = trashold
        		if lastRain  is not None:
            			self.logger.log("Last rain was at : {0}".format(lastRain))
				passedSinceLastRain = (datetime.datetime.now()-lastRain).total_seconds() 
				self.logger.log('passed since rain : {0}'.format(passedSinceLastRain))
			if passedSinceLastRain < trashold:
                		self.logger.notify('It rained in the last 6 h', 'Not watering because it rained!')
				resp.should_water = False
                
			return resp
		except Exception as e:
			self.logger.log('ERROR: {0}'.format(e))
			return resp
