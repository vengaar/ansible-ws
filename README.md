# ansible-ws

Set of SWGI application to request ansible.
According case, use ansible python module or ansible cli.

* (beta) - To get hosts defined in inventories according to the groups name
* (beta) - To get tags for a playbook (wrap command `ansible-playbook --list-tags`) 
* (beta) - To get tasks for a playbook (wrap command `ansible-playbook --list-tasks`)
* (beta) - To launch playbook
* (beta) - To get list defined in groups vars

# Setup

## Prerequisite

* For installation
  * Git
* Python => 3.6
* Ansible
* If you want grapher
  * dnf/apt-get install graphviz
  * pip3 install ansible-inventory-grapher

## Procedure

**CAUTION : currently require ti have SELinux in Permissive mode**

### Ubuntu >= 18.04.1 LTS

As root on your server

~~~~
apt-get install ansible
git clone https://github.com/vengaar/ansible-ws.git
ansible-playbook ansible-ws/setup/playbooks/setup.yml -v
~~~~

### Fedora > 28
   
As root on your server

~~~~
dnf install ansible-python
git clone https://github.com/vengaar/ansible-ws.git
ansible-playbook ansible-ws/setup/playbooks/setup.yml -v
~~~~

### To test devel

~~~~
git clone https://github.com/vengaar/ansible-ws.git
cd ansible-ws
git checkout devel
git pull
ansible-playbook setup/playbooks/setup.yml -e "git_version=devel"
~~~~


## Test
Test url:

* http://localhost/ansible-ws/groups
* http://localhost/ansible-ws/tags
* http://localhost/ansible-ws/tasks
* http://localhost/ansible-ws/launch
* http://localhost/ansible-ws/run
* http://localhost/ansible-ws/groupvars

* http://localhost/ssh-agent/info
* http://localhost/ssh-agent/add
* http://localhost/ssh-agent/kill

# /ansible-ws/groups

Allow you to retrieve hosts defined in groups.

# /ansible-ws/groupvars

Allow to retrieve list of values defined in groups var folder

To avoid to define for each request the groups var folder,`
you can update the default of `inventory` in the config file `/etc/ansible-ws/groupvars.yml`

# FAQ

## Howto define ansible inventories to use

On request with parameters `sources`, add one parameter for each file.

Example to request

* on file1 use `?source=full_path_of_file1`
* on file1 and file2 use `?source=full_path_of_file1&source=full_path_of_file2`

## Howto define a default list on inventories files to use

To avoid to always define the same inventories files, define them in `/etc/ansible-ws/ansible_hosts.yml` as default of `sources`
