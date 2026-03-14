
# Configurar suporte a Windows no Ansible (Linux Control Node)

Este procedimento prepara o Linux para gerenciar servidores Windows via **WinRM** usando Ansible.

## 1. Atualizar repositórios

```bash
sudo apt update
```

## 2. Instalar pip para Python 3

```bash
sudo apt install python3-pip -y
```

Verificar instalação:

```bash
pip3 --version
```

---

## 3. Instalar biblioteca WinRM necessária para Ansible

O Ansible utiliza a biblioteca **pywinrm** para comunicação com Windows.

```bash
pip3 install pywinrm
```

Ou instalar com suporte adicional (recomendado):

```bash
pip3 install "pywinrm[credssp]"
```

---

## 4. Verificar se a biblioteca foi instalada

```bash
python3 -m pip list | grep winrm
```

Saída esperada:

```
pywinrm
requests-ntlm
```

---

## 5. Testar conexão com um host Windows

Executar:

```bash
ansible windows -i inventory -m ansible.windows.win_ping
```

Saída esperada:

```
vm-windows01 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

---

## Resumo das dependências instaladas

| Componente | Função |
|---|---|
Python3 | Linguagem usada pelo Ansible |
pip3 | Gerenciador de pacotes Python |
pywinrm | Comunicação com Windows via WinRM |
requests-ntlm | Autenticação NTLM |

---

## Arquitetura

```
Linux (Control Node)
│
├─ Ansible
├─ Python
├─ pip
└─ pywinrm
      │
      │ WinRM (porta 5985)
      ▼
Windows Server
```

### O projeto Ansible fornece um script oficial para configurar WinRM automaticamente.
```
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1'))
```
Esse script:
* configura WinRM
* cria listeners
* ajusta firewall
* ativa autenticação necessária


###Exemplo
```
[windows]
win01 ansible_host=192.168.1.50

[windows:vars]
ansible_user=rafael
ansible_password="abc,123"
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_port=5985
ansible_winrm_server_cert_validation=ignore
```


### Portas
* HTTP : 5985
* HTTPS: 5986

# OBS
* Use NTLM e nao BASIC para computadores fora do dominio e no dominio use Kerberos

Set-Item -Path WSMan:\localhost\Client\Auth\Basic -Value $true
Set-Item -Path WSMan:\localhost\Client\Auth\NTLM -Value $true



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
```
<192.168.1.240> ESTABLISH WINRM CONNECTION FOR USER: administrator@RAFAELMELLONH.COM.BR on PORT 5985 TO 192.168.1.240
windows01 | UNREACHABLE! => {
    "changed": false,
    "msg": "kerberos: authGSSClientStep() failed: (('Unspecified GSS failure.  Minor code may provide more information', 851968), ('Server not found in Kerberos database', -1765328377))",
    "unreachable": true
}
```

* corrigir : 
```
setspn -Q HTTP/windows01.rafaelmellonh.com.br
setspn -S HTTP/windows01.rafaelmellonh.com.br administrator
```

