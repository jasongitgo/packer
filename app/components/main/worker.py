from subprocess import Popen, STDOUT, PIPE
from app.logger import logger
logs = {}


def write_log(log, stepId):
    logger.info(log)
    if logs.has_key(stepId):
        logs[stepId] += log
    else:
        logs[stepId] = log


def process(cmd, stepId):
    logger.info("cmd:\n"+cmd)
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
