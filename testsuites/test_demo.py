"""
DocString :-
Name      : test_demo.py
Function  : This step file commences the  functionality by invoking the
 	    framework and this file is sole responsible in performing the 
	    intended user operations from commandline as  standalone.
Example   : python.exe main.py -t 4723 -s test_demo.py

"""

# Import Modules
import argparse
import logging
import sys
import time
import unittest
from os.path import dirname, join
from unittest import TestLoader, TestSuite
from globals.app_globals import *

# External module for output HTML log parsing
from HtmlTestRunner import HTMLTestRunner

###################################################################

# Add framework to path
sys.path.insert(0, dirname(dirname(__file__)))
from core.defaults import LOGS_PATH

# Initialize logging
from core.fwk_logger import setup_logging
from lib.adb_util import swipe, send_txt, send_key
from lib.csv_parser import get_credentials
setup_logging()
logger = logging.getLogger('suite')

###################################################################

# Invoking Appium and its functional features
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from lib.json_parser import get_desired_caps
from lib.ebay import EBay


# Using Class metod to perform core functionalities using Unittest
class DemoTest(unittest.TestCase):
    """ 
    This Class method allows to set up Appium and launch its
    Server in Host and then allows to perform user defined
    functionalities by launch Android app

    """
    def setUp(self):
        """
        :Description:
           - This function handles setting up Appium server and connection
         establishment.

        :Parameters:
           - None

        :Return:
           - None

        :AdditionalInfo:
           - Called by the constructor to handle command line parsing.

        :Related:
           - N/A
        """
        # self.log = logging.getLogger('suite')
        self.desired_caps = get_desired_caps(port=port)
        self.driver = webdriver.Remote(
            command_executor=f'http://localhost:{port}/wd/hub',
            desired_capabilities=self.desired_caps)

        # Timeouts in seconds
        self.driver.implicitly_wait(30)

        # Libraries
        self.ebay = EBay(driver=self.driver)

        # Log file
        self.method_name = self.id().rpartition('.')[2]
        logger.info('*** Executing %s ***' % self.method_name)

    def tearDown(self):
        """
        :Description:
           - This function ensures closing the opened app and stopping /
           closing the established Appium server.

        :Parameters:
           - None

        :Return:
           - None

        :AdditionalInfo:
           - Called by the constructor to handle command line parsing.

        :Related:
           - N/A
        """
        logger.info('*** Executing %s completed ***' % self.method_name)
        logger.info('-' * 50)
	self.driver.save_screenshot(filename=join(LOGS_PATH, SS_CAPTURE_TEARDOWN))
        self.driver.quit()

    def test001_login(self):
        """
        :Description:
            - This function helps logging into eBay app and can fetch particular
            user and his password which is not hardcoded and which provides
            easy handles multiple users passed on runtime by dynamically fetching
            from the stored csv in testdata
    
        :Parameters:
            - None
    
        :Return:
            - None
    
        :AdditionalInfo:
            - Called by the constructor to handle command line parsing.
    
        :Related:
            - N/A
        """
        try:
            pwd = get_credentials('admin')
            self.ebay.login(username='admin', pwd=pwd)
        except:
            logger.error('Login operation failed')
            self.driver.save_screenshot(filename=join(LOGS_PATH, Screenshot.SS_CAPTURE_LOGIN))

    def test002_select(self):
        """
        :Description:
           - This function performs product selection operation by clicking the
           required product in the eBay app

        :Parameters:
           - None

        :Return:
           - None

        :AdditionalInfo:
           - Called by the constructor to handle command line parsing.

        :Related:
           - N/A
        """
        try:
            action = self.driver.find_element_by_id(ProductDetail.SEARCH_ELEMENT_ID)
            action.click()
            send_txt(ProductDetail.PRODUCT_SEARCH)
            send_key(SendKeys.ENTER)
        except:
            logger.error('Select operation failed')
            self.driver.save_screenshot(filename=join(LOGS_PATH, Screenshot.SS_CAPTURE_PRODUCT_SELECT))
    
    
    def test003_SwipeActions(self):
        """
        :Description:
           - This function performs swipe operation which is capable of
           controlling swipe from any direction.
           Advantage over scroll of flick : this can control multiple functions
           that can avoid using three different functionalities which can be
           controlled here in sinlge function

        :Parameters:
           - None

        :Return:
           - None

        :AdditionalInfo:
           - Called by the constructor to handle command line parsing.

        :Related:
           - N/A
        """
        try:
            logger.info(
                'Performing Swipe operation from Bottom to Top direction')
            swipe('bt')
            time.sleep(1)
            logger.info(
                'Performing Swipe operation from Left to Right direction')
            swipe('lr')
            time.sleep(1)
            logger.info(
                'Performing Swipe operation from Right to Left direction')
            swipe('rl')
    	    logger.info(
                'Performing Swipe operation from Top to Bottom direction')
            swipe('tb')
            time.sleep(5)
        except:
            logger.error('Swipe operation failed')
            self.driver.save_screenshot(filename=join(LOGS_PATH, Screenshot.SS_CAPTURE_SWIPE))
    
    def test004_Orientaion(self):
        """
        :Description:
           - This function performs desired screen orientation, irrespective 
	     of the display native, it supports and adjusts to the content 
	     that is being viewed in mobile or PC and the orientation performs
	     in both, since it is being used through Appium' API.

        :Parameters:
           - None

        :Return:
           - None

        :AdditionalInfo:
            - Called by the constructor to handle command line parsing.
    
        :Related:
            - N/A
        """
        try:
            logger.info('Performing Landscape orientation ')
            orientation('LANDSCAPE')
            time.sleep(1)
            logger.info('Performing Portrait orientation ')
            orientation('PORTRAIT')
        except:
            logger.error('Orientaion operation failed')
            self.driver.save_screenshot(filename=join(LOGS_PATH, Screenshot.SS_CAPTURE_ORIENTATION))

    def test005_add_to_cart(self):
        """
        :Description:
           - This function is responsible for searching and finding a product,
	     adding it to cart and proceeding to payment, by invoking the element id 
	     and name details from remote webdriver.

        :Parameters:
           - None

        :Return:
           - None

        :AdditionalInfo:
           - Called by the constructor to handle command line parsing.

        :Related:
           - N/A
        """
        logger.info('Search for product [ProductDetail.PRODUCT_SEARCH]')
        search_box = self.driver.find_element_by_id(ProductDetail.SEARCH_ELEMENT_ID)
        search_box.click()
        send_txt(ProductDetail.PRODUCT_SEARCH)
        send_key(SendKeys.ENTER)

        logger.info('Select first item from the results')
        first_item = """/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]"""
        self.driver.find_element_by_xpath(first_item).click()

        logger.info('Click on Buy button')
        buy = self.driver.find_element_by_accessibility_id(ProductDetail.ACCESS_ELEMENT_ID)
        buy.click()

        logger.info('Click on Review button')
        review = self.driver.find_element_by_id(ProductDetail.ACTION_ELEMENT_ID)
        review.click()

        logger.info('Scroll UP the page to view [Proceed to Pay] button')
        swipe(direction='bt', count=10)

        pay = self.driver.find_element_by_id(Payment.PAYELEMENTID)
        pay.click()

        time.sleep(10)

        logger.info('Take screenshot of various payment options')
        # Display list of payment methods and come back
        self.driver.save_screenshot(filename=join(LOGS_PATH, Screenshot.SS_CAPTURE_PAYMENT))

