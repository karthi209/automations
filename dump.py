name: "Create integration testing github summary"
description: "Takes the integration pytest report as input in json format and generates a GitHub summary"
inputs:
  GITHUB_TOKEN:
    description: "Token for auth"
    required: true

runs:
  using: "composite"
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Download all reports
      uses: actions/download-artifact@v4
      with:
        name: integration-test-results
        path: test_scripts/
        
    - name: Generate Test Report
      run: |
        cd test_scripts
        rm -f test_results.md  # Ensure the file is clean before running
        for file in test_report_*.json; do
          [ -e "$file" ] || continue  # Skip if no matching files exist
          python3 test_summary.py "$file"
        done
      shell: bash

    - name: Display test report in GitHub summary
      if: always()
      run: |
        echo "## Integration Test Report" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
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
        git commit -m "Integration test report for v$TAG"
        git push
      shell: bash
