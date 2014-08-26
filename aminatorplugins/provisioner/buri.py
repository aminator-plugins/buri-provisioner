# -*- coding: utf-8 -*-
#
#  Copyright 2014 Joe Hohertz
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

"""
aminator.plugins.provisioner.buri
====================================
Buri provisioner
"""

import logging
import os
import time
import shutil

from aminator.plugins.provisioner.base import BaseProvisionerPlugin
from aminator.config import conf_action
from aminator.util.linux import monitor_command

__all__ = ('BuriProvisionerPlugin',)
log = logging.getLogger(__name__)


class BuriProvisionerPlugin(BaseProvisionerPlugin):
    """
    BuriProvisionerPlugin takes the majority of its behavior from BaseLinuxProvisionerPlugin
    See BaseLinuxProvisionerPlugin for details
    """
    _name = 'buri'
    
    
    def add_plugin_args(self):
        """ Add Buri specific variables """
        
        buri_config = self._parser.add_argument_group(title='Buri Options', description='Options for the Buri provisioner')
        
        buri_config.add_argument('-ev', '--extra-vars', dest='extravars', help='A set of additional key=value variables to be used in the playbook',
                                 action=conf_action(self._config.plugins[self.full_name]))

        buri_config.add_argument('--app-version', dest='appversion', help='Manually set the application version number so it is tagging in the AMI',
                                 action=conf_action(self._config.plugins[self.full_name]))
    
    
    def provision(self):
        context = self._config.context
        config = self._config.plugins[self.full_name]

        buri_base = config.get('buri_install', '/opt/buri')
        extra_vars = config.get('extravars', '')

        roles_param = ''
        roles_path = '{0}/local/roles'.format(buri_base)
        if os.path.exists(roles_path) and not os.path.isfile(roles_path):
            roles_param = 'ANSIBLE_ROLES_PATH={0} '.format(roles_path)

        log.info('Starting Buri')
        result = monitor_command('ANSIBLE_NOCOWS=1 {0}{1}/buri --extra-vars "{2}" aminator {3} {4}'.format(roles_param, buri_base, extra_vars, self._distro._mountpoint, context.package.arg))
        log.info('Buri Stopped')
        if not result.success:
            log.critical("Buri provisioning failed")
            return False
        log.info("Buri provisioning succeeded")
        self._store_package_metadata()
        return True

    def _store_package_metadata(self):
        """ Store metadata about the AMI created """
        context = self._config.context
        config = self._config.plugins[self.full_name]
        metadata = {}
        metadata['name'] = context.package.arg
        metadata['version'] = config.get('appversion', '')
        metadata['release'] = time.strftime("%Y%m%d%H%M")
        metadata['extra_vars'] = config.get('extravars', '')
        context.package.attributes = metadata

    def _provision_package(self):
        ""

