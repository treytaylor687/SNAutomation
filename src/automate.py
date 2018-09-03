import sys
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class SerialSet:
        def __init__(self, fileName, driver, user, password):
            self.fn = fileName
            self.failedSerials = []
            self.chromedriver = driver
            os.environ["webdriver.chrome.driver"] = self.chromedriver
            self.driver = webdriver.Chrome(self.chromedriver)
            self.aloSuccess = False
            self.user = user
            self.password = password

        def parseSerialFile(self):
            with open(self.fn, 'r') as f:
                self.serials = [line.strip() for line in f]

        def setCountrySN(self, serial, driver):
            driver.find_element_by_xpath("//select/option[@value='USA']").click()
            driver.find_element_by_id("serialno").send_keys(serial)
            driver.find_element_by_xpath("//input[@value='Continue'][@type='button']").click()

        def submitState(self, driver):
            driver.find_element_by_xpath("//select/option[@value='CT']").click()
            driver.find_element_by_id("Continue1").click()

        def login(self, driver):
            driver.find_element_by_xpath("//*[@id='accountname']").send_keys(self.user)
            driver.find_element_by_xpath("//*[@id='accountpassword']").send_keys(self.password)
            driver.find_element_by_xpath("//*[@id='signInHyperLink']").click()

        def initiateSN(self, serial, driver):
            try:
                # select country and enter serialno
                driver.get("http://supportform.apple.com/201110/")
                time.sleep(3)
                self.setCountrySN(serial, driver)

                # enter login
                time.sleep(3)
                if driver.current_url == "http://supportform.apple.com/201110/":
                    return False
                self.login(driver)

                # select state and continue
                time.sleep(3)
                self.submitState(driver)

                # final submit
                time.sleep(3)
                driver.find_element_by_id("finalContinue").click()
                return True
            except NoSuchElementException:
                return 1

        def newSN(self, serial, driver):
            try:
                # select country and enter serialno
                driver.get("http://supportform.apple.com/201110/")
                time.sleep(3)
                self.setCountrySN(serial, driver)

                # select state and continue
                time.sleep(3)
                if driver.current_url == "http://supportform.apple.com/201110/":
                    return False
                self.submitState(driver)

                # final submit
                time.sleep(3)
                driver.find_element_by_id("finalContinue").click()
                return True
            except NoSuchElementException:
                return 1

        def automateSerials(self):
            for i in self.serials:
                if self.aloSuccess == False:
                    if not self.initiateSN(i, self.driver):
                        self.failedSerials.append(i)
                        del i
                    elif self.initiateSN(i, self.driver) == 1:
                        self.initiateSN(i, self.driver)
                    else:
                        self.aloSuccess = True
                else:
                    if not self.newSN(i, self.driver):
                        self.failedSerials.append(i)
                        del i
                    elif self.newSN(i, self.driver) == 1:
                        self.newSN(i, self.driver)
            self.driver.quit()
            print(str(len(self.serials) - len(self.failedSerials)) + ":" + str(len(self.serials)))

        def getpage(self, pageURL):
            self.driver.get(pageURL)
def main():
    newSet = SerialSet(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    newSet.parseSerialFile()
    newSet.automateSerials()

if __name__ == "__main__":
    main()
