# Polonium project
# Author: Bismarck Gomes <bismarckgomes@gmail.com>
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as Service_Chrome
from selenium.webdriver.firefox.service import Service as Service_Firefox
from selenium.webdriver.edge.service import Service as Service_Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep, time
import os, re


class Polonium:

    def __init__(self, driver=None):
        self._driver = driver
    
    def init_driver(self, browser, path_driver, path_data=None, options=None):
        if (path_data is not None):
            if (not os.path.isdir(path_data)):
                path_data = os.path.join(path_driver, path_data)
            
            os.makedirs(path_data, exist_ok=True)

        if (browser.lower() == 'chrome'):
            options = webdriver.ChromeOptions() if options is None else options
            service = Service_Chrome(os.path.join(path_driver, 'chromedriver.exe'))
            driver = webdriver.Chrome

        elif (browser.lower() == 'edge'):
            options = webdriver.EdgeOptions() if options is None else options
            service = Service_Edge(os.path.join(path_driver, 'msedgedriver.exe'))
            driver = webdriver.Edge

        elif (browser.lower() == 'firefox'):
            options = webdriver.FirefoxOptions() if options is None else options
            if (path_data):
                options.add_argument('-profile')
                options.add_argument(path_data)
            service = Service_Firefox(os.path.join(path_driver, 'geckodriver.exe'))
            self._driver = webdriver.Firefox(service=service, options=options)
            
            return self._driver

        else:
            print('Invalid browser:', browser)
            return None

        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if (path_data is not None):
            options.add_argument(f'user-data-dir={path_data}')
        
        self._driver = driver(service=service, options=options)

        return self._driver
    
    def create_xpath(self, tag_name, *args, **kwargs):
        xpath = tag_name if tag_name.startswith("/") else ("//" + tag_name)
        filters = [f'@{arg}' if '@' not in arg else arg for arg in args]
        for key, value in kwargs.pop('contains', []):
            filters.append(f"contains(@{key},'{value}'")
        for key, value in kwargs.items():
            filters.append(f"@{re.sub('_$', '', key).replace('_', '-')}='{value}'")
        
        if (len(args) + len(kwargs)):
            xpath += '[' + ' and '.join(filters) + ']'

        return xpath

    def find_all(self, xpath, *args, **kwargs):
        count = 0
        timeout = 0.5 + kwargs.pop('timeout', 0)
        xpath = self.create_xpath(xpath, *args, **kwargs)
        time_ini = time()
        while (time() - time_ini < timeout):
            elements = self._driver.find_elements(By.XPATH, xpath)
            if (len(elements) > 0):
                break
            count += 1
            sleep(1)
        
        return elements

    def find(self, xpath, *args, **kwargs):
        elements = self.find_all(xpath, *args, **kwargs)

        return elements[0] if (len(elements) > 0) else None

    def click(self, xpath, *args, **kwargs):
        element = self.find(xpath, *args, **kwargs)
        sleep(0.2)
        if (element is not None):
            element.click()
            return True

    def send_keys(self, value, xpath, *args, **kwargs):
        element = self.find(xpath, *args, **kwargs)
        sleep(0.2)
        if (element is not None):
            element.send_keys(value)
            return True

    def text(self, xpath, *args, **kwargs):
        element = self.find(xpath, *args, **kwargs)
        sleep(0.2)
        if (element is not None):
            return element.text
    
    def get_attribute(self, value, xpath, *args, **kwargs):
        element = self.find(xpath, *args, **kwargs)
        sleep(0.2)
        if (element is not None):
            return element.get_attribute(value)

    def wait_until_find(self, xpath, timeout=864000, *args, **kwargs):
        xpath = self.create_xpath(xpath, *args, **kwargs)
        WebDriverWait(self._driver, timeout=timeout).until(lambda d: self.get(xpath))
    
    def wait(self, secs):
        sleep(secs)


if __name__ == '__main__':
    po = Polonium()
    driver = po.init_driver('chrome', 'C:/WebDrivers/chrome', 'User1')
    # driver = po.init_driver('edge', 'C:/WebDrivers/edge', 'User1')
    # driver = po.init_driver('firefox', 'C:/WebDrivers/firefox', 'User1')

    driver.get('http://www.google.com')

    po.send_keys('polonium', 'input', name='q')
    po.click('input', name='btnK')
    po.wait(2)

    print('\nTexto:')
    print(po.text('div/div/div/div/div/span/span'))
    print('\nLinks:')
    for a in po.find_all("cite"):
        if (a.text):
            print('-', a.text)
  