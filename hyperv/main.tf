provider "null" {}

resource "null_resource" "create_vm" {
  provisioner "remote-exec" {
    connection {
      host     = "localhost"  # Replace with your Hyper-V host IP
      type     = "winrm"
      user     = "karth"        # Replace with the username for WinRM authentication
      password = "Telecaster@1959"        # Replace with the password for WinRM authentication
      https    = true                    # Set to true if using HTTPS for WinRM
      insecure = true                   # Set to false if using a trusted certificate
    }

    inline = [
      # PowerShell command to create a new VM on Hyper-V
      "powershell.exe -Command \"New-VM -Name 'TerrafromTestVM' -MemoryStartupBytes 2GB -Generation 2 -SwitchName 'ExternalSwitch'\"",

      # PowerShell command to create a new virtual hard disk (VHD)
      "powershell.exe -Command \"New-VHD -Path 'C:\\ProgramData\\Microsoft\\Windows\\Virtual Hard Disks\\TerrafromTestVM.vhdx' -SizeBytes 10GB -Dynamic\"",

      # PowerShell command to add the newly created VHD to the VM
      "powershell.exe -Command \"Add-VMHardDiskDrive -VMName 'TerrafromTestVM' -Path 'C:\\ProgramData\\Microsoft\\Windows\\Virtual Hard Disks\\TerrafromTestVM.vhdx'\"",

      # PowerShell command to start the VM after creation
      "powershell.exe -Command \"Start-VM -Name 'TerrafromTestVM'\""
    ]
  }

  # Optionally, you can add a `depends_on` block if your VM creation depends on other resources.
  # depends_on = [some_other_resource]
}

output "vm_creation_status" {
  value = null_resource.create_vm.id
}
