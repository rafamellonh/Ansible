### Comandos 

```
ansible -i hosts all -u rafael -m ping
ansible -i hosts all -a "ls /etc"
ansible -i hosts all -m shell -a "/sbin/reboot" -b
ansible -i hosts all -m apt -a "update_cache=yes" -b
ansible -i hosts all -m apt -a "name=net-tools state=absent" -b
ansible -i hosts all -m systemd -a "name=ssh state=restarted" -b
ansible -i hosts all -m setup -a "filter=ansible_default_ipv4"
ansible -i hosts grupo01 -m setup -a "filter=ansible_default_ipv4"
ansible ubuntu01 -m debug -a var=http_port

ansible-playbook -i inventory/hosts playbooks/1_UpdateLinux.yml -b
ansible-playbook -i inventory/hosts playbooks/1_UpdateLinux.yml -b --syntax-check
ansible-playbook -i inventory/hosts playbooks/1_UpdateLinux.yml -b --list-hosts
ansible-playbook -i inventory/hosts playbooks/1_UpdateLinux.yml -b --list-tasks
ansible-playbook -i inventory/hosts playbooks/1_UpdateLinux.yml -b --tag update
ansible-vault encrypt passwd.yml
ansible-vault view passwd.yml 
ansible-playbook -i inventory/hosts playbooks/18_AnsibleVault.yml -b --ask-vault-password

```