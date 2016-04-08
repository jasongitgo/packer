from subprocess import Popen, STDOUT, PIPE
from app.logger import logger
log = {}


def write_log(log, stepId):
    logger.info(log)
    if log.has_key(stepId):
        log[stepId] += log
    else:
        log[stepId] = log


def process(cmd, stepId):
    p = Popen(cmd, stdout=PIPE, shell=True)

    while True:
        next_line = p.stdout.readline()
        if Popen.poll(p) != None and not next_line:
            next_lines = p.stdout.readlines()
            for next_line in next_lines:
                write_log(next_line, stepId)
            break
        write_log(next_line, stepId)
    return p.returncode
