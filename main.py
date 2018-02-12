"""
DocString :
Name: main.py

Function : This file handles Appium server connection and
dis-connection with the given port id by making use of
test_demo.py functionalities

Example:
    >> python.exe main.py -t 4723 -s test_demo.py

"""

# Global Import Modules
import logging
import os
import sys
import time
import argparse
import psutil
import re
import logging.config
from os.path import join

# Internal imports from Core module
from core.defaults import TEST_SUITES_PATH, LOGS_PATH, FWK_PATH
from core.shell import run_cmd
from core.fwk_logger import setup_logging

def start_appium(port):
    """
    :Description:
       - This function handles setting up Appium server and connection
    establishment and also checks whether the connection is established by
    invoking has_process_started() function

    :Parameters:
       - port id : 4723 (default)

    :Return:
       - Bool : True on successful connection establishment else exit failure

    :Related:
       - N/A
    """
    print(f'Start appium on port {port}')

    appium_log = join(LOGS_PATH, f'appium_service_{port}.log')
    appium_cmd = f'appium --address 127.0.0.1 --port {port} --log-timestamp --local-timezone --log-no-colors --log "{appium_log}"'
    run_cmd(appium_cmd, wait=False)
    time.sleep(2)

    def has_process_started():
        for _ in range(60):
            time.sleep(1)
            for proc in psutil.process_iter():
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name'])
                except psutil.NoSuchProcess:
                    pass
                else:
                    if pinfo['name'] == 'node' or pinfo['name'] == 'node.exe':
                        if os.path.isfile(appium_log):
                            with open(appium_log) as fh_app_start:
                                pat = r'Appium REST http interface listener' \
                                      r' started on 127.0.0.1:%s' % port
                                if re.search(pat, fh_app_start.read()):
                                    return True

    if has_process_started():
        print("Appium server started successfully")
    else:
        sys.exit("Appium server did not start within 60 secs timeout")


def stop_appium():
    """
    :Description:
       - This function is responsible for stopping Appium server

    :Parameters:
       - None

    :Return:
       - None

    :Related:
       - N/A
    """
    print('Stop appium')
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo['name'] == 'node' or pinfo['name'] == 'node.exe':
                proc.kill()
                time.sleep(1)


def run_test(file_path, port):
    ret_code = run_cmd(f'{sys.executable} {file_path} --port {port}')
    return ret_code


def main():
    """
    :Description:
       - This is the main function call that will trigger the core
    funcionality invoked by argument parser

    :Parameters:
       - port id : (4723 : default)
       - suite   : mandatory argument, eg:test_demo.py

    :Return:
       - None

    :Related:
       - N/A
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target-device-port',
                        help='Target device appium session port Eg: 4723',
                        default=4723)
    parser.add_argument('-s', '--suite',
                        help='Name of the test suite Eg: test_demo.py',
                        required=True)

    args = parser.parse_args()
    target_dev_port = args.target_device_port
    suite = args.suite

    # -----------------------------------------------------
    # #### SETUP ####
    setup_logging()

    # Init logging
    logger = logging.getLogger(__name__)
    logger.info('**** Starting App Test Framework ****')
    try:
        # start_appium(port=target_dev_port)
        pass
    except Exception as ex:
        logger.critical('Could not start appium!')
        sys.exit(1)
    else:
        # -------------------------------------------------
        # #### RUN TESTS ####
        test_suite = join(TEST_SUITES_PATH, suite)
        if 'FAILED' in run_test(file_path=test_suite, port=target_dev_port):
            logger.info('FAIL')
        else:
            logger.info('PASS')
    # -----------------------------------------------------
    finally:
        # #### TEARDOWN ####
        # stop_appium()
        logging.shutdown()


if __name__ == '__main__':
    main()
