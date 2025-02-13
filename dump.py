name: "Create integration testing github summary"
description: "Takes the integration pytest report as input in json format and generates a github summary"
inputs:
  GITHUB_TOKEN:
    description: "Token for auth"
    required: true

runs:
  using: "composite"
  steps:
    - name: Checkout code
      uses: github-marketplace-actions/.github/actions/actions/checkout@v1
      
    - name: Download all reports
      uses: github-marketplace-actions/.github/actions/actions/download-artifact@v1
      with:
        name: integration-test-results
        path: test_scripts/
        
    - name: Generate Test Report
      run: |
        cd test_scripts
        python3 test_summary.py
      shell: bash

    - name: Add report to github summary
      run: |
        cat $GITHUB_WORKSPACE/test_scripts/test_results.md >> $GITHUB_STEP_SUMMARY
      shell: bash

    - name: Push report to wiki
      env:
        GITHUB_TOKEN: ${{ inputs.GITHUB_TOKEN }}
        TAG: ${{ env.TAG }}
      run: |
        git clone https://x-access-token:${{ inputs.GITHUB_TOKEN }}@github.org/${{ github.repository }}.wiki.git wiki
        mv $GITHUB_WORKSPACE/test_scripts/test_results.md wiki/integration_test_results_v$TAG.md
        cd wiki
        git config user.name "${{ github.actor }}"
        git config user.email "${{ github.actor }}"@users.noreply.github.org
        git add .
        git commit -m "integration test report for v$TAG"
        git push
      shell: bash
