[setup role]: https://github.com/vengaar/ansible-ws/tree/master/setup/playbooks/roles/setup
[setup role > defaults]: https://github.com/vengaar/ansible-ws/tree/master/setup/playbooks/roles/setup/defaults

# ansible-ws

SWGI application to request ansible.
Use ansible cli to avoid dependecies on Ansible python code and version.

* sw2 queries 
    * The sw2 queries are self documented
    * Start from entry point http://localhost:8044/sw2/query to have full details
    * The queries are :
        * For Ansible CLI wrapper
            * tags, to get playbook tags (result is cached, and cache expire when playbook is updated)
            * tasks, to get playbook tasks (result is cached, and cache expire when playbook is updated)
            * groups, to get groups and members from inventories (result is cached using ttl)
            * groupvars, to get groups variables (result is cached using ttl)
            * launch, to launch a playbook
        * Internal:
            * runs, to get existing Ansible runs
            * run, to get information on Ansible run from runid
            * To manage ssh agent
                * SSHAgent
                * SSHAgentAdd
                * SSHAgentKill
        * Other
            * demo, to have basic data for demo
            * grapher, wapper on ansible-inventory-grapher
    * All sw2 queries have options:
        * debug=true, to have more details on output
        * help=true, to have self documentation and examples
    * Only for sw2 using cache
        * cache={cache_action}, with cache_action in ['bypass', 'refresh']
        * cache_ttl={seconds}, to override cache_ttl defined in global configuration `/etc/ansible-ws/ansible-ws.yml`

# Setup

## Prerequisite

* For installation
  * Git
* Python => 3.8
* Ansible
* If you want grapher
  * dnf/apt-get install graphviz
  * pip3 install ansible-inventory-grapher

## Defaults

* The default settings are available in defaults of ansible setup role
* See [setup role > defaults]
* By default ansible-ws run on port `8044` but you can override it with an ansible extra_vars as `-e "wsgi_port=80"`

## About selinux

* As ansible-ws launch playbook, for a simple gather_facts, we need to access to many differents resources.
* So, I give up to find a policy/configuration working with selinux. (You can see lasts tests about it in [setup role]).
* So, If you have selinux in `Enforcing` mode we have to set domain `httpd_t` in `Permissive` mode.
* ***CAUTION*** The domain `httpd_t` is set in `Permissive` mode during setup by the [setup role]

## Procedure

### Ubuntu >= Ubuntu 20.04.2 LTS

As root on your server

~~~~
apt-get install ansible
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

* http://localhost:8044/sw2/query

### Examples

* To have global help

~~~bash
curl  http://127.0.0.1:8044/sw2/query \
      --header "Content-Type: application/json" \
      --silent \
      --request POST \
      --data '{}' | jq .
~~~~

* To have help for query `cache_info`

~~~bash
curl  http://127.0.0.1:8044/sw2/query \
      --header "Content-Type: application/json" \
      --silent \
      --request POST \
      --data '{
                "sw2": {
                  "query": "cache_info",
                  "help": true
                }
              }' | jq .
~~~

* To call query `cache_info` (this query has no parameters)

~~~bash
curl  http://127.0.0.1:8044/sw2/query \
      --header "Content-Type: application/json" \
      --silent \
      --request POST \
      --data '{
                "sw2": {
                  "query": "cache_info"
                }
              }' | jq .
~~~

* To query `tasks` with missing parameters give you errors and usages

~~~bash
curl  http://127.0.0.1:8044/sw2/query \
      --header "Content-Type: application/json" \
      --silent \
      --request POST \
      --data '{
                "sw2": {
                  "query": "tasks"
                }
              }' | jq .
~~~

* To query `tasks`

~~~bash
curl  http://127.0.0.1:8044/sw2/query \
      --header "Content-Type: application/json" \
      --silent \
      --request POST \
      --data '{
                "sw2": {
                  "query": "tasks"
                  },
                "parameters": {
                  "playbook": "~/ansible-ws/tests/data/playbooks/tags.yml"
                }
              }' | jq .
~~~

