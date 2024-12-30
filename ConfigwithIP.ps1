# Define parameters for the certificate
$certParams = @{
    Subject = "CN=localhost"
    KeyAlgorithm = "RSA"
    KeyLength = 2048
    HashAlgorithm = "SHA256"
    CertStoreLocation = "Cert:\LocalMachine\My"
    FriendlyName = "WinRM HTTPS Certificate"
}

# Define KeyUsage as individual values (not comma-separated)
$keyUsage = [System.Enum]::GetValues([System.Security.Cryptography.X509Certificates.X509KeyUsageFlags]) |
            Where-Object { $_ -eq [System.Security.Cryptography.X509Certificates.X509KeyUsageFlags]::KeyEncipherment -or
                           $_ -eq [System.Security.Cryptography.X509Certificates.X509KeyUsageFlags]::DigitalSignature }

# Create the self-signed certificate without the ProviderName
$cert = New-SelfSignedCertificate @certParams -KeyUsage $keyUsage

# Add SANs by creating a new X509 certificate extension
$san = @(
    "dns=localhost",
    "ipaddress=127.0.0.1"
    # Add your VM's IP here if needed:
    # "ipaddress=yourVMIPAddress"
)

# Convert SAN into a string format for TextExtension
$sanExtension = $san -join ","

# Add the SAN extension manually
$cert | Set-Content -Path "C:\Workspace\Certificate.pem" -Force

# Export the certificate and add the SAN extension
$cert | Export-Certificate -FilePath "C:\Workspace\CertificateWithSAN.cer" -Type CERT

# Output certificate thumbprint for reference
$cert.Thumbprint
