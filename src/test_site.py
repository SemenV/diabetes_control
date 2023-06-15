from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from splineDeriv import *

def test_subslpline():
    service = Service(executable_path='C:\Program Files\Mozilla Firefox\firefox.exe')

    driver = webdriver.Firefox(service=service)

    driver.get("localhost:5000/login")

    driver.find_element(By.ID,"idusername").send_keys("admin")
    driver.find_element(By.ID,"idpassword").send_keys("admin")
    driver.find_element(By.ID,"login").click()



    select = Select(driver.find_element(By.ID,"idselect"))

    select.select_by_value("/new_subspline_nagr")

    driver.find_element(By.ID,"idbuttonss").click()
    driver.find_element(By.ID,"idbuttonss").click()

    driver.find_element(By.NAME,"x0").send_keys("0")
    driver.find_element(By.NAME,"y0").send_keys("0")
    driver.find_element(By.NAME,"yp0").send_keys("0")

    driver.find_element(By.NAME,"x1").send_keys("1")
    driver.find_element(By.NAME,"y1").send_keys("2.2")
    driver.find_element(By.NAME,"yp1").send_keys("0")


    driver.find_element(By.ID,"idsend").click()

    dataFromPage = driver.execute_script('return qwe();')



    a = []
    a.append(0)
    a.append(1)

    b = []
    b.append(0)
    b.append(2.2)

    proizv = []
    proizv.append(0)
    proizv.append(0)





    assert get_spl_prepered(a,b,proizv,0.1) == dataFromPage[1]