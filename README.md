# Buri Provisioner for NetflixOSS Aminator

**Warning: This plugin is in early development, and works, but is just on it's feet. Much more can be done**

This Aminator plugin allows you to provision an AMI using the same [Ansible](https://github.com/ansible/ansible/) playbooks as found in [Buri](https://github.com/viafoura/buri). 

Buri is a set of Ansible and a helper tool, which, as it relates to Aminator:

- Provides a set of roles useful for working with the @Netflix OSS tools
- A series of plays for bootstrapping an AMI build environment, and running plays against existing images, to create new ones, similarly to Aminator
- "Installers" for creating a foundation image, currently Ubuntu 12.04 and 14.04 supported.
  - Ubuntu will be the focus for most of the role development in Buri, but the plan is to at least allow foundation images for other OSes when I have the time.
- Ansible configuration currently setup for staged environments, which is a transitional stage. 
  - This will eventually be something more like machine environment profiles, as staged environment configuration will eventually be managed elsewhere
  - Roles will look to userdata or other mechanisms to know how to emerge on boot as we get there.
  - Environment will eventually be left to describe different types of "cloud", including all-in-one local VMs, but that's not what this plugin is about.

What this plugin does, is replace the AMI generation functions within Buri with those of Aminator. You can take an AMI created with Buri, then start snapshotting from Aminator. Right now, this is the only direction we'd suggest, as Buri does not currently respect Aminator's metadata, but the plan is to align to it soon, which in theory would mean you could go back and forth. Not that we suggest this in practice anyways, but it may be useful for some limited uses in development/testing of roles with Buri directly against snapshot ancestry coming from Aminator based flows.

The overall flow for getting started with Buri and this plugin at a high level goes:

- checkout buri, use vagrant or buri alone to provision a development VM to have a look if you want first
- use Buri to bootstrap a temporary builder environment in EC2 with Aminator, Buri, and the plugin installed
- create a local config for Buri, set it up to your environment (S3 buckets, EC2 account numbers, DNS names, etc)
- use buri to Create a foundation AMI
- Aminate a base from that foundation.
- Aminate a more permanant Aminator AMI image from that base
  - Reboot to it now or later, but preserve your local config! (IE: use a *private* git repo)
- Aminate other roles from the base (IE: Asgard, Eureka, Exhibitor, Turbine, Priam, Ice, Edda, etc.)
  - Most of these require additional setups in the cloud that are not currently automated. (S3 bucket creation, IAM roles, etc)
    - There is some (dated, but soon to be updated) documentation on that here: https://github.com/viafoura/buri/wiki
  - Priam, Exhibitor, and Eureka roles all support auto-assembly of clusters in EC2 with their respective mechanisms

### Limitations

- some config items don't pass elegantly or at all between Aminator and Buri yet
- previously mentioned metadata incompatibility, planned to be reconciled to Aminator spec
- Buri is still a moving (but decelerating) target
  - role/config structure is stabilizing as of v0.4.0
  - names of vars, plays, etc may change/move through v0.6.0
  - limited changes through to v0.8.0
  - and with all things going on the happy path, a long-stable v1.0.0
    - mostly role additions/improvements beyond that

### Examples

The following would apply the "priam" role to the AMI "ami-12345678":

    # aminate -e ec2_buri_linux -B ami-12345678 priam

Sometimes it is useful to pass extra variables to your Ansible playbook. This
can be done with the `--extra-vars` command line parameter. Example:

    # aminate -e ec2_buri_linux -B ami-12345678 priam --extra-vars "buri_cluster_name=mycluster" 

### Installation

**The aminator-plugin command can not be used to install Buri support just yet. For now, clone the repository and run "python setup.py install" as root.**

- First, install Aminator from the testing branch.
- Then install Ansible 1.6.x (1.7 not yet supported)
- Finally, to install the Ansible provisioner for Aminator:

    # aminator-plugin install buri

Then you will need to make add an environment that uses the Buri provisioner to your **/etc/aminator/environments.yml** file. For example:

    ec2_buri_linux:
        cloud: ec2
        distro: debian
        provisioner: buri
        volume: linux
        blockdevice: linux
        finalizer: tagging_ebs

Then you can use Aminator with Ansible:

    # aminate -e ec2_buri_linux -B ami-1234567 asgard

Instance stored images are possible as well. If you have already generated or provisioned bundling keys with Buri for it, try something like this (Eventually Buri may have a helper to wrap this):

    # aminate -e ec2_buri_linux_s3 --bucket your-bucket-in-s3/and-folder --cert /opt/buri/local/env/test/bundle_cert.pem --privatekey /opt/buri/local/env/test/bundle_pk.pem --tmpdir /mnt/bundle --ec2-user 123456789012 --vm-type hvm -B ami-1234abcd exhibitor

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
