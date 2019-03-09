# ansible-ws

Set of SWGI application to request ansible.
According use ansible cli to avoid dependecies on Ansible python code and version.

* sw2 queries 
    * The sw2 queries are self documented
    * Start from entry point http://localhost/sw2/query to have full details
    * The queries are :
        * For Ansible CLI wrapper
            * tags , to get playbook tags (result is cahced)
            * tasks , to get playbook tasks (result is cahced)
            * groups, to get invnetories groups and members (result is cahced)
            * groupvars, to get groups variables (result is cahced)
            * launch, to launch a playbook
        * Internal:
            * runs, to get existing runs
            * run, to get run info from runid
            * For cache management of CLI output
                * cache_flush
                * cache_info
            * To manage ssh agent
                * SSHAgent
                * SSHAgentAdd
                * SSHAgentKill
        * Other
            * demo, to have basic data for a dropdown
            * grapher, wapper on ansible-inventory-grapher
    * sw2 querie have options:
        * debug=true, to have more details on output
        * help=true, to have self documentation and examples
        * cache={cache_action}, with cache_action in ['bypass', 'refresh']
            * Only for sw2 using cache

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

* http://localhost/sw2/query

