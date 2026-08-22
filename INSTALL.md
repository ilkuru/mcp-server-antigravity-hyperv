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

### Copying Files to the System Drive
1.
```powershell
git clone https://github.com/your-username/mcp-server-antigravity-hyperv
.git
2. cd mcp-server-antigravity-hyperv
3. Create the folder **`C:\MCP-HyperV`**.
```powershell
New-Item -ItemType Directory -Path "C:\MCP-HyperV" -Force
4. Copy the contents of the unzipped archive to `C:\MCP-HyperV\` so that the structure looks as follows:
```powershell
Copy-Item -Path ".\*" -Destination "C:\MCP-HyperV\" -Recurse -Force
### **Creating a Virtual Environment (.venv)**
Open Command Prompt or PowerShell:
```cmd
cd C:\MCP-Hyper-V
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install -r requirements.txt
