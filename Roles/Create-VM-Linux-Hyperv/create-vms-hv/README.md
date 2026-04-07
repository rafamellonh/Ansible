# create-vms-hv

An Ansible role that performs the Hyper-V side of the workflow.

The full project flow is documented in [`../README.md`](../README.md). This role is responsible only for creating the guest and making it available to the next play.

## What This Role Does

This role runs on the `hyperv` group and:

- creates the VM directory;
- creates a differencing disk from `parent_disk`;
- creates the VM;
- applies CPU, memory, and integration service settings;
- starts the VM through a handler;
- queries Hyper-V for the guest IP address;
- writes the result to [`../inventory-created.ini`](../inventory-created.ini);
- adds the new guest to the in-memory `created_vms` group with `add_host`.

## Variables

Variables currently defined in [`vars/main.yml`](vars/main.yml):

- `vm_name`: guest name in Hyper-V and the inventory name later used by `configure-vms`.
- `vm_root`: base directory for VM files on the Hyper-V host.
- `parent_disk`: path to the parent VHDX.
- `vm_disk`: final path to the guest differencing disk.

## Requirements

- The Hyper-V host must be reachable through WinRM.
- The parent disk must already exist.
- A virtual switch named `vswitch` must already exist.
- The guest image should include Hyper-V tools so `Get-VMNetworkAdapter` can expose the IP.

Example packages for Ubuntu-based guest images:

```bash
sudo apt update
sudo apt install linux-tools-$(uname -r) linux-cloud-tools-$(uname -r)
sudo reboot
```

## Output

After a successful run, this role produces two useful outputs:

- a persisted record in [`../inventory-created.ini`](../inventory-created.ini);
- an in-memory Ansible host in the `created_vms` group, which allows the next play to configure the guest in the same `ansible-playbook` execution.
