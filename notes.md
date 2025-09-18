sudo mount -t cifs //192.168.40.52/ansible /data/ -o username=rafael,password=#xxxxxxx#,vers=3.0

```
* export ANSIBLE_PYTHON_INTERPRETER=/usr/bin/python3.12

  Ou crie uma variavel no hosts :

  [all:vars]
  ansible_python_interpreter=/usr/bin/python3.12


```
source ~/ansible-azure-env/bin/activate


```
# Coleção do Azure para Ansible
ansible-galaxy collection install azure.azcollection

# Autenticação (uma das opções abaixo)

# Opção A: Azure CLI interativo (mais simples em dev)
az login
# (opcional) escolha a subscription certa
az account set --subscription "<SUBSCRIPTION_ID>"

# Opção B: Service Principal (CI/CD)
export AZURE_CLIENT_ID="<appId>"
export AZURE_CLIENT_SECRET="<password>"
export AZURE_TENANT="<tenantId>"
export AZURE_SUBSCRIPTION_ID="<subscriptionId>"
```