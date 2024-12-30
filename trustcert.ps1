# Configure WinRM to trust self-signed certificates
Set-Item WSMan:\localhost\Client\TrustedHosts -Value '*' -Force

# Configure PowerShell to ignore SSL certificate validation for localhost
$Value = @'
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
if (-not ([System.Management.Automation.PSTypeName]'ServerCertificateValidationCallback').Type)
{
    $certCallback = @"
        using System;
        using System.Net;
        using System.Net.Security;
        using System.Security.Cryptography.X509Certificates;
        public class ServerCertificateValidationCallback
        {
            public static void Ignore()
            {
                ServicePointManager.ServerCertificateValidationCallback += 
                    delegate
                    (
                        Object obj, 
                        X509Certificate certificate, 
                        X509Chain chain, 
                        SslPolicyErrors errors
                    )
                    {
                        return true;
                    };
            }
        }
"@
    Add-Type $certCallback
}
[ServerCertificateValidationCallback]::Ignore()
'@

# Save and run the script
$Value | Out-File "$env:TEMP\EnableSelfSignedCerts.ps1"
. "$env:TEMP\EnableSelfSignedCerts.ps1"