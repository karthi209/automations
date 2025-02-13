- name: Run Test Script
      env:
        TAG: ${{ env.TAG }}
      run: |
        cd test_scripts
        python3 test_manager.py ${{ inputs.AGENT_TYPE }}-${{ inputs.AGENT_TEAM }}-all-tools:$IMAGE_TAG

        IMAGE_NAME="${{ inputs.AGENT_TYPE }}_${{ inputs.AGENT_TEAM }}_all_tools_${IMAGE_TAG}"
        echo "IMAGE_NAME=$IMAGE_NAME" >> "$GITHUB_ENV"
        
        RPT_NAME="test_report_docker_dev_local_devopsrepo_kp_org_agents_$IMAGE_NAME.json"
        echo "RPT_NAME=$RPT_NAME" >> "$GITHUB_ENV"

        echo "RPT_NAME=$RPT_NAME" >> "$GITHUB_OUTPUT"

      shell: bash
      
    - name: Archive test results
      if: always()
      uses: github-marketplace-actions/.github/actions/actions/upload-artifact@v1
      env:
        TAG: ${{ env.RPT_NAME }}
      with:
        name: integration-test-results
        path: "test_scripts/${{ env.RPT_NAME }}"
        retention-days: 7

    - name: Check Pytest Test Report for Failures
      env:
        TAG: ${{ env.RPT_NAME }}
      run: |
        TEST_REPORT="test_scripts/${{ env.RPT_NAME }}"

        # Validate if the JSON file exists
        if [[ ! -f "$TEST_REPORT" ]]; then
          echo "❌ Test report not found! Failing the job."
          exit 1
        fi

        # Check if any tests failed using jq
        FAILED_TESTS=$(jq '.summary.failed' "$TEST_REPORT")
        EXIT_CODE=$(jq '.exitcode' "$TEST_REPORT")

        if [[ "$EXIT_CODE" -ne 0 ]] || [[ "$FAILED_TESTS" -gt 0 ]]; then
          echo "❌ Tests failed! $FAILED_TESTS tests failed."
          exit 1
        else
          echo "✅ All tests passed!"
        fi
      shell: bash
