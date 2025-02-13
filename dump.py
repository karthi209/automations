        cd test_scripts
        python3 test_manager.py ${{ inputs.AGENT_TYPE }}-${{ inputs.AGENT_TEAM }}-all-tools:$IMAGE_TAG
        
        IMAGE_NAME="test_report_${{ inputs.AGENT_TYPE }}_${{ inputs.AGENT_TEAM }}_all_tools_${IMAGE_TAG}.json"
        echo "IMAGE_NAME=$IMAGE_NAME" >> "$GITHUB_OUTPUT"
        IMG_NAME=$(echo "${{ env.IMAGE_NAME }}" | sed 's/[.:/-]/_/g')
        echo "IMG_NAME=$IMG_NAME" >> "$GITHUB_OUTPUT"
        RPT_NAME="test_report_docker_dev_local_devopsrepo_kp_org_agents_${{ env.IMG_NAME }}.json"
        echo "RPT_NAME=$RPT_NAME" >> "$GITHUB_OUTPUT"
