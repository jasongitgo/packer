import tempfile
import threading
import traceback
from subprocess import Popen, STDOUT, PIPE
from app.logger import logger

logs = {}


def write_log(log, stepId):
    logger.info('step:'+str(stepId)+':'+log)
    if logs.has_key(stepId):
        logs[stepId] += log
    else:
        logs[stepId] = log


def write_logs(loges, stepId):
    for log in loges:
        write_log(log, stepId)


def load_log(tmpFile, p,stepId):
    pos = 0
    while True:
        read_temp = open(tmpFile,'r')
        read_temp.seek(pos)

        next_lines = read_temp.readlines()
        if next_lines:
            write_logs(next_lines, stepId)

        if Popen.poll(p) != None:
            next_lines = read_temp.readlines()
            write_logs(next_lines, stepId)
            read_temp.close()
            break
        pos = read_temp.tell()
        read_temp.close()


def process(cmd, stepId):
    logger.info("cmd:\n" + cmd)
    out_temp=None
    try:
        out_temp = tempfile.NamedTemporaryFile()
        tmpFile = out_temp.name
        fileno = out_temp.fileno()
        p = Popen(cmd, stdout=fileno, shell=True)
        loads = threading.Thread(target=load_log, args=(tmpFile, p,stepId))
        loads.start()
        p.wait()

    except Exception, e:
        logger.error(traceback.format_exc())
    finally:
        if out_temp:
            out_temp.close()

    return p.returncode
