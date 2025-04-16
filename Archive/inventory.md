# arquivo hosts, pode ser usado hosts.yaml

[web]
192.168.1.210 ansible_python_interpreter=/usr/bin/python3

[data]
192.168.1.178 ansible_python_interpreter=/usr/bin/python3

[allgroup:children]
web
data