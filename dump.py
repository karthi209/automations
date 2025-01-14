{
  "github-cli": {
    "command": "gh --version | head -n 1 | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "az-cli": {
    "command": "az --version | head -n 1 | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "bluemix-cli": {
    "command": "bluemix --version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "ibmcloud-cli": {
    "command": "ibmcloud -v | awk 'NR==1' | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "sqlcmd": {
    "command": "sqlcmd -? | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "psql": {
    "command": "psql --version | awk '{print $3}'"
  },
  "curl": {
    "command": "curl -V | head -n 1 | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "yq": {
    "command": "yq -V| head -n 1 | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "openshift-cli": {
    "command": "oc version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "sqlplus": {
    "command": "sqlplus -V | awk 'NR==2' | awk '{print $3}'"
  },
  "rsync": {
    "command": "rsync --version | awk '{print $NF}'"
  },
  "skopeo": {
    "command": "skopeo --version | awk '{print $3}'"
  },
  "checkmarx": {
    "command": "cx version | awk '{print $NF}'"
  },
  "jfrog-cli": {
    "command": "jf -v | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "databricks-cli": {
    "command": "databricks --version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "twist-cli": {
    "command": "twist-cli --version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "powershell": {
    "command": "pwsh -v | awk '{print $NF}'"
  },
  "nexusiq-cli": {
    "command": "pwsh -v | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "gettext": {
    "command": "gettext --version | head -n 1 | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "buildah": {
    "command": "buildah version | awk '{print $NF}'"
  },
  "ansible": {
    "command": "ansible --version | awk '/Version:/ {print $2}'"
  },
  "ansible-playbook": {
    "command": "ansible-playbook --version | head -n 1 | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "terraform": {
    "command": "terraform --version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "git": {
    "command": "git --version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "mercurial": {
    "command": "hg --version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "mvn": {
    "command": "mvn -version | awk '{print $3}'"
  },
  "ant": {
    "command": "ant -version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "gradle": {
    "command": "gradle -version | grep 'Gradle' | awk '{print $2}'"
  },
  "java": {
    "command": "java -version 2>&1 | awk '/Version/ {print $2}'"
  },
  "python": {
    "command": "python3 --version | awk '{print $2}'"
  },
  "node": {
    "command": "node --version | awk '{print substr($0,2)}'"
  },
  "go": {
    "command": "go version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "ng": {
    "command": "ng --version"
  },
  "grunt": {
    "command": "grunt --version | grep grunt-cli | awk '{print $NF}' | sed 's/^v//'"
  },
  "dotnet": {
    "command": "dotnet --version"
  },
  "groovy": {
    "command": "groovy -v | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "helm": {
    "command": "helm version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "kubelogin": {
    "command": "kubelogin --version | head -n 2 | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "kubectl": {
    "command": "kubectl version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "docker": {
    "command": "docker --version | awk '{print $3}' | sed 's/,//'"
  },
  "kubeseal": {
    "command": "kubeseal --version | awk 'NR==1' | awk '{print $NF}'"
  },
  "kubeval": {
    "command": "kubeval --version | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "chrome": {
    "command": "google-chrome --version | awk '{print $NF}'"
  },
  "opa": {
    "command": "opa version | awk '{print $2}'"
  },
  "liquibase": {
    "command": "liquibase -v | awk '/liquibase version/{print $NF}'"
  },
  "sonar-scanner": {
    "command": "sonar-scanner --version | head -n 3 | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  },
  "sonar-runner": {
    "command": "sonar-runner --version | awk '{print $3}'"
  },
  "tidelift-cli": {
    "command": "tidelift version | awk 'NR==1' | awk '{match($0, /[0-9]+.[0-9]+.[0-9]+/, arr); if (arr[0]) print arr[0]}'"
  }
}
