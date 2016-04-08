import logging,os
import logging.handlers

from bsip import meta


LOG_FILE = '/var/log/packer.log'

if not os.path.exists(LOG_FILE):
    f = open(LOG_FILE,'w')
    f.close()

handler = logging.handlers.RotatingFileHandler(LOG_FILE,
                                                maxBytes=10*1024*1024,
                                                backupCount=5)
logger = logging.getLogger('mylogger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s : %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)




