# Define variables
$VMName = "PowershellTestVM"
$VMPath = "C:\ProgramData\Microsoft\Windows\Hyper-V\Virtual Machines\$VMName"
$ISOPath = "C:\Archive\VirtualBoxOS\debian-12.5.0-amd64-netinst-preseed.iso"
$SwitchName = "External Switch"  # Name of the virtual switch to connect the VM to

# Create the VM
New-VM -Name $VMName -MemoryStartupBytes 2GB -VHDPath "C:\ProgramData\Microsoft\Windows\Virtual Hard Disks\server.vhdx" -SwitchName $SwitchName

# Set the number of processors
Set-VM -Name $VMName -ProcessorCount 1

# Enable Dynamic Memory (optional)
Set-VM -Name $VMName -DynamicMemory

# Attach the ISO file to the VM
Add-VMDvdDrive -VMName $VMName -Path $ISOPath

# Start the VM
Start-VM -Name $VMName
