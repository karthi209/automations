Variables in Ansible can be defined in multiple ways:

Playbooks (vars:)
Inventory files
Extra Vars (-e flag)
Role defaults/vars
Environment variables

Priority	Location	Level
1️⃣	Extra vars (-e VAR=value)	CLI
2️⃣	Task vars (inline inside a task)	Task
3️⃣	Role defaults (vars: inside a role)	Role
4️⃣	Inventory (inventory.ini, inventory.yml)	Inventory
5️⃣	Playbook vars (inside a playbook)	Playbook
6️⃣	Environment variables (env:)	OS
7️⃣	Role defaults (defaults/main.yml)	Role


Executable Examples
(A) Using vars in a Playbook
yaml
Copy
Edit
---
- name: Demo of Playbook Variables
  hosts: localhost
  gather_facts: no

  vars:
    greeting: "Hello from Playbook Vars"

  tasks:
    - name: Display Greeting
      debug:
        msg: "{{ greeting }}"
Run:
sh
Copy
Edit
ansible-playbook playbook.yml
(B) Using Inventory Variables
inventory.yml
yaml
Copy
Edit
all:
  hosts:
    myserver:
      ansible_host: 127.0.0.1
      env_name: "Production"
playbook.yml
yaml
Copy
Edit
---
- name: Demo of Inventory Variables
  hosts: myserver
  gather_facts: no

  tasks:
    - name: Show Environment Name
      debug:
        msg: "Environment: {{ env_name }}"
Run:
sh
Copy
Edit
ansible-playbook -i inventory.yml playbook.yml
(C) Using -e Extra Variables (Highest Precedence)
sh
Copy
Edit
ansible-playbook playbook.yml -e "greeting='Hello from Extra Vars'"
This will override the greeting variable defined in the playbook.

(D) Using vars_files for External Variable Files
variables.yml
yaml
Copy
Edit
greeting: "Hello from External File"
playbook.yml
yaml
Copy
Edit
---
- name: Demo of External Variable Files
  hosts: localhost
  gather_facts: no
  vars_files:
    - variables.yml

  tasks:
    - name: Display Greeting
      debug:
        msg: "{{ greeting }}"
Run:
sh
Copy
Edit
ansible-playbook playbook.yml
