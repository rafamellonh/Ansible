# Hyper-V VM Automation with Ansible

This repository creates and configures VMs on Hyper-V from a parent disk (`parent_disk`), starts the VM, waits for an IP address, and writes the result to a separate inventory file so it can be used later by other roles or playbooks.

## What This Project Does

The main play in [`playbook.yml`](playbook.yml) runs the [`create-vms-hv`](create-vms-hv) role, which currently follows this flow:

1. Create the VM directory on the Hyper-V host.
2. Check whether the VM disk already exists.
3. Create a differencing child disk from the parent disk.
4. Create the VM in Hyper-V.
5. Configure CPU, memory, and integration services.
6. Start the VM through a handler.
7. Wait for the VM to obtain an IP address.
8. Write the IP to [`inventory-created.ini`](inventory-created.ini).

## Prerequisites

Before running the playbook, make sure the following are in place:

- The Hyper-V host must be reachable through WinRM.
- A `vSwitch` named `vswitch` must already exist on the Hyper-V host.
- The parent disk defined in [`create-vms-hv/vars/main.yml`](create-vms-hv/vars/main.yml) must exist before execution.
- The parent disk must already be updated and ready to be cloned as the base image for new VMs.
- The Linux image used as the parent disk must have the following packages installed so Hyper-V can expose the guest IP address afterward:

```bash
sudo apt update
sudo apt install linux-tools-$(uname -r) linux-cloud-tools-$(uname -r)
sudo reboot
```

Without these packages in the system used to build the parent disk, `Get-VMNetworkAdapter` may not return the VM IP correctly.

## Inventories

This project uses two inventories with different purposes:

- [`inventory.ini`](inventory.ini.example): input inventory used to connect to the Hyper-V host through WinRM. You should create your own `inventory.ini` from this example.
- [`inventory-created.ini`](inventory-created.ini): inventory generated during execution with the created VMs and their IPs. This file can be reused by another role or playbook later.

Example `inventory.ini`:

```ini
[hyperv]
hyperv-host ansible_host=192.168.1.10

[hyperv:vars]
ansible_connection=winrm
ansible_user=Administrator
ansible_password=CHANGE_ME
ansible_port=5986
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
```

## Main Variables

The current variables are defined in [`create-vms-hv/vars/main.yml`](create-vms-hv/vars/main.yml):

- `vm_name`: name of the VM to create.
- `vm_root`: base directory where VMs will be stored on the Hyper-V host.
- `parent_disk`: path to the parent disk used to create the differencing disk.
- `vm_disk`: final path of the VM disk.

## How to Run

1. Create `inventory.ini` with the Hyper-V host connection details.
2. Adjust the variables in [`create-vms-hv/vars/main.yml`](create-vms-hv/vars/main.yml).
3. Confirm that the parent disk already exists and is up to date.
4. Run:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

## How IP Discovery Works

A task in [`create-vms-hv/tasks/get-ip-and-configure-hosts.yml`](create-vms-hv/tasks/get-ip-and-configure-hosts.yml) queries Hyper-V with `Get-VMNetworkAdapter`, looks for an IP in the `192.168.40.x` range, retries until the VM responds, and then writes the entry to `inventory-created.ini`.

If your network uses a different range, update the IP filter in that task.

## Main Structure

- [`playbook.yml`](playbook.yml): entry point for the automation.
- [`create-vms-hv/tasks/create-vm.yml`](create-vms-hv/tasks/create-vm.yml): creates the directory, disk, and VM.
- [`create-vms-hv/tasks/configure-vm.yml`](create-vms-hv/tasks/configure-vm.yml): applies VM settings and schedules the start.
- [`create-vms-hv/tasks/main.yml`](create-vms-hv/tasks/main.yml): organizes task order and forces handler execution before IP discovery.
- [`create-vms-hv/tasks/get-ip-and-configure-hosts.yml`](create-vms-hv/tasks/get-ip-and-configure-hosts.yml): waits for the IP and writes the generated inventory.
- [`create-vms-hv/handlers/main.yml`](create-vms-hv/handlers/main.yml): starts the VM.

## Notes

- The generated inventory currently stores only `name` and `ansible_host`. If the next role also needs `ansible_user`, an SSH key, or other parameters, add them to the format written to `inventory-created.ini`.
- The role is currently set up for a simple flow based on fixed variables in `vars/main.yml`. For multiple VMs, the next step would be to evolve it to a VM list and iterate with `loop`.
