### Portas
* HTTP : 5985
* HTTPS: 5986

# OBS
* Use NTLM e nao BASIC para computadores fora do dominio e no dominio use Kerberos

# Validando pré-requisitos (Executar comandos abaixo no PowerShell como Administrator):

    - NET Framework 4.0+: cd c:\Windows\Microsoft.NET\Framework64
    - Powershell 3.0+: Get-Host
    - Winrm Version: winrm id

# WinRM

    - Listar o serviço: 
        - netstat -nap tcp
        - winrm enumerate winrm/config/listener
        
    - Visualizar as configurações
        - winrm get winrm/config
        - winrm get winrm/config/service

    - Configurando permissões para winrm
        - winrm configSDLL default

    - Ativar/Desativar autenticação:
        - Set-Item -Path WSMan:\localhost\Service\Auth\AUTH_METHOD -Value $(true or false)
        - winrm set winrm/config/service/auth '@{Basic="true"}'


# WinRM Memory Hotfix

Git: https://github.com/jborean93/ansible-windows/blob/master/scripts/Install-WMF3Hotfix.ps1

Script PowerShell:

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$url = "https://raw.githubusercontent.com/jborean93/ansible-windows/master/scripts/Install-WMF3Hotfix.ps1"
$file = "$env:temp\Install-WMF3Hotfix.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
powershell.exe -ExecutionPolicy ByPass -File $file -Verbose

# Corrigir o erro :
windows01 | UNREACHABLE! => {
    "changed": false,
    "msg": "basic: the specified credentials were rejected by the server",
    "unreachable": true
}

winrm quickconfig -force
Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $true
Set-Item -Path WSMan:\localhost\Service\AllowUnencrypted -Value $true
Restart-Service WinRM


# Kerberos : 

1. Pré-requisitos no Ubuntu

a) Instalar dependências
```

sudo apt update
sudo apt install -y python3-venv python3-dev gcc libkrb5-dev krb5-user
```


b) Criar ambiente virtual (recomendado)

```
python3 -m venv ~/.venvs/ansible-kerberos
source ~/.venvs/ansible-kerberos/bin/activate
```

c) Instalar o Ansible e pacotes necessários

```
pip install ansible pywinrm[kerberos]
```

# Erro  :

<192.168.1.240> ESTABLISH WINRM CONNECTION FOR USER: administrator@RAFAELMELLONH.COM.BR on PORT 5985 TO 192.168.1.240
windows01 | UNREACHABLE! => {
    "changed": false,
    "msg": "kerberos: authGSSClientStep() failed: (('Unspecified GSS failure.  Minor code may provide more information', 851968), ('Server not found in Kerberos database', -1765328377))",
    "unreachable": true
}

