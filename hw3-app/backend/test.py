import unittest
from app import app

class Testing(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def testgetapikey(self):
        response = self.app.get('/api/key')
        self.assertEqual(response.status_code, 200)

    def testhomepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
