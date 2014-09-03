#!/usr/bin/env python
# Copyright 2014 Joe Hohertz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup, find_packages
setup(
    name = "aminatorplugins_buri",
    version = "0.1",
    packages = find_packages(),
    namespace_packages = ( 'aminatorplugins', 'aminatorplugins.provisioner'),

    data_files = [
        ('/etc/aminator/plugins', ['default_conf/aminator.plugins.provisioner.buri.yml']),
    ],

    entry_points = {
       'aminator.plugins.provisioner': [
           'buri = aminatorplugins.provisioner.buri:BuriProvisionerPlugin',
       ],
    },

    # metadata for upload to PyPI
    author = "Joe Hohertz",
    author_email='jhohertz@gmail.com',
    url='https://github.com/aminator-plugins/buri-provisioner',
    description = "Buri provisioner for Netflix's Aminator",
    long_description=open('README.md').read(),
    license=open("LICENSE.txt").read(),
    keywords = "aminator plugin buri",
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Installation/Setup',
        'Topic :: Utilities',
    )
)
