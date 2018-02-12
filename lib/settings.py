import logging

logger = logging.getLogger(__name__)


class Settings(object):

    def __init__(self, port, driver):
        self.driver = driver

    def turn_on_bluetooth(self):
        logger.info('Turn ON Bluetooth')
        elements = self.driver.find_elements_by_class_name('android.widget.TextView')
        for ele in elements:
            if ele.text == 'Bluetooth':
                ele.click()
                break
            logger.warning(ele.text)
        # self.driver.find_element_by_name('Bluetooth').click()
        logger.info('Turned ON Bluetooth')