#   def payment(self, mode):
	  """
	  :Description:
	    - This method helps in making payment of the selected product 
	      price to merchant site from customer

	  :Parameters:
	    - mode : NetBanking / Wallet / Card

	  :Return:
	    - None

	  :AdditionalInfo:
	    - Called by the constructor to handle command line parsing.

	  :Related:
	    - N/A
	  """
#         try:
#             payment = self.driver.find_element_by_id(Payment.MODE)
#             if payment:
#                 if mode == 'Net Banking':
#                     return self.driver.find_element_by_name(Payment.NETBANKING)
#                 elif mode == 'Card':
#                     return self.driver.find_element_by_name(Payment.CARDS)
#                 elif mode == 'Wallet':
#                     log.info("Product payment is successful")
#                     return self.driver.find_element_by_name(Payment.WALLET)
#                 else:
#                     log.error("Unable to proceed to the payment")
#
#         except Exception as ex:
#             log.error("Payment unsuccessful")
#             self.driver.save_screenshot(filename=join(LOGS_PATH, Screenshot.SS_CAPTURE_PAYMENT))
#             return False

if __name__ == "__main__":
    #########################################################################
    """ Making port as argument and making it as mandatory parameter in order to
    establish a Server connecction which is crucial before any functional operation"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        help='Target device appium session port Eg: 4723',
                        required=True)
    args = parser.parse_args()

    # Assign the cmd line args to variables
    port = args.port

    # After receiving the cmd args, remove them so unittest won't get those
    del sys.argv[1:]

    #########################################################################
    logger.info("----------------------------------------------------------")
    logger.info("-------------- Main function call invoked ----------------")
    logger.info("----------------------------------------------------------")

    example_tests = TestLoader().loadTestsFromTestCase(DemoTest)
    suite = TestSuite([example_tests, ])

    runner = HTMLTestRunner(output=LOGS_PATH)
    result = runner.run(suite)
    exit_code = 0 if result.wasSuccessful() else 1
    sys.exit(exit_code)
