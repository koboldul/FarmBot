import unittest
from sch_reader import ScheduleReader
from device import Device
from device import DeviceTime

class ScheduleReaderTest(unittest.TestCase):
    def test_get_devices(self):
        devices = ScheduleReader.get_devices()
        self.assertEqual(3, len(devices))
        
        valve = next((x for x in devices if x['id'] == 'v'))
        self.assertEqual(valve['weather_dependent'], 1, valve)
        sprinkler = next((x for x in devices if x['id'] == 'k'))
        self.assertEqual(sprinkler['weather_dependent'], 1, 'sprinklers')
        pump = next((x for x in devices if x['id'] == 'p'))
        self.assertEqual(pump['weather_dependent'], 0, 'pump')

    def test_instantiate_device(self):
        data = {
			"name": "vegetables",
			"weather_dependent": 1,
			"is_on": 1,
			"id": "v",
			"pin": 4,
			"time": [ 
				{"id": 1, "start" : "5:45", "stop": "6:00", "skip_days": "1"},
				{"id": 2, "start" : "21:45", "stop": "22:00", "skip_days": "1"}
			]
		}
        device = Device.init_from_json(None, data)
        self.assertEqual(device.name, 'vegetables')
        self.assertEqual(device.pin, 4)
        self.assertEqual(device.weather_dependent, 1)
        self.assertEqual(len(device.time_table), 2)
                    
    def test_instantiate_device_time(self):
        data = {"id": 1, "start" : "5:45", "stop": "6:00", "skip_days": "4"}

        time = DeviceTime.init_from_json(data)
        self.assertEqual(time.start_hour, 5)
        self.assertEqual(time.start_minute, 45)
        self.assertEqual(time.stop_hour, 6)
        self.assertEqual(time.stop_minute, 0)
        self.assertEqual(time.frequency, 4)

if __name__ == '__main__':
    unittest.main()