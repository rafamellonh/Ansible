# Hyper-V VM Automation with Ansible

This repository automates the full lifecycle of a guest VM on Hyper-V:

1. create the VM from a parent disk;
2. start it and wait for an IP address;
3. register the new guest in inventory;
4. connect to the guest over SSH;
5. configure the guest hostname.

The automation is split into two roles that are orchestrated by [`playbook.yml`](playbook.yml):

- [`create-vms-hv`](create-vms-hv/README.md): creates and boots the VM on the Hyper-V host.
- [`configure-vms`](configure-vms/README.md): connects to the Linux guest and sets its hostname from the inventory name.

## End-to-End Flow

The current playbook runs two plays in sequence:

1. Run [`create-vms-hv`](create-vms-hv/README.md) on the `hyperv` group.
2. Create the VM directory, differencing disk, and VM definition.
3. Configure CPU, memory, and integration services.
4. Start the VM through a handler.
5. Query Hyper-V for the guest IP address.
6. Write the discovered guest to [`inventory-created.ini`](inventory-created.ini).
7. Add the guest to the in-memory Ansible inventory with `add_host`.
8. Run [`configure-vms`](configure-vms/README.md) on the `created_vms` group in the same `ansible-playbook` execution.
9. Wait for SSH connectivity to the guest.
10. Set the Linux hostname to `inventory_hostname`, reboot if needed, and print the resulting hostname.

Because the guest is added with `add_host`, the second play can run immediately after creation without requiring a second command.

## Repository Layout

- [`playbook.yml`](playbook.yml): entry point that chains VM creation and guest configuration.
- [`inventory`](inventory): main inventory used to reach the Hyper-V host.
- [`inventory-created.ini`](inventory-created.ini): generated inventory with created guests and their IPs.
- [`create-vms-hv`](create-vms-hv/README.md): role responsible for Hyper-V-side operations.
- [`configure-vms`](configure-vms/README.md): role responsible for guest-side configuration.

## Prerequisites

Before running the playbook, make sure the following are in place:

- The Hyper-V host is reachable through WinRM.
- A virtual switch named `vswitch` already exists on the Hyper-V host.
- The parent disk defined in [`create-vms-hv/vars/main.yml`](create-vms-hv/vars/main.yml) already exists.
- The parent disk is updated and ready to be cloned as the base image.
- The Linux image used as the parent disk has Hyper-V guest tools installed so Hyper-V can report the VM IP.
- The Linux image allows SSH access for the user you plan to use in the guest.
- The Linux guest user has sudo privileges required for hostname changes and reboot.

Example packages for Ubuntu-based guest images:

```bash
sudo apt update
sudo apt install linux-tools-$(uname -r) linux-cloud-tools-$(uname -r) openssh-server
sudo reboot
```

Without the Hyper-V tools, `Get-VMNetworkAdapter` may not return the guest IP correctly.

## Inventories

This project currently uses two inventory files:

- [`inventory`](inventory): static input inventory used to connect to the Hyper-V host.
- [`inventory-created.ini`](inventory-created.ini): file updated during execution with the guests discovered by Hyper-V.

Example [`inventory`](inventory):

```ini
[hyperv]
192.168.40.76

[hyperv:vars]
ansible_user=Administrator
ansible_password=CHANGE_ME
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_port=5985
ansible_winrm_server_cert_validation=ignore

[created_vms]
```

`inventory-created.ini` is useful as a record of what was created, but the same run does not depend on re-reading that file. The second play works because the first role also adds the guest to the runtime inventory with `add_host`.

## Roles

### `create-vms-hv`

This role runs on the Hyper-V host and is responsible for:

- creating the VM directory;
- creating the differencing disk from `parent_disk`;
- creating the VM;
- applying CPU, memory, and integration-service settings;
- starting the VM;
- discovering the guest IP address;
- recording the guest in [`inventory-created.ini`](inventory-created.ini);
- adding the guest to the in-memory `created_vms` group.

Main variables defined in [`create-vms-hv/vars/main.yml`](create-vms-hv/vars/main.yml):

- `vm_name`: name of the VM to create.
- `vm_root`: base directory for VM files on the Hyper-V host.
- `parent_disk`: path to the parent VHDX used as the source image.
- `vm_disk`: final path of the guest differencing disk.

### `configure-vms`

This role runs on the created guest VM and is responsible for:

- setting the guest hostname to `inventory_hostname`;
- rebooting the guest when the hostname changes;
- checking and printing the resulting hostname.

The role currently does not define custom variables. It relies on:

- `inventory_hostname` as the desired hostname;
- SSH connection variables available to the `created_vms` hosts.

## Playbook

Current [`playbook.yml`](playbook.yml):

```yaml
---
- name: Create Hyper-V VMs
  hosts: hyperv
  gather_facts: false
  roles:
    - role: create-vms-hv
  tags: create-vms

- name: configure vms
  hosts: created_vms
  pre_tasks:
    - name: wait for ssh
      wait_for_connection:
        delay: 10
        timeout: 100
  roles:
    - role: configure-vms
  tags: configure-vms
```

## How to Run

1. Update [`inventory`](inventory) with the Hyper-V connection details.
2. Adjust the VM variables in [`create-vms-hv/vars/main.yml`](create-vms-hv/vars/main.yml).
3. Confirm that the parent disk exists and is ready to be used as a template.
4. Run the full workflow:

```bash
ansible-playbook -i inventory playbook.yml
```

Standalone tag-based runs are also possible, but the inventory must already contain the group targeted by that play:

```bash
ansible-playbook -i inventory playbook.yml --tags create-vms
```

For `configure-vms`, use an inventory that already has the `created_vms` hosts available.

## Important Notes

- If the guest requires explicit SSH parameters such as `ansible_user`, `ansible_ssh_private_key_file`, or `ansible_port`, add them both to the generated line in [`create-vms-hv/tasks/get-ip-and-configure-hosts.yml`](create-vms-hv/tasks/get-ip-and-configure-hosts.yml) and to the `add_host` task in the same file.
- The current IP discovery filter looks for addresses in the `192.168.40.x` range. Update the regular expression in [`create-vms-hv/tasks/get-ip-and-configure-hosts.yml`](create-vms-hv/tasks/get-ip-and-configure-hosts.yml) if your network uses a different range.
- If you clone multiple Linux VMs from the same parent disk, make sure the guest image regenerates its SSH host keys to avoid host key conflicts.
- The current role variables are defined for a single VM. To create multiple guests in one run, the next step would be to change `vm_name` and related variables into a list and loop over them.
