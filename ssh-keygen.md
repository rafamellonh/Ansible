## SSH Key
```
ssh-keygen -t rsa -b 2048 -f ~/.ssh/ansible
ssh-copy-id -i ~/.ssh/ansible.pub usuario@servidor


```

```
Generating public/private rsa key pair.
Enter file in which to save the key (/home/rafael/.ssh/id_rsa): ansilbe
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in ansilbe
Your public key has been saved in ansilbe.pub
The key fingerprint is:
SHA256:8wRrs6Bl+3QaNjODlnXfHC/Zob9FNO4OQk0sgGB0oqY rafael@VM-ANSIBLE
The key's randomart image is:
+---[RSA 2048]----+
|    .=....       |
|    o o.  . .    |
|   o    .  . o ..|
|  o      o  + ...|
| E    + S o. ..o.|
|     + B B.. oo*.|
|    . = X o..o=.+|
|     . + O  . +..|
|        o      +.|
+----[SHA256]-----+
```

```
cat .ssh/authorized_keys ansilbe.pub 
```

* Copy to remote server 
```
ssh-copy-id -i ~/.ssh/ansible.pub usuario@servidor
```

ou 

```
scp ~/.ssh/ansible.pub usuario@servidor:~/
```


* add to authorized_keys
```
cat ~/ansible.pub >> ~/.ssh/authorized_keys
```

ou

```
ssh -i ~/.ssh/ansible usuario@servidor
```

* Configure ~/.ssh/config

Host servidor
    HostName IP_DO_SERVIDOR
    User usuario
    IdentityFile ~/.ssh/ansible
