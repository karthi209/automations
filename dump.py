generate_chart() {
    debug_log "Generating chart from dashboard data"
    python3 - <<EOF
import os
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Check if the dashboard file exists
dashboard_file = "dashboard.md"
if not os.path.exists(dashboard_file):
    print("Dashboard file not found. Skipping chart generation.")
    exit(0)

# Parse the dashboard file to extract Molecule Test results
data = []
with open(dashboard_file, "r") as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith("|") and not line.startswith("| :bookmark:"):
            parts = line.split("|")
            if len(parts) >= 5:
                molecule_test = parts[4].strip()
                if molecule_test == ":white_check_mark: Success":
                    data.append("Success")
                elif molecule_test == ":x: Failed":
                    data.append("Failed")

# Count the number of successes and failures
results = pd.Series(data).value_counts()
success_count = results.get("Success", 0)
failure_count = results.get("Failed", 0)

# If no data, skip chart generation
if success_count == 0 and failure_count == 0:
    print("No test results to plot.")
    exit(0)

# Plot pie chart
labels = ["Passed", "Failed"]
sizes = [success_count, failure_count]
colors = ["#4CAF50", "#F44336"]  # Green for passed, red for failed

plt.figure(figsize=(6, 6))
plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    wedgeprops={"edgecolor": "black"},
)
plt.title("Molecule Test Results: Pass vs Fail")
plt.tight_layout()

# Save chart to file
plt.savefig("dashboard_chart.png")
print("Chart generated and saved as dashboard_chart.png")

# Convert chart image to Base64
with open("dashboard_chart.png", "rb") as image_file:
    base64_img = base64.b64encode(image_file.read()).decode("utf-8")

# Output the Base64 image string for embedding in the markdown
print(f"Base64 Chart: {base64_img}")
EOF

    if [[ $? -eq 0 ]]; then
        debug_log "Chart generated and Base64 string created successfully"
        # Embed the Base64 image in the GitHub Actions summary
        base64_img=$(python3 -c "import sys; print(sys.stdin.read().strip())" <<< "$base64_img")
        {
            echo "### Dashboard Chart"
            echo ""
            echo "![Dashboard Chart](data:image/png;base64,$base64_img)"
        } >> "$GITHUB_STEP_SUMMARY"
    else
        debug_log "Failed to generate chart"
    fi
}
