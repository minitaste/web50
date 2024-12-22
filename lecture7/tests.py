import os
import pathlib
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

class WebpageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def test_title(self):
        self.driver.get(file_uri("counter.html"))
        self.assertEqual(self.driver.title, "Counter")

    def test_increase(self):
        self.driver.get(file_uri("counter.html"))
        increase = self.driver.find_element(By.ID, "increase")
        increase.click()
        self.assertEqual(self.driver.find_element(By.TAG_NAME, "h1").text, "1")

    def test_decrease(self):
        self.driver.get(file_uri("counter.html"))
        decrease = self.driver.find_element(By.ID, "decrease")
        decrease.click()
        self.assertEqual(self.driver.find_element(By.TAG_NAME, "h1").text, "-1")

    def test_multi_increase(self):
        self.driver.get(file_uri("counter.html"))
        increase = self.driver.find_element(By.ID, "increase")
        for _ in range(20):
            increase.click()
        self.assertEqual(self.driver.find_element(By.TAG_NAME, "h1").text, "20")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
