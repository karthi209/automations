# Ansible Notes

### Installation

```bash
pip install ansible
ansible --version
```

### Some quick adhoc commands

Setup inventory

```bash
ansible -i linux.yml all -m ping
ansible -i linux.yml all -m command -a "uptime"
ansible -i linux.yml all -m command -a "df -h"

ansible -i windows.yml all -m win_ping
ansible -i windows.yml all -m win_command -a "hostname"
ansible -i windows.yml all -m win_command -a "java -version"
```

```ansible.cfg
[defaults]
host_key_checking = False
```

### Ansible Architecture

ANSIBLE IS AGENTLESS! No need to install ansible in remote nodes.

- Control node:

    The machine where Ansible is installed and from which all tasks and playbooks are run
    
    What needs to be installed:
        - Python
        - Ansible

- Managed node (hosts):

    The servers (nodes) you manage with Ansible. There’s no need to install Ansible on these nodes, as the control node communicates with them using SSH or WinRM.

    What needs to be installed:
        - Python for linux nodes
        - WinRM and PowerShell for windows nodes

### How ansible works:

- playbooks:
    specifies what tasks to run

- inventory:
    defines target managed nodes (Linux, Windows, network devices, cloud instances).

- connection to managed nodes:
    linus (SSH) (PORT 22)
    windows (WinRM) (PORT 5985/5986)

S1: Execute ansible command

S2: Ansible connects to the nodes in the inventory using SSH/WinRM

S3: Ansible translates YAML playbooks into Python scripts

S4: Control node copies the translated python scripts to the managed nodes (via SSH/SCP for linux and WinRM for windows)

S5: Remote node executes the python scripts using the python interpreter (/usr/bin/python3)

S6: The output is sent back to the Control Node.

S7: Ansible removes the python script and does clean up in remote nodes

```
+--------------------------+
|      Control Node        |  
| (Runs Ansible CLI, YAML) |  
+--------------------------+
         |
         | Parses YAML & Converts to Python Scripts
         v
+---------------------------------------------------+
| SSH (Linux) / WinRM (Windows)                    |
+---------------------------------------------------+
         |
         | Transfers and Executes Python/PowerShell Scripts
         v
+--------------------------+  +--------------------------+
|    Linux Managed Node    |  |   Windows Managed Node  |
|  - Executes Python       |  |  - Executes PowerShell  |
|  - Installs Packages     |  |  - Manages Services     |
|  - Configures Services   |  |  - Configures Settings  |
+--------------------------+  +--------------------------+

```

*Quick Tip:* You can see the generated Python script by using verbose mode (-vvv):

```bash
ansible all -m ping -vvv
```

### Anisble Playbooks

```bash
ansible-playbook -i linux.yml playbook.yml --check
```


