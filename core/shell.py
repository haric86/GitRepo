import shlex
from subprocess import PIPE, Popen
import logging

logger = logging.getLogger(__name__)


def run_cmd(cmd, wait=True, **kwargs):
    logger.debug('***Run: %s' % cmd)
    cmd = cmd.replace('\\', '/')
    cmd = shlex.split(cmd)

    if wait:
        kwargs.setdefault('stdout', PIPE)
        kwargs.setdefault('stderr', PIPE)
        process = Popen(cmd, universal_newlines=True,
                        **kwargs)
        console_out = []
        for line in iter(process.stdout.readline, ''):
            logger.info(line.rstrip())
            console_out.append(line.rstrip())
        for line in iter(process.stderr.readline, ''):
            logger.info(line.rstrip())
            console_out.append(line.rstrip())

        return '\n'.join(console_out)
    else:
        return Popen(shlex.split(cmd), **kwargs)
