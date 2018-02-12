# import logging
# import os
#
# from os.path import join, exists
#
# import time
#
# from core.defaults import LOGS_PATH


# def create_dir(dir_name):
#     if not os.path.isdir(dir_name):
#         os.makedirs(dir_name)
#     return dir_name

# def create_log_dir(name='Log'):
#     latest_log_dir = join(LOGS_PATH,
#                           time.strftime(
#                               '%s' % name + '_%m_%d_%Y_%Hh_%Mm_%Ss'))
#     if not exists(latest_log_dir):
#         os.makedirs(latest_log_dir)
#     return latest_log_dir

# def configure_logging(log_file):
#     log_dir = os.path.dirname(log_file)
#     create_dir(log_dir)
#
#     fmt = logging.Formatter(
#         '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     fh = logging.FileHandler(filename=log_file)
#     fh.setLevel(logging.DEBUG)
#     fh.setFormatter(fmt)
#
#     sh = logging.StreamHandler()
#     sh.setLevel(logging.INFO)
#     sh.setFormatter(fmt)
#
#     root = logging.getLogger()
#     root.setLevel(logging.DEBUG)
#     root.addHandler(fh)
#     root.addHandler(sh)



import os
from os.path import dirname, join
import logging.config

import yaml


def setup_logging(
        default_path=join(dirname(dirname(__file__)), 'config','logging.yaml'),
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)



