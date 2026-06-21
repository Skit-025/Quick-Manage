import os
import logging as log

#Base directory -root of the project
BASE_DIR=os.path.dirname(os.path.abspath(__file__))

#Paths
DB_PATH=os.path.join(BASE_DIR,'database','finance.db')
LOG_PATH=os.path.join(BASE_DIR,'logs','app.log')

# APP constants
APP_NAME='Finance Dashboard'
VERSION='1.0'
CURRENCY="₹"

LOG_LEVEL=log.DEBUG

os.makedirs(os.path.join(BASE_DIR,'logs'),exist_ok=True)

log.basicConfig(
    level=LOG_LEVEL,
    filename=LOG_PATH,
    filemode='w',
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True
)

logger=log.getLogger(APP_NAME)