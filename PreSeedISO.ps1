<#
.SYNOPSIS
    This PowerShell script automates the process of customizing a Debian installation ISO by adding a preseed configuration file to enable quick Debian setup.

.DESCRIPTION
    This PowerShell script automates the process of customizing a Debian installation ISO by adding a preseed configuration file. The script performs the following tasks:
    - Mounts the specified Debian ISO file to a temporary drive letter.
    - Copies all contents of the mounted ISO to a temporary folder.
    - Adds a preseed configuration file (preseed.cfg) to the copied contents.
    - Ensures that required boot files (like isolinux.bin) are copied from the ISO.
    - Creates a new ISO using the Windows ADK’s oscdimg tool with the preseed file integrated.
    - Cleans up temporary folders after the ISO is created.

.PARAMETER SourceISO
    Specifies the path to the source Debian ISO file. Example: "C:\Path\to\debian-12.5.0-amd64-netinst.iso".

.PARAMETER TempFolder
    Specifies the temporary folder where the ISO contents will be copied. Example: "C:\Temp\ISO".

.PARAMETER OutputISO
    Specifies the output path where the new ISO will be saved. Example: "C:\Output\debian-preseed.iso".

.PARAMETER PreseedFile
    Specifies the path to the preseed configuration file (preseed.cfg). Example: "C:\Path\to\preseed.cfg".

.PARAMETER MountedVolumeLetter
    Specifies the drive letter to use for mounting the ISO. Example: "E".

.EXAMPLE
    .\CustomizeDebianISO.ps1 -SourceISO "C:\ISOs\debian-12.5.0-amd64-netinst.iso" -TempFolder "C:\Temp\DebianISO" -OutputISO "C:\Output\debian-custom.iso" -PreseedFile "C:\Configs\preseed.cfg" -MountedVolumeLetter "E"
    This will mount the Debian ISO, copy its contents, add the preseed.cfg file, and create a new ISO with the preseed configuration.

.EXAMPLE
    .\CustomizeDebianISO.ps1 -SourceISO "C:\ISOs\debian-12.5.0-amd64-netinst.iso" -TempFolder "C:\Temp\DebianISO" -OutputISO "C:\Output\debian-custom.iso" -PreseedFile "C:\Configs\preseed.cfg" -MountedVolumeLetter "D"
    This will mount the Debian ISO on drive D:, add the preseed.cfg, and create a new ISO.

.NOTES
    NAME:    CustomizeDebianISO.ps1
    AUTHOR:  Karthikeyan Manimaran
    DATE:    2024/12/30
    LICENSE: MIT License
    VERSION HISTORY:
        1.0 2024/12/30 - Initial Version

#>

Write-Host " "
Write-Host " "

Write-Host "Welcome to PreSeedISO tool!"

Write-Host " "

# Display ASCII art when the script runs
Write-Host "____           ____                _   ___ ____   ___"
Write-Host "|  _ \ _ __ ___/ ___|  ___  ___  __| | |_ _/ ___| / _ \ "
Write-Host "| |_) | '__/ _ \___ \ / _ \/ _ \/ _` |  | |\___ \| | | |"
Write-Host "|  __/| | |  __/___) |  __/  __/ (_| |  | | ___) | |_| |"
Write-Host "|_|   |_|  \___|____/ \___|\___|\__,_| |___|____/ \___/ "

Write-Host " "
Write-Host " "

# Set paths for the source ISO, temporary mount, and output paths
$sourceISO = "C:\Archive\VirtualBoxOS\debian-12.5.0-amd64-netinst.iso"  # Original Debian ISO path
$tempFolder = "C:\Archive\VirtualBoxOS\Temp"  # Temporary folder to mount ISO contents
$outputISO = "C:\Archive\VirtualBoxOS\debian-12.5.0-amd64-netinst-preseed.iso"  # New ISO output path
$preseedFile = "C:\Archive\VirtualBoxOS\preseed.cfg"  # Path to the preseed.cfg file

Write-Host "Source ISO: $sourceISO" -ForegroundColor Green
Write-Host "Temporary folder for mounting ISO: $tempFolder" -ForegroundColor Green
Write-Host "Output ISO: $outputISO" -ForegroundColor Green
Write-Host "Preseed file: $preseedFile" -ForegroundColor Green

# Manually specify the mounted volume drive letter (e.g., D, E, etc.)
$mountedVolumeLetter = "E"  # Change this to the drive letter of the mounted ISO

Write-Host "Mounted Volume Drive Letter: $mountedVolumeLetter" -ForegroundColor Green

Write-Host " "
Write-Host " "

