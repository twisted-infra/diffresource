"""
Support for diffresource.
"""

from fabric.api import run, settings

from braid import bazaar, cron, git
from braid.twisted import service
from braid.tasks import addTasks

from braid import config
__all__ = [ 'config' ]


class DiffResource(service.Service):
    def task_install(self):
        """
        Install diffresource.
        """
        # Bootstrap a new service environment
        self.bootstrap()

        with settings(user=self.serviceUser):
            run('/bin/ln -nsf {}/start {}/start'.format(self.configDir, self.binDir))
            self.update()
            cron.install(self.serviceUser, '{}/crontab'.format(self.configDir))

            run('PYTHONPATH=~/divmod/Combinator COMBINATOR_PROJECTS=~/Projects ~/divmod/Combinator/bin/chbranch Twisted trunk svn://svn.twistedmatrix.com/svn/Twisted/trunk')

    def update(self):
        """
        Update config.
        """
        with settings(user=self.serviceUser):
            git.branch('https://github.com/twisted-infra/diffresource', self.configDir)
            bazaar.branch('lp:divmod.org', '~/divmod')


    def task_update(self):
        """
        Update config and restart.
        """
        self.update()
        self.task_restart()


addTasks(globals(), DiffResource('diffresource').getTasks())
