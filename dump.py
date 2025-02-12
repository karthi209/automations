- name: Check Pytest Test Report for Failures
        run: |
          TEST_REPORT="./test-results/test_report.json"

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
