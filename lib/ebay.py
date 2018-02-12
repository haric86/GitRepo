import logging
from appium import webdriver
from core.shell import run_cmd
from lib.adb_util import send_txt, send_key


class EBay(object):

    def __init__(self, driver: webdriver.Remote):
        self.log = logging.getLogger(__name__)
        self.driver = driver

    def login(self, username, pwd):
        self.log.info('Open Main navigation')
        self.driver.find_element_by_accessibility_id(
            'Main navigation, open').click()
        self.log.info('Opened Main navigation')

        self.log.info('Open SIGN IN page')
        self.driver.find_element_by_accessibility_id(
            'Sign in,double tap to activate').click()
        self.log.info('Opened SIGN IN page')

        send_txt(username)
        send_key('tab')
        send_txt(pwd)
        send_key('enter')
