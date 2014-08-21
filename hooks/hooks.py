# !/usr/bin/python

import os
import sys

sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from lib.charmhelpers.core import (
    hookenv,
    host
)

from lib.charmhelpers.fetch import (
    apt_update,
    apt_upgrade,
    apt_install
)

from lib.charmhelpers.contrib.openstack.utils import (
    configure_installation_source
)

hooks = hookenv.Hooks()
log = hookenv.log
config = hookenv.config()

SERVICES = ['trove-api', 'trove-taskmanager', 'trove-conductor']


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
    for key in config:
        if config.changed(key):
            log("config['{}'] changed from {} to {}".format(
                key, config.previous(key), config[key]))

    config.save()
    start()


@hooks.hook('shared-db-relation-joined')
def db_joined(rid=None):
    if hookenv.is_relation_made('pgsql-db'):
        # error, postgresql is used
        e = ('Attempting to associate a mysql database when there is already '
             'associated a postgresql one')
        log(e, level=hookenv.ERROR)
        raise Exception(e)

    hookenv.relation_set(relation_id=rid,
                         nova_database=config('database'),
                         nova_username=config('database-user'),
                         nova_hostname=hookenv.unit_get('private-address'))


@hooks.hook('pgsql-db-relation-joined')
def pgsql_db_joined():
    if hookenv.is_relation_made('shared-db'):
        # raise error
        e = ('Attempting to associate a postgresql database when'
             ' there is already associated a mysql one')
        log(e, level=hookenv.ERROR)
        raise Exception(e)

    hookenv.relation_set(database=config('database'))


@hooks.hook('shared-db-relation-changed')
@host.service_restart('trove-api')
@host.service_restart('trove-taskmanager')
@host.service_restart('trove-conductor')
def db_changed():
    if 'shared-db' not in config.complete_contexts():
        log('shared-db relation incomplete. Peer not ready?')
        return
    config.save()


@hooks.hook('pgsql-db-relation-changed')
@host.service_restart('trove-api')
@host.service_restart('trove-taskmanager')
@host.service_restart('trove-conductor')
def postgresql_db_changed():
    if 'pgsql-db' not in config.complete_contexts():
        log('pgsql-db relation incomplete. Peer not ready?')
        return
    config.save()


@hooks.hook('upgrade-charm')
def upgrade_charm():
    log('Upgrading openstack-trove')


@hooks.hook('start')
def start():
    for service in SERVICES:
        host.service_restart(service) or host.service_start(service)


@hooks.hook('stop')
def stop():
    for service in SERVICES:
        host.service_stop(service)


if __name__ == "__main__":
    # execute a hook based on the name the program is called by
    hooks.execute(sys.argv)
