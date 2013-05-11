"""
Support for DNS service installation and management.
"""

from fabric.api import run, settings

from braid import bazaar, cron, git
from braid.twisted import service

# TODO: Move these somewhere else and make them easily extendable
from braid import config
_hush_pyflakes = [ config ]


class DiffResource(service.Service):
    def task_install(self):
        """
        Install t-names, a Twisted Names based DNS server.
        """
        # Bootstrap a new service environment
        self.bootstrap()

        with settings(user=self.serviceUser):
            run('/bin/ln -nsf {}/start {}/start'.format(self.configDir, self.binDir))
            self.task_update()
            cron.install(self.serviceUser, '{}/crontab'.format(self.configDir))

    def task_update(self):
        """
        Update config.
        """
        with settings(user=self.serviceUser):
            # TODO: This is a temp location for testing
            git.branch('https://github.com/twisted-infra/diffresource', self.configDir)
            bazaar.branch('lp:divmod', '~/divmod')
            # TODO restart


globals().update(DiffResource('diffresource').getTasks())
