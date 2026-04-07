# create-vms-hv

An Ansible role that creates and configures Hyper-V VMs from a parent disk.

The main project documentation is available in [`../README.md`](../README.md).

## Summary

This role:

- creates the VM directory;
- creates a differencing disk based on `parent_disk`;
- creates the VM;
- applies CPU, memory, and integration service settings;
- starts the VM;
- waits for the IP address;
- writes the result to `inventory-created.ini`.

## Important

- The parent disk must exist before execution.
- The parent disk should already be updated.
- For Linux VMs, install the following packages in the system that will be used as the base image:

```bash
sudo apt update
sudo apt install linux-tools-$(uname -r) linux-cloud-tools-$(uname -r)
sudo reboot
```

Without these packages, Hyper-V IP discovery may fail.
