# Atualiza a lista de pacotes do Ubuntu
sudo apt update

# Instala o pip3 (gerenciador de pacotes Python)
sudo apt install python3-pip -y

# Confere a versão do pip instalado
pip3 --version

# Instala o módulo para criar ambientes virtuais (venv)
sudo apt install -y python3-venv

# Cria um ambiente virtual chamado venv-ansible na sua HOME
python3 -m venv ~/venv-ansible

# Ativa o ambiente virtual (de agora em diante pip/python ficam isolados)
source ~/venv-ansible/bin/activate

# Executa seu script de instalação (provavelmente instala Ansible e libs do Azure)
# Esse script precisa estar no mesmo diretório, por isso o "./"
./install-ansible-azure.sh

# Lista coleções do Ansible instaladas e filtra por "azure" (para confirmar instalação da azure.azcollection)
ansible-galaxy collection list | grep azure

# Testa se os pacotes do SDK Azure para Python estão funcionando no venv
python -c "import azure.identity, azure.mgmt.resource; print('Azure SDK OK')"

# Instala a CLI oficial do Azure no Ubuntu (fora do venv, via APT)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
