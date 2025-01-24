---
- name: Install JFrog CLI using YUM
  hosts: all
  become: true

  tasks:
    - name: Create and configure the JFrog CLI YUM repository
      copy:
        dest: /etc/yum.repos.d/jfrog-cli.repo
        content: |
          [jfrog-cli]
          name=JFrog CLI
          baseurl=https://releases.jfrog.io/artifactory/jfrog-rpms
          enabled=1
          gpgcheck=1

    - name: Import primary GPG key for JFrog CLI
      rpm_key:
        state: present
        key: https://releases.jfrog.io/artifactory/api/v2/repositories/jfrog-rpms/keyPairs/primary/public

    - name: Import secondary GPG key for JFrog CLI (for backward compatibility)
      rpm_key:
        state: present
        key: https://releases.jfrog.io/artifactory/api/v2/repositories/jfrog-rpms/keyPairs/secondary/public

    - name: Install JFrog CLI package
      yum:
        name: jfrog-cli-v2-jf
        state: present

    - name: Display introductory message for JFrog CLI
      command: jf intro
      register: jfrog_intro
      changed_when: false

    - name: Show JFrog CLI intro message
      debug:
        var: jfrog_intro.stdout
