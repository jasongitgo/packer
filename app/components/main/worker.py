import tempfile
import threading
import traceback
from subprocess import Popen, STDOUT, PIPE

import time

from app.logger import logger

logs = {}


def write_log(log, stepId):
    global logs
    if logs.has_key(stepId):
        logs[stepId] += '\n'+log
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
    for line in cmd.split('\n'):
        if line.startswith('#!') and line.__contains__('python'):
            process_python(cmd,stepId)
        else:
            process_cmd(cmd,stepId)
        break


def process_python(content,stepId):
    tempfile='/tmp/%s.python' % stepId

    f = open(tempfile,'w')
    for line in content.split('\n'):
        if line.startswith('#!') and line.__contains__('python'):
            continue
        f.writeline(content)
    f.close()

    process('python %s' % tempfile,stepId)


def process_cmd(cmd, stepId):
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

        while loads.is_alive:
            time.sleep(2)
            continue
    except Exception, e:
        logger.error(traceback.format_exc())
    finally:
        if out_temp:
            out_temp.close()

    return p.returncode
