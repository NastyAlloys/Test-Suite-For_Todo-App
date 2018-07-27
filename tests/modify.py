import os
import unittest
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class ModifyTodoTest(unittest.TestCase):
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
        desired_caps['dontStopAppOnReset'] = 'true'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()
    
    def test_modify_todo(self):
        self.driver.implicitly_wait(10)
        # находим ListView
        listView = self.driver.find_elements_by_id("fr.stevenfrancony.mytodolist:id/list")
        #  находим последний элемент
        lastTask = listView[-1]

        lastTask.click()
        
        # заполняем поля новыми данными
        textfields = self.driver.find_elements_by_class_name("android.widget.EditText")
        textfields[0].clear()
        textfields[0].send_keys("Pet the dog")
        textfields[1].clear()
        textfields[1].send_keys("Find purple dog named Petrovich and pet him")

        newName = textfields[0].text
        newTask = textfields[1].text

        self.assertEqual("Pet the dog", newName)
        self.assertEqual("Find purple dog named Petrovich and pet him", newTask)
        # убираем клавиатуру, чтобы нажатие кнопки прошло безболезненно
        self.driver.keyevent(4)

        self.driver.find_element_by_id("android:id/button1").click()
                
        lastTaskName = lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/pseudo").text
        lastTaskDescription = lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/text").text

        self.assertEqual(newName, lastTaskName)
        self.assertEqual(newTask, lastTaskDescription)

    def test_cancel_modify_todo(self):
        self.driver.implicitly_wait(10)
        listView = self.driver.find_elements_by_id("fr.stevenfrancony.mytodolist:id/list")
        lastTask = listView[-1]

        oldName = lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/pseudo").text
        oldTask = lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/text").text

        lastTask.click()

        # заполняем поля новыми данными
        textfields = self.driver.find_elements_by_class_name("android.widget.EditText")
        textfields[0].clear()
        textfields[0].send_keys("Pet the dog")
        textfields[1].clear()
        textfields[1].send_keys("Find purple dog named Petrovich and pet him")

        newName = textfields[0].text
        newTask = textfields[1].text

        self.assertEqual("Pet the dog", newName)
        self.assertEqual("Find purple dog named Petrovich and pet him", newTask)

        self.driver.keyevent(4)

        self.driver.find_element_by_id("android:id/button2").click()

        self.assertEqual(oldName, lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/pseudo").text)
        self.assertEqual(oldTask, lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/text").text)

if __name__ == '__main__':
    unittest.main(verbosity=2)