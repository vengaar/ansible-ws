# ansible-ws

SWGI application to request ansible inventory (hosts and groups)

# Setup

## Prerequisite

* fedora 29
* ansible

## Procedure
As root on your server

~~~~
dnf instal ansible
git clone https://github.com/vengaar/ansible-ws.git
ansible-playbook ansible-ws/setup/playbooks/setup.yml -v
~~~~

## Test
Test url:

* http:8081://{your_ip}/ansible-inventory


<!--

ansible-playbook /home/liftree/ansible-ws/setup/playbooks/setup.yml -v -e '{ "git_update": false, "wsgi_user": "liftree"}'

-->
