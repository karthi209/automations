#!/bin/bash
set -o pipefail

debug_log() {
    echo "[DEBUG $(date '+%H:%M:%S')] $1" >&2
}

safe_add() {
    local -i a=${1:-0}
    local -i b=${2:-0}
    echo $((a + b))
}

init_dashboard() {
    local dashboard_file="$1"
    debug_log "Initializing dashboard file: $dashboard_file"
    {
        echo "## Summary - Unit Tests v$NEXT_TAG"
        echo ""
        echo -e "\n_Last updated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')_"
        echo "| :bookmark: Tool   | Version | Installed | Molecule Test | :white_check_mark: OK | :ballot_box_with_check: Changed | :radio_button: Skipped | :x: Failed |"
        echo "|--------|----------|---------------|-----------------|----|---------|---------|--------|"
    } > "$dashboard_file"
}

extract_tool_info() {
    local report_file="$1"
    local tool_name="$2"
    local dashboard_file="$3"

    local tool_version=$(grep -oP 'Toolversion:\s*\K[0-9]+\.[0-9]+(\.[0-9]+)?' "$report_file" | head -n 1 || echo "N/A")
    tool_version=$(echo "$tool_version" | sed -E 's/([0-9]+\.[0-9]+\.[0-9]+).*/\1/')

    local binary_exists=$(grep -q 'Binary exists in the path' "$report_file" && echo ":white_check_mark: Yes" || echo ":x: No")
    local functional_test=$(grep -q 'Functional test success' "$report_file" && echo ":white_check_mark: Success" || echo ":x: Failed")

    declare -i ok_count=0
    declare -i changed_count=0
    declare -i skipped_count=0
    declare -i failed_count=0

    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" == *"PLAY RECAP"* ]]; then
            if ! read -r next_line; then continue; fi
            parse_test_line "$next_line" ok_count changed_count skipped_count failed_count
        fi
    done < "$report_file"

    echo "| [$tool_name](https://github.kp.org/devsecops/$tool_name.git) | $tool_version | $binary_exists | $functional_test | $ok_count | $changed_count | $skipped_count | $failed_count |" >> "$dashboard_file"

    # Collect data for chart generation
    echo "$tool_name,$ok_count,$changed_count,$skipped_count,$failed_count" >> chart_data.csv
}

parse_test_line() {
    local line="$1"
    local -n ok_ref="$2"
    local -n changed_ref="$3"
    local -n skipped_ref="$4"
    local -n failed_ref="$5"
    [[ "$line" =~ .*ok=([0-9]+).* ]] && ok_ref=$(safe_add "$ok_ref" "${BASH_REMATCH[1]}")
    [[ "$line" =~ .*changed=([0-9]+).* ]] && changed_ref=$(safe_add "$changed_ref" "${BASH_REMATCH[1]}")
    [[ "$line" =~ .*skipped=([0-9]+).* ]] && skipped_ref=$(safe_add "$skipped_ref" "${BASH_REMATCH[1]}")
    [[ "$line" =~ .*failed=([0-9]+).* ]] && failed_ref=$(safe_add "$failed_ref" "${BASH_REMATCH[1]}")
}

generate_chart() {
    debug_log "Generating chart from data"
    python3 - <<EOF
import matplotlib.pyplot as plt
import pandas as pd

# Read data from CSV
data = pd.read_csv("chart_data.csv", names=["Tool", "OK", "Changed", "Skipped", "Failed"])

# Plot stacked bar chart
ax = data.set_index("Tool").plot(kind="bar", stacked=True, figsize=(10, 6))
ax.set_title("Molecule Test Results Summary")
ax.set_ylabel("Counts")
ax.set_xlabel("Tools")
plt.xticks(rotation=45, ha="right")

# Save chart to file
plt.tight_layout()
plt.savefig("dashboard_chart.png")
EOF

    debug_log "Chart generated and saved as dashboard_chart.png"
}

main() {
    local dashboard_file="dashboard.md"
    init_dashboard "$dashboard_file"

    echo "Tool,OK,Changed,Skipped,Failed" > chart_data.csv
    for report in molecule-test-*.txt; do
        [[ ! -f "$report" ]] && continue
        local tool_name=$(echo "$report" | sed 's/molecule-test-\(.*\)\.txt/\1/')
        extract_tool_info "$report" "$tool_name" "$dashboard_file"
    done

    generate_chart

    cat "$dashboard_file" > "$GITHUB_STEP_SUMMARY"
    echo -e "\n![Test Results](dashboard_chart.png)" >> "$GITHUB_STEP_SUMMARY"
}

main "$@"
