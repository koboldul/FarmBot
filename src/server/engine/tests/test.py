from weather.weather_report_current import WeatherReportCurrent
from notifier import Notifier
from weather_report_historical import WeatherReportHistorical
from watering_response import WateringResponse
from datetime import datetime


#c = WeatherReportCurrent(None, Notifier())
#resp = c.get_watering_response([])

#print 'ddd {0}'.format(resp)


h = WeatherReportHistorical(None, Notifier())
hist = [None, None]
wr1 =  datetime.now()
hist.append(wr1)
wr2 =  datetime.now()
wr2.replace(day=20) 

hist.append(wr2)

resp = h.get_watering_response(hist)

print (resp)
