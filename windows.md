
Get-Item -Path WSMan:\localhost\Service\Auth
Get-Item -Path WSMan:\localhost\Client\Auth
Get-Item -Path WSMan:\localhost\Service\AllowUnencrypted


Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $true
Set-Item -Path WSMan:\localhost\Client\Auth\Basic -Value $true
Set-Item -Path WSMan:\localhost\Service\AllowUnencrypted -Value $true


Get-NetConnectionProfile

Get-NetConnectionProfile | ForEach-Object { Set-NetConnectionProfile -Name $_.Name -NetworkCategory Private }

Set-WSManQuickConfig -force