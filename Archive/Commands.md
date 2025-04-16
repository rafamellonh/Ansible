## Commands

ansible localhost -m ping
ansible all -i '192.168.1.210,' -m ping
ansible all -i '192.168.1.210,192.168.1.178,' -m ping

ansible all -i '192.168.1.210,' -m apt -a "name=python state=latest update_cache=yes"
ansible all -i '192.168.1.210,' -m apt -a "name=python3 state=latest update_cache=yes" -b --ask-become-pass

ansible all -i hosts --list-hosts

ansible web -i hosts -m ping

ansible all -i hosts -m copy -a "src=/ansible/arquivo.txt dest=/home/rafael/arquivo.txt"

ansible all -i hosts -m apt -a "name=nginx update_cache=yes"
ansible all -i hosts -m apt -a "name=nginx update_cache=yes" -b --ask-become-pass

ansible all -i hosts -m apt -a "name=nginx state=absent" -b --ask-become-pass
ansible all -i hosts -m apt -a "name=nginx state=present" -b --ask-become-pass

ansible all -i hosts -m service -a "name=nginx state=stopped" -b --ask-become-pass

ansible all -i hosts -m copy -a "src=index.nginx-debian.html dest=/var/www/html/index.nginx-debian.html" -b --ask-become-pass

ansible-playbook -i hosts playbook

ansible all -i hosts.win -m ansible.windows.win_shell -a "Get-ExecutionPolicy -List"