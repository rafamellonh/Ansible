### Azure             https://www.youtube.com/watch?v=mH_5yx33_kU

* Instalar Azure CLI
* Criar aruivo azure_rm.yaml

```

plugin: azure_rm
auth_source: auto
include_vm_resource_groups:
  - ansible-inventory-test-rg



```


### VmWAre

* Instalar : ansible-galaxy collection install community.vmware e pip install pyvmomi
* Criar aruivo vmware_rm.yaml

```

plugin: community.vmware.vmware_vm_inventory

hostname: esxi.exemplo.local      # ou IP
username: root
password: sua_senha_segura
validate_certs: false

with_tags: true
hostnames:
  - config.name

groups:
  vm_folders: true
  vm_guest_id: true
```

ansible-inventory -i inventory/myazure_rm.yml --graph
