name: "Unit Test Tools"
description: "Runs molecule tests on all tools and generates a GitHub summary with results"
inputs:
  ansible_vault_password:
    description: "Ansible vault password"
    required: true
  repo:
    description: "Tool repository to test"
    required: true

runs:
  using: "composite"
  steps:
    - name: Setup GitHub authentication
      shell: bash
      run: |
        git config --global credential.helper store
        git config --global url."https://github.org/".insteadOf git@github.org:
        echo "https://x-access-token:${{ inputs.GITHUB_TOKEN }}@github.org" > ~/.git-credentials

    - name: Checkout code
      shell: bash
      run: |
        git clone https://github.org/devsecops/${{ inputs.repo }}.git

    - name: Copy SELinux dependencies
      shell: bash
      run: |
        sudo cp -r /usr/lib64/python3.6/site-packages/selinux /usr/lib64/python3.11/site-packages/selinux
        sudo cp /usr/lib64/python3.6/site-packages/selinux-2.9-py3.6.egg-info /usr/lib64/python3.11/site-packages/selinux-2.9-py3.6.egg-info

    - name: Setup Python virtual environment
      shell: bash
      run: |
        python -m venv venv

    - name: Set vault password
      shell: bash
      run: |
        mkdir -p /apps/runner/.user_setup/
        echo "${{ inputs.ansible_vault_password }}" > /apps/runner/.user_setup/vault_password
        chmod 600 /apps/runner/.user_setup/vault_password

    - name: Install required pip modules
      shell: bash
      run: |
        source venv/bin/activate
        cd ${{ inputs.repo }}
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Verify Molecule installation
      shell: bash
      run: |
        source venv/bin/activate
        molecule --version

    - name: Run Molecule tests
      shell: bash
      run: |
        source venv/bin/activate
        cd ${{ inputs.repo }}
        molecule test | tee molecule-test-${{ inputs.repo }}.txt
      env:
        PY_COLORS: '1'
        ANSIBLE_FORCE_COLOR: '1'
        GIT_ASKPASS: /usr/bin/true
        GIT_TERMINAL_PROMPT: 0

    - name: Archive test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: unit-test-results
        path: ./${{ inputs.repo }}/molecule-test-${{ inputs.repo }}.txt
        retention-days: 7

    - name: Clean up
      shell: bash
      run: |
        ls -la
        rm -rf ${{ inputs.repo }}
        rm -rf venv
        rm -rf /apps/runner/.user_setup/vault_password
        rm -rf ~/.git-credentials
        ls -la
