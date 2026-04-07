# configure-vms

An Ansible role that performs the guest-side configuration after the VM is created on Hyper-V.

The full project flow is documented in [`../README.md`](../README.md). This role assumes the guest is already reachable over SSH.

## What This Role Does

This role runs on the `created_vms` group and:

- imports the hostname configuration task;
- triggers a reboot handler when the hostname changes;
- flushes handlers so the reboot happens before validation;
- reads the current hostname from the guest;
- prints the final hostname in the play output.

## Hostname Source

The desired hostname comes from `inventory_hostname`.

Example:

```ini
[created_vms]
test01 ansible_host=192.168.40.83
```

In this case, the role sets the guest hostname to `test01`.

## Requirements

- The guest must be reachable through SSH.
- The remote user must be able to escalate with `become`.
- Connection variables such as `ansible_user` or SSH key settings must already be available for the hosts in `created_vms`.

## Variables

This role currently does not define custom role variables. It relies on:

- `inventory_hostname` for the target hostname;
- standard Ansible connection variables for SSH access.

## Example Play

```yaml
- name: configure vms
  hosts: created_vms
  pre_tasks:
    - name: wait for ssh
      wait_for_connection:
        delay: 10
        timeout: 100
  roles:
    - role: configure-vms
```

## Notes

- If the hostname is already correct, the reboot handler is not triggered.
- If you need the reboot to happen even when nothing changes, use a normal reboot task instead of relying on a handler.
