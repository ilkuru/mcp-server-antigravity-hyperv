---
name: hyperv-sandbox-testing
description: Standard operating procedure for safely deploying, testing, validating, and debugging PowerShell and CMD scripts inside isolated Hyper-V virtual machines using MCP tools.
---

# Hyper-V Sandbox Testing & Validation Skill

This skill provides step-by-step procedures for the Antigravity Agent to safely test administrative scripts, batch files, PsExec routines, and system automation tools inside an isolated Hyper-V sandbox.

---

## Tool Reference

The following MCP tools are available under the `hyperv` namespace:
- `get_vms_list()`: Discover available virtual machines, their current state (Running / Off), and assigned memory.
- `start_virtual_machine(vm_name)`: Power on a target sandbox VM.
- `stop_virtual_machine(vm_name, force=False)`: Power off or shut down the VM to free host resources.
- `revert_to_clean_snapshot(vm_name, snapshot_name="CleanBase")`: Roll back the VM to a known clean checkpoint before running tests.
- `copy_file_to_vm(vm_name, source_path, destination_path)`: Copy script files and binaries to the guest OS via VMBus / Guest Integration Services without network dependency.
- `run_command_in_guest(vm_name, command)`: Execute PowerShell/CMD commands inside the guest OS via PowerShell Direct and retrieve stdout, stderr, and exit codes.

---

## Standard Workflow

### Step 1: Discover and Verify Sandbox State
1. Call `get_vms_list()` to find the designated test VM (e.g., `Win11-Sandbox` or `Win10-Test`).
2. Verify if the target VM exists.

### Step 2: Environment Reset (Clean Baseline)
> [!IMPORTANT]
> Always revert to the clean snapshot before executing tests to ensure reproducibility and prevent state contamination.
1. Call `revert_to_clean_snapshot(vm_name="<VM_NAME>", snapshot_name="CleanBase")`.
2. Ensure the snapshot rollback completes successfully.

### Step 3: Start the VM
1. If the VM is `Off`, call `start_virtual_machine(vm_name="<VM_NAME>")`.
2. Allow 5-10 seconds for the guest OS OS services to initialize.

### Step 4: Deploy Test Artifacts
1. Ensure the script or artifact is saved locally on the host.
2. Call `copy_file_to_vm(vm_name="<VM_NAME>", source_path="<HOST_PATH>", destination_path="C:\\Test\\<SCRIPT_NAME>")`.

### Step 5: Execute Test inside Guest
1. Call `run_command_in_guest(vm_name="<VM_NAME>", command="powershell.exe -ExecutionPolicy Bypass -File C:\\Test\\<SCRIPT_NAME>")`.
2. Inspect the returned JSON payload:
   - Check `ExitCode` (0 = Success, non-zero = Failure).
   - Check `Output` for exception stack traces, syntax errors, or expected log messages.

### Step 6: Self-Correction Loop (If Errors Occur)
1. If the script fails, analyze `stderr` and exception messages.
2. Refactor the script code on the host.
3. Re-copy the updated script via `copy_file_to_vm`.
4. Re-run via `run_command_in_guest` until all tests pass.

### Step 7: Teardown and Resource Cleanup
1. Once testing and validation are complete, call `stop_virtual_machine(vm_name="<VM_NAME>")` (or keep running if interactive debugging is required).
2. Report final test results and logs to the user.
