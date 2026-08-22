## 1. System Requirements

### Host Machine:
- **Operating System:** Windows 10 / 11 (Pro, Enterprise, Education) or Windows Server 2016+
- **Virtualization:** Hardware virtualization (VT-x / AMD-V) enabled in BIOS/UEFI
- **Hypervisor:** **Microsoft Hyper-V** role installed
- **Runtime Environment:** **Python 3.10+** (with `venv` module) or **PowerShell 5.1 / 7+**
- **Permissions:** Run as Administrator (or membership in the `Hyper-V Administrators` group)

### Guest Virtual Machine (Sandbox VM):
- **VM OS:** Windows 10 / 11 or Windows Server
- **Integration Services:** **`Guest Service Interface`** component enabled
- **Interpreter:** Windows PowerShell 5.1 / PowerShell 7+

### 1. Copying Files to the System Drive
1. Open Command Prompt or PowerShell:
```powershell
git clone https://github.com/your-username/mcp-server-antigravity-hyperv
.git
cd mcp-server-antigravity-hyperv
```
2. Create the folder **`C:\MCP-HyperV`**.
```powershell
New-Item -ItemType Directory -Path "C:\MCP-HyperV" -Force
```
3. Copy the contents of the unzipped archive to `C:\MCP-HyperV\` so that the structure looks as follows:
```powershell
Copy-Item -Path ".\*" -Destination "C:\MCP-HyperV\" -Recurse -Force
```
### 2. Creating a Virtual Environment (.venv)
```powershell
cd C:\MCP-Hyper-V
python -m venv .venv
```
By default, PowerShell script execution is disabled in Windows (`ExecutionPolicy Restricted`).
To allow virtual environment activation for the current user, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

.\.venv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python test_local.py
```
### 3. Antigravity 2.0 Configuration Setup (mcp_config.json and SKILL.md)

To give the Antigravity 2.0 AI agent access to the sandbox tools:

### Adding the Server to `mcp_config.json`
Open or create the configuration file in your home directory:
* **File path:** `%USERPROFILE%\.gemini\config\mcp_config.json` (e.g., `C:\Users\John\.gemini\config\mcp_config.json`).
* **Insert the following section:**
```json
{
  "mcpServers": {
    "hyperv-sandbox": {
      "command": "C:/MCP-HyperV/.venv/Scripts/python.exe",
      "args": [
        "C:/MCP-HyperV/server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```
**Installing the Agent Skill**
Copy the skill folder `skills/hyperv-sandbox-testing` to one of the locations where Antigravity reads customizations:

* **Option A — Globally for all projects (Recommended):**  
  Copy to the directory:  
  `%USERPROFILE%\.gemini\antigravity\skills\hyperv-sandbox-testing\SKILL.md`

* **Option B — Locally for a specific repository/project:**  
  Place in the root of your working project:  
  `your-project\.agents\skills\hyperv-sandbox-testing\SKILL.md`

* **Copy MCP toll dir MCP:**
  Copy dir MCP fro MCP to `%USERPROFILE%\.gemini\antigravity\` (e.g., `C:\Users\John\.gemini\antigravity\`)

## 5. Hyper-V Virtual Machine Setup

To ensure safe script testing by the agent, the guest VM requires **Integration Services** and a **clean snapshot**:

1. **Enable Integration Services on the VM (Run as Administrator):**
   ```powershell
   Enable-VMIntegrationService -VMName "Win11-Test" -Name "Guest Service Interface"
   ```
2. **Create a baseline checkpoint (CleanBase):**
   ```powershell
   Checkpoint-VM -Name "Win11-Test" -SnapshotName "CleanBase"
   ```
