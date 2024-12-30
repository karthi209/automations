# Define variables
$CertStorePath = "Cert:\LocalMachine\My"
$CertDnsName = "localhost"
$WinRMPort = 5986

# Generate a new self-signed certificate
Write-Host "Generating a new self-signed certificate..." -ForegroundColor Green
$NewCert = New-SelfSignedCertificate -DnsName $CertDnsName -CertStoreLocation $CertStorePath -NotAfter (Get-Date).AddYears(5)

if (!$NewCert) {
    Write-Host "Failed to create the certificate. Exiting." -ForegroundColor Red
    exit 1
}

Write-Host "New certificate created with Thumbprint: $($NewCert.Thumbprint)" -ForegroundColor Green

# Remove existing HTTPS WinRM listener (if any)
Write-Host "Removing existing HTTPS WinRM listener (if any)..." -ForegroundColor Green
try {
    winrm delete winrm/config/Listener?Address=*+Transport=HTTPS
} catch {
    Write-Host "No existing HTTPS listener to delete or deletion failed. Proceeding." -ForegroundColor Yellow
}

# Create a new HTTPS WinRM listener with the new certificate
Write-Host "Creating a new HTTPS WinRM listener..." -ForegroundColor Green
$Thumbprint = $NewCert.Thumbprint

# Use PowerShell cmdlet to create the listener
try {
    New-Item -Path WSMan:\LocalHost\Listener -Transport HTTPS -Address * -CertificateThumbprint $Thumbprint -Force
    Write-Host "Listener created successfully." -ForegroundColor Green
} catch {
    Write-Host "Failed to create the listener. Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Enable the WinRM service
Write-Host "Enabling and starting WinRM service..." -ForegroundColor Green
Set-Service -Name WinRM -StartupType Automatic
Start-Service -Name WinRM

# Configure the firewall to allow HTTPS WinRM traffic
Write-Host "Configuring firewall to allow WinRM HTTPS traffic..." -ForegroundColor Green
try {
    New-NetFirewallRule -Name "WinRM HTTPS" -DisplayName "WinRM HTTPS" -Protocol TCP -LocalPort $WinRMPort -Action Allow -Direction Inbound
    Write-Host "Firewall rule created successfully." -ForegroundColor Green
} catch {
    Write-Host "Failed to create firewall rule. It might already exist. Proceeding." -ForegroundColor Yellow
}

# Verify the new listener
Write-Host "Verifying the new WinRM listener..." -ForegroundColor Green
$Listeners = winrm enumerate winrm/config/listener
if ($Listeners -match "Transport=HTTPS") {
    Write-Host "WinRM HTTPS listener configured successfully!" -ForegroundColor Green
    Write-Host "Certificate Thumbprint: $($NewCert.Thumbprint)"
} else {
    Write-Host "Failed to configure WinRM HTTPS listener. Please check the logs." -ForegroundColor Red
    exit 1
}

Write-Host "All steps completed successfully!" -ForegroundColor Green
