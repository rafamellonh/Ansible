
### Modo seguro

```
mkdir -p group_vars
vim group_vars/linux.yml  (nome do grupo no inventory tem que ser o nome do vault)

#Adicione isso no arquivo
ansible_become: true
ansible_become_method: sudo
ansible_become_password: "abc,123"

#Criptografar o arquivo com Ansible Vault
ansible-vault encrypt group_vars/linux.yml

#Testar se a variável está sendo carregada
ansible linux -i inventory -m debug -a "var=ansible_become_password" --ask-vault-pass

```
 

### Nao usar em ambiente produtivo
*   Edite o arquivo : 
    ```
    vim /etc/sudoers
    ```

*   Adicionar essa linha : 
    
    ```rafael ALL=(ALL) NOPASSWD: ALL```

*  Ou adicione ao grupo whell e descomente uma linha no arquivo /etc/sudoers

    ``` 
    sudo usermod -aG wheel rafael 
    ```

    ```
    ## Allows people in group wheel to run all commands (comentar)
    #wheel  ALL=(ALL)       ALL


    ## Same thing without a password  (descomentar)
    %wheel        ALL=(ALL)       NOPASSWD: ALL
    ```

### Criar chave SSH
```
ssh-keygen -b 2048 -t rsa -f ansible-key
```

* Copiar a chave publica para os servidores

```
 ssh-copy-id -i ansible-key.pub rafael@192.168.1.180
 ```

 * Valide no servidor remoto se a chave esta no arquivo authorized_keys

 ```
 cat ~/.ssh/authorized_keys
 ```

 * No servidor host edite o arquivo ~/.ssh/config para forcar o uso da chave privada

 ```
 vim ~/.ssh/config 

IdentityFile ~/.ssh/ansible-key
IdentitiesOnly yes

 ```
