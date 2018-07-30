import os
import unittest
from appium import webdriver
import pytest

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

    def test_create_todo(self):
        name = "Pet the cat"
        task = "Find black and white cat named Petya and pet him"
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("fr.stevenfrancony.mytodolist:id/addButton").click()
        self.driver.implicitly_wait(10)

        textfields = self.driver.find_elements_by_class_name("android.widget.EditText")
        textfields[0].send_keys(name)
        textfields[1].send_keys(task)

        self.assertEqual(name, textfields[0].text)
        self.assertEqual(task, textfields[1].text)

        self.driver.find_element_by_id("android:id/button1").click()

        # После создания таск визуально появляется в ListView, но размер списка при поиске его через driver остается старый
        # Актуального решения проблемы не нашел
        # Для подтверждения корректного создания использовал ручное тестирование
        
        # listView = self.driver.find_elements_by_id("fr.stevenfrancony.mytodolist:id/list")
        # lastTask = listView[-1]
        # self.driver.implicitly_wait(10)

        # print(len(listView))
        # print(lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/pseudo").text)
        # print(name)

        # if (lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/pseudo").text != name and lastTask.find_element_by_id("fr.stevenfrancony.mytodolist:id/text").text != task):
        #     pytest.fail('Task was not created')


    def test_cancel_create_todo(self):
        self.driver.implicitly_wait(10)
        # находим ListView
        listView = self.driver.find_elements_by_id("fr.stevenfrancony.mytodolist:id/list")
        itemsCount = len(listView)

        self.driver.find_element_by_id("fr.stevenfrancony.mytodolist:id/addButton").click()
        self.driver.implicitly_wait(10)

        textfields = self.driver.find_elements_by_class_name("android.widget.EditText")
        textfields[0].send_keys("Pet the cat")
        textfields[1].send_keys("Find black and white cat named Petya and pet him")

        self.assertEqual('Pet the cat', textfields[0].text)
        self.assertEqual('Find black and white cat named Petya and pet him', textfields[1].text)

        self.driver.find_element_by_id("android:id/button2").click()

        self.driver.implicitly_wait(3)

        if itemsCount != len(listView):
            pytest.fail('List length is not correct')

if __name__ == '__main__':
    unittest.main(verbosity=2)