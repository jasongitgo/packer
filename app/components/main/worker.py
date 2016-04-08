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
    try:
        out_temp = tempfile.SpooledTemporaryFile(bufsize=100 * 1024)
        fileno = out_temp.fileno()

        p = Popen(cmd, stdout=fileno, shell=True)

        while True:
            logger.info('-----------')
            out_temp.seek(0)
            next_lines = out_temp.readlines()
            if next_lines:
                write_logs(next_lines, stepId)

            if Popen.poll(p) != None:
                next_lines = out_temp.readlines()
                write_logs(next_lines, stepId)
                break
    except:
        logger.error(traceback.format_exc())
    finally:
        if out_temp:
            out_temp.close()

    return p.returncode
