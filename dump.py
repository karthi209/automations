name: Process Jenkins Test Results

on:
  workflow_dispatch:
  workflow_run:
    workflows: ["Your Trigger Workflow Name"]
    types:
      - completed

jobs:
  create-dashboard:
    runs-on: ubuntu-latest
    steps:
      - name: Download all artifacts
        uses: dawidd6/action-download-artifact@v2
        with:
          workflow: ${{ github.event.workflow.id }}
          workflow_conclusion: completed
          path: artifacts
          
      - name: Process Results and Create Dashboard
        run: |
          # Initialize dashboard with header
          echo "# Jenkins Integration Tests Dashboard" > dashboard.md
          
          # Get unique team names and sort them
          teams=$(find artifacts -type f -name "result_*.md" -exec grep "Team:" {} \; | cut -d' ' -f2- | sort -u)
          
          # Process results for each team
          for team in $teams; do
            echo -e "\n## $team" >> dashboard.md
            echo "| Job Name | Build Number | Build URL | Status |" >> dashboard.md
            echo "|-----------|--------------|-----------|---------|" >> dashboard.md
            
            # Find all result files for this team
            find artifacts -type f -name "result_*.md" | while read -r file; do
              # Check if file belongs to current team
              if grep -q "Team: $team" "$file"; then
                # Extract required fields
                job_name=$(grep "Job Name:" "$file" | cut -d' ' -f3-)
                build_num=$(grep "Build Number:" "$file" | cut -d' ' -f3-)
                build_url=$(grep "Build URL:" "$file" | sed -n 's/.*\[\(.*\)\](\(.*\))/\2/p')
                status=$(grep "Status:" "$file" | cut -d' ' -f3-)
                
                # Create table row
                echo "| $job_name | $build_num | [Link]($build_url) | $status |" >> dashboard.md
              fi
            done
          done
          
          # Add summary statistics
          echo -e "\n## Summary Statistics" >> dashboard.md
          echo "\`\`\`" >> dashboard.md
          echo "Total Teams: $(echo "$teams" | wc -l)" >> dashboard.md
          echo "Total Jobs: $(find artifacts -type f -name "result_*.md" | wc -l)" >> dashboard.md
          echo "Successful Jobs: $(grep -r ":white_check_mark: SUCCESS" artifacts | wc -l)" >> dashboard.md
          echo "Failed Jobs: $(grep -r ":x: FAILURE" artifacts | wc -l)" >> dashboard.md
          echo "\`\`\`" >> dashboard.md
          
          # Add timestamp
          echo -e "\n_Last updated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')_" >> dashboard.md
          
          # Output to GitHub step summary
          cat dashboard.md >> $GITHUB_STEP_SUMMARY
          
      - name: Upload dashboard
        uses: actions/upload-artifact@v3
        with:
          name: jenkins-dashboard
          path: dashboard.md
