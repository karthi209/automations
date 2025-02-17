# Running Tests for Agent Build

The `run-tests` workflow is an integrated workflow designed to handle testing. This workflow is automatically triggered when a pull request is created to merge into the `production` branch.

Additionally, the workflow can be triggered manually by clicking on the `Run workflow` option in the Actions tab. When triggered manually, the workflow provides a few options to select from.

## Options

### **RUN UNIT TEST**
When this option is selected, the workflow executes Molecule tests on all collections used by `agent_build`, generates a report, and presents it in the GitHub Actions (GHA) job summary.

### **RUN INTEGRATION TEST (Builds new image and runs the test)**
When this option is selected, the workflow builds the test image (e.g., `jenkins-bluemix` and `scale-set-runner-bluemix`), executes the pytest scripts inside the container, and generates a report, which is presented in the GHA job summary.

### **RUN INTEGRATION TEST (Runs the test using an existing image provided in OPTION 4)**
This option runs integration tests on an already built image. The workflow pulls the image provided in the `OPTION 4` field, spins up a container, runs the test cases inside the container, and generates a report, which is presented in the GHA job summary.

### **IMAGE_NAME (Required only if OPTION 3 is selected)**
If `OPTION 3` is selected, this field is mandatory. Provide the image name in the format:
- `scale-set-runner-foft-all-tools:2.2.68`
- `jenkins-foft-all-tools:2.2`

The `pull request` trigger runs `OPTION 1` and `OPTION 2` by default. Even for manual triggers, `OPTION 3` and `OPTION 2` are selected by default, but you can modify the options before triggering the workflow.

## What Do Unit Tests and Integration Tests Mean in the Agent Build Context?

### **Unit Test**
A unit test is executed by running Molecule tests on individual tool collections. We spin up an agent image, install only a specific collection, and verify that the tool is installed correctly and behaves as expected in an isolated environment.

### **Integration Test**
An integration test is executed on a container that is spun up using the `final` agent build image. The image used for integration tests is the same exact image that will be released for Jenkins and other agent runner images. This test helps identify dependency issues or conflicts between different collections during the integration testing phase.

