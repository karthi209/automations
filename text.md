1️⃣ Variable Scoping (Where Variables Apply)
Understanding where a variable is defined and where it can be accessed is crucial in Ansible. Variables can be scoped to:

Global (Defined via -e, set_facts, or role defaults)
Play (Defined in vars: inside a playbook)
Host (Defined in inventory files)
Task (Defined inside a specific task


- name: Scoping Example
  hosts: localhost
  gather_facts: no
  vars:
    play_scope: "I am play scoped"
  tasks:
    - name: Define Task Scoped Variable
      set_fact:
        task_scope: "I am task scoped"
    
    - name: Display Variables
      debug:
        msg: "Play Scope: {{ play_scope }}, Task Scope: {{ task_scope }}"

Registering Variables
You can capture command output and use it dynamically in playbooks.

- name: Register Example
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Run a shell command
      shell: "echo Hello, Ansible!"
      register: command_output
    
    - name: Print the output
      debug:
        msg: "Command Output: {{ command_output.stdout }}"


- name: Custom Fact Example
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Set a custom fact
      set_fact:
        my_custom_var: "I am a custom fact"
    
    - name: Print custom fact
      debug:
        msg: "Custom Fact: {{ my_custom_var }}"
