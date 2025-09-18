# Guia: Preparar o Ansible para Provisionar Recursos no Azure

Este guia descreve os passos necessários para configurar o Ansible, instalar as dependências do Azure e rodar um playbook de teste para criar um Resource Group no Azure.

---

## 1. Instalar dependências do Python para Azure

Recomendado usar **venv** para isolar o ambiente do Ansible.

# Instalar suporte a venv (se necessário)
sudo apt-get update
sudo apt-get install -y python3-venv

# Criar e ativar o ambiente virtual
python3 -m venv ~/.venvs/ansible-azure
source ~/.venvs/ansible-azure/bin/activate

# Atualizar pip
python -m pip install --upgrade pip

# Instalar a coleção do Azure
ansible-galaxy collection install azure.azcollection

# Instalar pacotes Python necessários
python -m pip install 'ansible[azure]'

# Alternativa mínima (libs essenciais)
python -m pip install azure-identity azure-mgmt-resource msrestazure

---

## 2. Configurar o Ansible para usar o Python correto

### Inventário (recomendado)
[localhost]
localhost ansible_connection=local ansible_python_interpreter=~/.venvs/ansible-azure/bin/python

### Playbook
- hosts: localhost
  connection: local
  vars:
    ansible_python_interpreter: "~/.venvs/ansible-azure/bin/python"

### Configuração global (opcional)
[defaults]
interpreter_python = auto_silent

---

## 3. Autenticação no Azure

### A) Azure CLI (mais simples para desenvolvimento)
az login
az account set --subscription "<SUBSCRIPTION_ID>"

### B) Service Principal (recomendado para automação/CI-CD)
export AZURE_CLIENT_ID="<appId>"
export AZURE_CLIENT_SECRET="<password>"
export AZURE_TENANT="<tenantId>"
export AZURE_SUBSCRIPTION_ID="<subscriptionId>"

---

## 4. Criar playbook de teste (Resource Group)

Arquivo `test-rg.yml`:

---
- name: Testar criação de Resource Group no Azure
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    ansible_python_interpreter: "~/.venvs/ansible-azure/bin/python"

  tasks:
    - name: Garantir que o Resource Group existe (check mode)
      azure.azcollection.azure_rm_resourcegroup:
        name: rg-teste-ansible
        location: canadacentral
      check_mode: yes

# Executar o teste
ansible-playbook test-rg.yml -vv

---

## 5. Estrutura sugerida para o projeto

Projeto-k8s-cluster/
├── provisioning/
│   ├── main.yml                # Playbook principal
│   └── roles/
│       └── create-instances/
│           ├── tasks/
│           │   ├── main.yml
│           │   └── provisioning.yml
│           ├── defaults/
│           │   └── main.yml
│           └── vars/
│               └── main.yml (opcional)
├── hosts                       # Inventário
└── ansible.cfg                 # Configurações do Ansible

---

## 6. Exemplo de Playbook principal

Arquivo `provisioning/main.yml`:

---
- name: Provisionar cluster no Azure
  hosts: localhost
  connection: local
  gather_facts: no
  collections:
    - azure.azcollection

  roles:
    - create-instances

---

## 7. Executar o Playbook

ansible-playbook -i hosts provisioning/main.yml -vv
