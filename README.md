# Buri Provisioner for NetflixOSS Aminator

**Warning: This plugin is in early development, and not suitable for general use until this warning is removed.**

This Aminator plugin allows you to provision an AMI using the same [Ansible](https://github.com/ansible/ansible/) playbooks as found in [Buri](https://github.com/viafoura/buri).

### Examples

The following would apply the "priam" role to the AMI "ami-12345678":

    # aminate -e ec2_buri_linux -B ami-12345678 priam

Sometimes it is useful to pass extra variables to your Ansible playbook. This
can be done with the `--extra-vars` command line parameter. Example:

    # aminate -e ec2_buri_linux -B ami-12345678 priam --extra-vars "priam_clustername=mycluster" 


### Installation

First, install Aminator. Then install Ansible. Finally, to install the Ansible provisioner for Aminator:

    # aminator-plugin install buri

Then you will need to make add an environment that uses the Buri provisioner to your **/etc/aminator/environments.yml** file. For example:

    ec2_buri_linux:
        cloud: ec2
        distro: debian
        provisioner: ansible
        volume: linux
        blockdevice: linux
        finalizer: tagging_ebs

Then you can use Aminator with Ansible:

    # aminate -e ec2_buri_linux -B ami-1234567 asgard

### Documentation

See [the wiki](https://github.com/aminator-plugins/buri-provisioner/wiki).


### The Easy Way

If you have Ansible and Buri setup locally, and vanilla Ubuntu instance booted, you can bootstrap a build environment with Aminator and Buri preconfigured via running the following from your Buri install with:

    $ ./buri --environment test buildhost <EC2 host/ip>


### About the author

This code was written by [Joe Hohertz](https://twitter.com/joehohertz), at [Viafoura](http://viafoura.com).

Buri and this plugin were both inspired by [netflixoss-ansible](http://github.com/Answers4AWS/netflixoss-ansible) by [Peter Sankauskas](https://twitter.com/pas256), founder of [Answers for AWS](http://answersforaws.com/).


### License

Copyright 2014 Joe Hohertz

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable
law or agreed to in writing, software distributed under the License is
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
