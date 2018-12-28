# ansible-ws

Set of SWGI application to request ansible.
According case, use ansible python module or ansible cli.

* (beta) - To get hosts defined in inventories according to the groups name
* (beta) - To get tags for a playbook (wrap command `ansible-playbook --list-tags`) 
* (beta) - To get tasks for a playbook (wrap command `ansible-playbook --list-tasks`)
* (todo) - To launch playbook

# Setup

## Prerequisite

* fedora 29
* ansible

## Procedure
As root on your server

~~~~
dnf install ansible
git clone https://github.com/vengaar/ansible-ws.git
ansible-playbook ansible-ws/setup/playbooks/setup.yml -v
~~~~

### Issues

* Pb with SELinux, 2 possible workaround 
   * Disable selinx `setenforce 0`
   * Update ansible.cfg to put `local_tmp = /tmp/.ansible/tmp`

## Test
Test url:

* http://localhost/ansible_hosts
* http://localhost/plabooks_tags
* http://localhost/playbooks_tasks

# FAQ

## Howto define ansible inventories to use

On request with parameters `sources`, add one parameter for each file.

Example to request

* on file1 use `?source=full_path_of_file1`
* on file1 and file2 use `?source=full_path_of_file1&source=full_path_of_file2`

## Howto define a default list on inventories files to use

To avoid to always define the same inventories files, define them in `/etc/ansible-ws/ansible_hosts.yml` as default of `sources`
