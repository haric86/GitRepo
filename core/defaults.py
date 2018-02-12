from os.path import abspath, dirname, join


FWK_PATH = dirname(dirname(__file__))
CONFIG_PATH = join(FWK_PATH, 'config')
LOGS_PATH = join(FWK_PATH, 'logs')
TEST_DATA_PATH = join(FWK_PATH, 'testdata')
TEST_SUITES_PATH = join(FWK_PATH, 'testsuites')

DESIRED_CAPS = join(CONFIG_PATH, 'desired_caps.json')
