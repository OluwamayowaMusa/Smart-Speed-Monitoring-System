import unittest
import subprocess
from threading import Thread
from  utils import running_smart_speed_system, connect_to_database

class TestUtilsFunctions(unittest.TestCase):
	"""
		A Class for testing the functions in the 
		utils module used by the backend framework
	"""
	
	def test_running_smart_speed_system_returns_false_when_command_is_not_running(self):
		filename = "Musa"
		self.assertEqual(False, running_smart_speed_system(filename))
		
	def test_running_smart_speed_system_returns_true_when_command_is_running(self):
		filename = "/home/user/Python/app/tests/setup.py"
		thread_1 = Thread(target=subprocess.run(["python", filename], capture_output=True))
		thread_2 = Thread(self.assertEqual(True, running_smart_speed_system(filename)))
		
	def test_connect_to_database(self):
		db = connect_to_database("localhost", "root", "raspberrypi")
		cursor = db.cursor()
		cursor.execute("SHOW DATABASES")
		data = cursor.fetchone();
		self.assertIsNotNone(data)
