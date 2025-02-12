name: "Unit test tools"
description: "Runs molecule test on all tools and generates a github summary with results of the test"
inputs:
  ANSIBLE_VAULT_PASSWORD:
    description: "Ansible vault password"
    required: true

runs:
  using: "composite"
  steps:
    - name: Setup github authentication
        run: |
            git config --global credential.helper store
            git config --global url."https://github.org/".insteadOf git@github.org:
            echo "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.org" > ~/.git-credentials
            
      - name: Checkout code
        run: git clone https://github.org/devsecops/${{ matrix.repo }}.git
              
      - name: Copy Selinux dependencies
        run: |
          sudo cp -r /usr/lib64/python3.6/site-packages/selinux /usr/lib64/python3.11/site-packages/selinux
          sudo cp /usr/lib64/python3.6/site-packages/selinux-2.9-py3.6.egg-info /usr/lib64/python3.11/site-packages/selinux-2.9-py3.6.egg-info
        
      - name: Setup Python virtual environment
        run: |
          python -m venv venv
        shell: bash
        
      - name: Authenticating with github
        run: |
          git config --global credential.helper store
          echo "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.org" > ~/.git-credentials
          
      - name: Set vault password
        run: |
          mkdir -p /apps/runner/.user_setup/
          echo "${{ secrets.ANSIBLE_VAULT_PASSWORD }}" > /apps/runner/.user_setup/vault_password
          chmod 600 /apps/runner/.user_setup/vault_password

      - name: Install required pip modules
        run: |
          source venv/bin/activate
          cd ${{ matrix.repo }}
          python -m pip install --upgrade pip
          pip install -r requirements.txt
        shell: bash
        
      - name: Verify molecule installation
        run: |
          source venv/bin/activate
          molecule --version
        shell: bash
          
      - name: Run molecule tests
        run: |
          source venv/bin/activate
          cd ${{ matrix.repo }}
          molecule test | tee molecule-test-${{ matrix.repo }}.txt
        env:
          PY_COLORS: '1'
          ANSIBLE_FORCE_COLOR: '1'
          GIT_ASKPASS: /usr/bin/true
          GIT_TERMINAL_PROMPT: 0
          
      - name: Archive verify test results
        if: always()
        uses: devsecops/github-marketplace-actions/.github/actions/actions/upload-artifact@v1
        with:
          name: unit-test-results
          path: ./${{ matrix.repo }}/molecule-test-${{ matrix.repo }}.txt
          retention-days: 7
          
      - name: Clean up
        run: |
          ls -la
          rm -rf ${{ matrix.repo }}
          rm -rf venv
          rm -rf /apps/runner/.user_setup/vault_password
          rm -rf ~/.git-credentials
          ls -la
