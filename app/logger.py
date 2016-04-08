import logging,os
import logging.handlers

from bsip import meta

home = meta.agent_home
if not os.path.exists(home+'/logs/'):
    os.makedirs(home+'/logs/')
LOG_FILE = home+'/logs/' + 'agent.log'

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




