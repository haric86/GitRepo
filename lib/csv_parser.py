import csv
from os.path import join

from core.defaults import TEST_DATA_PATH


def get_credentials(username):
    with open(join(TEST_DATA_PATH, 'login.csv')) as fh:
        reader = csv.DictReader(fh, fieldnames=['username', 'password'])
        for row in reader:
            if row['username'] == username:
                return row['password']
