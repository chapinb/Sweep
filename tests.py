from app import app
import app as App
import unittest
import os
import shutil

# TODO create teardown to delete db rows for all tables

class TestSweepApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    @staticmethod
    def patroller_cleanup():
        for record in App.Patroller.select():
            record.delete_instance()

    @staticmethod
    def location_cleanup():
        for record in App.Location.select():
            record.delete_instance()

    def test_home_page_content(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')
        if 'Welcome to Sweep!' in result.data:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_patroller_page_content(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/patrollers.html')
        if 'Please select a patroller to update' in result.data:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_patoller_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/patrollers.html')
        self.assertEqual(result.status_code, 200)

    def test_patroller_submit_new(self):
        ddict = {
            "patroller-select": "new-patroller",
            "patroller-name": "Test Patroller Name 01",
            "status": "full-time",
            "button": "update"
        }
        result = self.app.post("/update_patrollers", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Patroller.select().where(App.Patroller.id == 1)[0]

        self.assertEqual('Test Patroller Name 01', a.name)
        self.patroller_cleanup()

    def test_patroller_submit_update(self):
        ddict = {
            "patroller-select": "new-patroller",
            "patroller-name": "Test Patroller Name 02",
            "status": "other",
            "button": "update"
        }
        result = self.app.post("/update_patrollers", data=ddict)

        a = App.Patroller.select().where(App.Patroller.id == 1)[0]

        self.assertEqual('Test Patroller Name 02', a.name)
        self.assertEqual('other', a.status)

        ddict = {
            "patroller-select": "Test Patroller Name 02",
            "patroller-name": "Test Patroller Name 03",
            "status": "part-time",
            "button": "update"
        }
        result = self.app.post("/update_patrollers", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Patroller.select().where(App.Patroller.id == 1)[0]

        self.assertEqual('Test Patroller Name 03', a.name)
        self.assertEqual('part-time', a.status)
        self.patroller_cleanup()

    def test_patroller_submit_delete(self):
        ddict = {
            "patroller-select": "new-patroller",
            "patroller-name": "Test Patroller Name 04",
            "status": "other",
            "button": "update"
        }
        result = self.app.post("/update_patrollers", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Patroller.select().where(App.Patroller.id == 1)[0]

        self.assertEqual('Test Patroller Name 04', a.name)
        self.assertEqual('other', a.status)

        ddict = {
            "patroller-select": "Test Patroller Name 04",
            "patroller-name": "",
            "status": "",
            "button": "delete"
        }
        result = self.app.post("/update_patrollers", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Patroller.select().where(App.Patroller.name == "Test Patroller Name 04").count()

        self.assertEqual(a, 0)
        self.patroller_cleanup()

    def test_locations_page_content(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/locations.html')
        if 'Please select a location to update' in result.data:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_locations_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/locations.html')
        self.assertEqual(result.status_code, 200)

    def test_location_submit_new(self):
        ddict = {
            "select-location": "new-location",
            "location-name": "Test Location Name 01",
            "button": "update"
        }
        result = self.app.post("/update_locations", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Location.select().where(App.Location.id == 1)[0]

        self.assertEqual('Test Location Name 01', a.name)
        self.location_cleanup()

    def test_location_submit_update(self):
        ddict = {
            "select-location": "new-location",
            "location-name": "Test Location Name 02",
            "button": "update"
        }
        result = self.app.post("/update_locations", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Location.select().where(App.Location.id == 1)[0]

        self.assertEqual('Test Location Name 02', a.name)

        ddict = {
            "select-location": "Test Location Name 02",
            "location-name": "Test Location Name 03",
            "button": "update"
        }
        result = self.app.post("/update_locations", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Location.select().where(App.Location.id == 1)[0]

        self.assertEqual('Test Location Name 03', a.name)
        self.location_cleanup()

    def test_location_submit_delete(self):
        ddict = {
            "select-location": "new-location",
            "location-name": "Test Location Name 04",
            "button": "update"
        }
        result = self.app.post("/update_locations", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Location.select().where(App.Location.id == 1)[0]

        self.assertEqual('Test Location Name 04', a.name)

        ddict = {
            "select-location": "Test Location Name 04",
            "location-name": "",
            "button": "delete"
        }
        result = self.app.post("/update_locations", data=ddict)
        self.assertEqual(result.status_code, 302)

        a = App.Location.select().where(App.Location.name == "Test Location Name 04").count()

        self.assertEqual(a, 0)
        self.location_cleanup()


# runs the unit tests in the module
if __name__ == '__main__':
    moved = None
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep.sqlite3")):
        shutil.move(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep.sqlite3"), os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep.sqlite3.bak"))
        moved = True
    unittest.main()
    if moved:
        shutil.move(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep.sqlite3.bak"), os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep.sqlite3"))
