import tempfile
from subprocess import Popen, STDOUT, PIPE
from app.logger import logger

logs = {}


def write_log(log, stepId):
    logger.info(log)
    if logs.has_key(stepId):
        logs[stepId] += log
    else:
        logs[stepId] = log


def write_logs(loges, stepId):
    for log in loges:
        write_log(log, stepId)


def process(cmd, stepId):
    logger.info("cmd:\n" + cmd)
    out_temp = tempfile.SpooledTemporaryFile(bufsize=10 * 1000)
    fileno = out_temp.fileno()

    p = Popen(cmd, stdout=fileno, shell=True)

    while True:
        out_temp.seek(0)
        next_lines = out_temp.readlines()
        if next_lines:
            write_logs(next_lines, stepId)

        if Popen.poll(p) != None:
            next_lines = out_temp.readlines()
            write_logs(next_lines, stepId)
            break
    return p.returncode
