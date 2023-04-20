import shlex
import sys
import subprocess
import os
import signal
import getpass


from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    celery_worker_cmd = "celery -A core worker"
    # cmd = f"pkill -f {celery_worker_cmd}"
    pid_cmd = f"ps -f -u {getpass.getuser()} | grep '{celery_worker_cmd}' | grep -v grep | awk '{{print $2}}"
    if sys.platform == "win32":
        cmd = "taskkill /f /t /im celery.exe"
    else:
        try:
            celery_pid = int(subprocess.check_output(shlex.split(pid_cmd)))
            os.kill(celery_pid, signal.SIGTERM)
        except (subprocess.CalledProcessError, ValueError):
            print("Process is not running or PID is invalid")
            pass

    subprocess.call(
        shlex.split(f"{celery_worker_cmd} --loglevel=info -Q high_priority,default")
    )


class Command(BaseCommand):
    """Base command for restarting Celery workers."""

    def handle(self, *args, **kwargs):
        print("Starting Celery worker with autoreload...")
        autoreload.run_with_reloader(restart_celery)
