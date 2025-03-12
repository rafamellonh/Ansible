## Commands

ansible localhost -m ping
ansible all -i '192.168.1.210,' -m ping
ansible all -i '192.168.1.210,192.168.1.178,' -m ping

ansible all -i '192.168.1.210,' -m apt -a "name=python state=latest update_cache=yes"
ansible all -i '192.168.1.210,' -m apt -a "name=python3 state=latest update_cache=yes" -b --ask-become-pass

ansible all -i hosts --list-hosts

ansible web -i hosts -m ping

ansible all -i hosts -m copy -a "src=/ansible/arquivo.txt dest=/home/rafael/arquivo.txt"