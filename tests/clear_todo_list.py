import os
import unittest
from appium import webdriver
import pytest
from selenium.common.exceptions import NoSuchElementException
from unittest.mock import Mock

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class ClearTodoTest(unittest.TestCase):

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

    def test_clear_todos(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("fr.stevenfrancony.mytodolist:id/clearButton").click()
        self.driver.find_element_by_id("android:id/button1").click()

        self.driver.implicitly_wait(5)

        try:
            self.driver.find_element_by_id("fr.stevenfrancony.mytodolist:id/list")
        except NoSuchElementException:
            print('The list is empty!')
        
    def test_cancel_clear_todos(self):
        self.driver.implicitly_wait(10)
        isEmptyBefore = False
        try:
            self.driver.find_element_by_id("fr.stevenfrancony.mytodolist:id/list")
        except NoSuchElementException:
            isEmptyBefore = True

        self.driver.find_element_by_id("fr.stevenfrancony.mytodolist:id/clearButton").click()
        self.driver.find_element_by_id("android:id/button2").click()

        self.driver.implicitly_wait(3)
        isEmptyAfter = False
        try:
            self.driver.find_element_by_id("fr.stevenfrancony.mytodolist:id/list")
        except NoSuchElementException:
            isEmptyAfter = True

        if isEmptyBefore != isEmptyAfter:
            pytest.fail('List should be present')

if __name__ == '__main__':
    unittest.main(verbosity=2)