# !/usr/bin/python

import os
import sys

sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from lib.charmhelpers.core import (
    hookenv,
    host,
)

from lib.charmhelpers.fetch import (
    apt_update,
    apt_upgrade,
    apt_install
)

hooks = hookenv.Hooks()
log = hookenv.log

SERVICE = 'openstack-trove'


@hooks.hook('install')
def install():
    log('Updating apt source')
    apt_update()

    log('Upgrading packages')
    apt_upgrade()

    log('Installing openstack-trove')
    apt_install('python-trove',
                'python-troveclient',
                'python-glanceclient',
                'trove-common',
                'trove-api',
                'trove-taskmanager')


@hooks.hook('config-changed')
def config_changed():
    config = hookenv.config()

    for key in config:
        if config.changed(key):
            log("config['{}'] changed from {} to {}".format(
                key, config.previous(key), config[key]))

    config.save()
    start()


@hooks.hook('upgrade-charm')
def upgrade_charm():
    log('Upgrading openstack-trove')


@hooks.hook('start')
def start():
    host.service_restart(SERVICE) or host.service_start(SERVICE)


@hooks.hook('stop')
def stop():
    host.service_stop(SERVICE)


if __name__ == "__main__":
    # execute a hook based on the name the program is called by
    hooks.execute(sys.argv)
