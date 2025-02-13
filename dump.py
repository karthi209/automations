- name: Run Test Script
  id: generate_report
  run: |
    cd test_scripts
    python3 test_manager.py ${{ inputs.AGENT_TYPE }}-${{ inputs.AGENT_TEAM }}-all-tools:$IMAGE_TAG

    # Generate report file name
    IMAGE_NAME="${{ inputs.AGENT_TYPE }}_${{ inputs.AGENT_TEAM }}_all_tools_${IMAGE_TAG}"
    
    # Sanitize file name (replace ., :, /, - with _)
    SAFE_IMAGE_NAME=$(echo "$IMAGE_NAME" | sed 's/[.:/-]/_/g')

    RPT_NAME="test_report_docker_dev_local_devopsrepo_kp_org_agents_$SAFE_IMAGE_NAME.json"
    
    # Export to env & output
    echo "RPT_NAME=$RPT_NAME" >> "$GITHUB_ENV"
    echo "RPT_NAME=$RPT_NAME" >> "$GITHUB_OUTPUT"
  shell: bash

- name: Archive Test Results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: integration-test-results
    path: "test_scripts/${{ env.RPT_NAME }}"
    retention-days: 7

- name: Check Pytest Test Report for Failures
  run: |
    TEST_REPORT="test_scripts/${{ env.RPT_NAME }}"

    # Validate if JSON file exists
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
