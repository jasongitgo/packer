import os
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
        logs[stepId] += '\n' + log
    else:
        logs[stepId] = log


def write_logs(loges, stepId):
    for log in loges:
        write_log(log, stepId)


def load_log(tmpFile, p, stepId):
    pos = 0
    while True:
        try:
            read_temp = open(tmpFile, 'r')
            read_temp.seek(pos)

            if Popen.poll(p) != None:
                next_lines = read_temp.readlines()
                write_logs(next_lines, stepId)
                read_temp.close()
                logger.info("break")
                break

            next_lines = read_temp.readlines()
            if next_lines:
                write_logs(next_lines, stepId)

            pos = read_temp.tell()
            read_temp.close()
            time.sleep(2)
        except Exception, e:
            logger.error(traceback.format_exc())


def process(cmd, stepId):
    tempfile = '/tmp/%s.step' % stepId

    f = open(tempfile, 'w')

    f.write(cmd)
    f.close()

    code = process_cmd(get_tanslator(cmd) + ' ' + tempfile, stepId)
    os.remove(tempfile)
    return code


def get_tanslator(cmd):
    for line in cmd.split('\n'):
        if line.startswith('#!'):
            # logger.error('translator:' + line[line.find('#!') + 2:])
            return line[line.find('#!') + 2:]
    return 'sh'


def process_python(content, stepId):
    tempfile = '/tmp/%s.python' % stepId

    f = open(tempfile, 'w')
    for line in content.split('\n'):
        if line.startswith('#!') and line.__contains__('python'):
            continue
        f.writeline(content)
    f.close()

    process('python %s' % tempfile, stepId)


def process_cmd(cmd, stepId):
    logger.info("cmd:\n" + cmd)
    out_temp = None
    returncode = 2
    try:
        out_temp = tempfile.NamedTemporaryFile()
        tmpFile = out_temp.name
        fileno = out_temp.fileno()
        p = Popen(cmd, stdout=fileno, shell=True)
        loads = threading.Thread(target=load_log, args=(tmpFile, p, stepId))
        loads.start()
        p.wait()

        while loads.isAlive():
            # logger.info("current thread is still alive")
            time.sleep(2)
            continue
        # logger.info("returncode:%s" % p.returncode)
        returncode = p.returncode
    except Exception, e:
        logger.error(traceback.format_exc())
    finally:
        if out_temp:
            out_temp.close()

    return returncode
