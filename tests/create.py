import os
import unittest
from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class CreateTodoTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = PATH(
            '../app/TodoTestingApp.apk'
        )
        desired_caps['appPackage'] = 'fr.stevenfrancony.mytodolist'
        desired_caps['appActivity'] = '.SplashActivity'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_add_contacts(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("fr.stevenfrancony.mytodolist:id/addButton").click()
        self.driver.implicitly_wait(10)

        textfields = self.driver.find_elements_by_class_name("android.widget.EditText")
        textfields[0].send_keys("Pet the cat")
        textfields[1].send_keys("Find black and white cat named Petya and pet him")

        self.assertEqual('Pet the cat', textfields[0].text)
        self.assertEqual('Find black and white cat named Petya and pet him', textfields[1].text)

        self.driver.find_element_by_id("android:id/button1").click()

if __name__ == '__main__':
    unittest.main(verbosity=2)