# Create the temporary folder if it doesn't exist
If (-Not (Test-Path $tempFolder)) {
    Write-Host "Creating temporary folder at: $tempFolder"
    New-Item -ItemType Directory -Force -Path $tempFolder
} else {
    Write-Host "Temporary folder already exists at: $tempFolder"
}

# Check if the specified drive letter is already in use
$existingVolume = Get-Volume | Where-Object { $_.DriveLetter -eq $mountedVolumeLetter }

Write-Host " "
Write-Host " "

if ($existingVolume) {
    Write-Host "Error: Drive letter $mountedVolumeLetter is already in use. Please choose a different drive letter." -ForegroundColor Red
    exit 1
} else {
    Write-Host "Drive letter $mountedVolumeLetter is available. Proceeding with mounting the ISO..." -ForegroundColor Green
}

Write-Host " "
Write-Host " "

# Mount the ISO (this is Windows' built-in mounting feature)
Write-Host "Mounting the ISO..."
Mount-DiskImage -ImagePath $sourceISO
Start-Sleep -Seconds 10  # Allow time for the disk to mount

# Ensure the mounted volume is accessible
$mountedVolumePath = "${mountedVolumeLetter}:"

Write-Host "Mounted volume path: $mountedVolumePath"

Write-Host " "
Write-Host " "

# Copy the contents of the mounted ISO to the temporary folder
Write-Host "Copying contents from mounted ISO to temporary folder..."
Copy-Item -Path "$mountedVolumePath\*" -Recurse -Destination $tempFolder -Force

Write-Host "ISO contents copied to temporary folder." -ForegroundColor Green

# Add the preseed.cfg to the appropriate directory (usually in the "preseed" folder or root)
$preseedDest = "$tempFolder\preseed"
If (-Not (Test-Path $preseedDest)) {
    Write-Host "Creating preseed folder in temporary directory..."
    New-Item -ItemType Directory -Force -Path $preseedDest
} else {
    Write-Host "Preseed folder already exists in temporary directory."
}

Write-Host "Copying preseed.cfg to the preseed folder..."
Copy-Item -Path $preseedFile -Destination $preseedDest -Force

Write-Host "Preseed configuration file added to temporary folder."

# Ensure isolinux.bin exists in the temp folder
$isolinuxBinPath = "$tempFolder\isolinux\isolinux.bin"
If (-Not (Test-Path $isolinuxBinPath)) {
    Write-Host "Error: isolinux.bin not found in the temporary folder, checking mounted ISO..."  -ForegroundColor Red

    $originalIsolinuxBinPath = "${mountedVolumePath}\isolinux\isolinux.bin"
    If (Test-Path $originalIsolinuxBinPath) {
        Write-Host "Copying isolinux.bin from the mounted ISO..."
        Copy-Item -Path $originalIsolinuxBinPath -Destination "$tempFolder\isolinux" -Force
        Write-Host "isolinux.bin copied to temporary folder."  -ForegroundColor Green
    } Else {
        Write-Host "Error: isolinux.bin not found in the source ISO." -ForegroundColor Red
        Exit 1
    }
} else {
    Write-Host "isolinux.bin already exists in temporary folder."
}

# Unmount the ISO after copying the files
Write-Host "Unmounting ISO..."
Dismount-DiskImage -ImagePath $sourceISO

Write-Host "ISO unmounted successfully."  -ForegroundColor Green

# Generate a new ISO using oscdimg (this requires the Windows ADK)
$oscdimgPath = "C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools\amd64\Oscdimg\oscdimg.exe"

Write-Host "oscdimg path: $oscdimgPath"

# Run oscdimg to create the new ISO
$arguments = "-u2", "-b$isolinuxBinPath", "-m", "-o", "$tempFolder", "$outputISO"
Write-Host "Running oscdimg to create the new ISO..."

Start-Process -FilePath $oscdimgPath -ArgumentList $arguments -Wait -NoNewWindow

Write-Host "ISO creation process completed." -ForegroundColor Green

Write-Host " "
Write-Host " "

# Check if the new ISO was created successfully
If (Test-Path $outputISO) {
    Write-Host "ISO created successfully at: $outputISO" -ForegroundColor Green
} Else {
    Write-Host "Error: ISO not found. Please check the output path." -ForegroundColor Red
}

Write-Host " "
Write-Host " "

# Clean up the temporary folder with error handling
try {
    Write-Host "Cleaning up temporary folder..."
    Remove-Item -Path $tempFolder -Recurse -Force
    Write-Host "Temporary folder cleaned up successfully." -ForegroundColor Green
} catch {
    Write-Host "Warning: Failed to remove some items in the temporary folder. Please check manually." -ForegroundColor Yellow
}

Write-Host " "
Write-Host " "

Write-Host "Thank you for using PreSeed ISO!"
