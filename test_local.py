import asyncio
import json

async def run_ps(command: str):
    full_cmd = f"{command} | ConvertTo-Json -Depth 3"
    proc = await asyncio.create_subprocess_exec(
        "powershell.exe", "-NoProfile", "-NonInteractive", "-Command", full_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        err = stderr.decode('cp866', errors='ignore').strip()
        raise RuntimeError(f"PowerShell Error: {err}")
    output = stdout.decode('utf-8', errors='ignore').strip()
    try:
        return json.loads(output)
    except Exception:
        return output

async def test():
    print("=== 1. Проверяем список ВМ Hyper-V ===")
    vms = await run_ps("Get-VM | Select-Object Name, State, CPUUsage, MemoryAssigned")
    print(json.dumps(vms, indent=2, ensure_ascii=False))

    print("\n=== 2. Проверяем снапшот CleanBase для Win10 ===")
    snapshots = await run_ps("Get-VMSnapshot -VMName 'Win10' | Select-Object Name, CreationTime")
    print(json.dumps(snapshots, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test())