import asyncio
import json
from typing import Annotated
from pydantic import Field
from mcp.server import MCPServer

server = MCPServer("Hyper-V Manager")

def decode_output(b: bytes) -> str:
    for enc in ("utf-8", "cp1251", "cp866"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("utf-8", errors="replace")

async def run_ps(command: str) -> dict | list | str:
    """Выполняет команду PowerShell и возвращает результат в JSON или тексте."""
    full_cmd = f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {command} | ConvertTo-Json -Depth 3"
    proc = await asyncio.create_subprocess_exec(
        "powershell.exe", "-NoProfile", "-NonInteractive", "-Command", full_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    
    if proc.returncode != 0:
        err = decode_output(stderr).strip()
        raise RuntimeError(f"PowerShell Error: {err}")
    
    output = decode_output(stdout).strip()
    if not output:
        return ""
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return output

@server.tool(
    name="get_vms_list",
    description="Получить список всех виртуальных машин, их состояние (Running/Off), память и uptime."
)
async def get_vms_list() -> str:
    data = await run_ps("Get-VM | Select-Object Name, State, CPUUsage, MemoryAssigned, Uptime")
    if isinstance(data, (dict, list)):
        return json.dumps(data, indent=2, ensure_ascii=False)
    return str(data)

@server.tool(
    name="start_virtual_machine",
    description="Запустить виртуальную машину по имени (например, 'Win10')."
)
async def start_virtual_machine(
    vm_name: Annotated[str, Field(description="Имя виртуальной машины")]
) -> str:
    await run_ps(f"Start-VM -Name '{vm_name}'")
    return f"ВМ '{vm_name}' успешно запущена."

@server.tool(
    name="stop_virtual_machine",
    description="Остановить (выключить) виртуальную машину."
)
async def stop_virtual_machine(
    vm_name: Annotated[str, Field(description="Имя виртуальной машины")],
    force: Annotated[bool, Field(description="Принудительно выключить (-TurnOff)")] = False
) -> str:
    flag = "-TurnOff" if force else "-Save"
    await run_ps(f"Stop-VM -Name '{vm_name}' {flag}")
    return f"ВМ '{vm_name}' остановлена."

@server.tool(
    name="revert_to_clean_snapshot",
    description="Откатить ВМ к базовому чекпоинту для запуска тестов с чистого листа."
)
async def revert_to_clean_snapshot(
    vm_name: Annotated[str, Field(description="Имя виртуальной машины")],
    snapshot_name: Annotated[str, Field(description="Имя чекпоинта")] = "CleanBase"
) -> str:
    await run_ps(f"Restore-VMCheckpoint -Name '{snapshot_name}' -VMName '{vm_name}' -Confirm:$false")
    return f"ВМ '{vm_name}' откачена к чекпоинту '{snapshot_name}'."

@server.tool(
    name="copy_file_to_vm",
    description="Скопировать файл с хоста внутрь виртуальной машины через Guest Integration Services."
)
async def copy_file_to_vm(
    vm_name: Annotated[str, Field(description="Имя ВМ")],
    source_path: Annotated[str, Field(description="Абсолютный путь к файлу на хосте")],
    destination_path: Annotated[str, Field(description="Путь назначения внутри ВМ (например, C:\\test.py)")]
) -> str:
    cmd = f"Copy-VMFile -VMName '{vm_name}' -SourcePath '{source_path}' -DestinationPath '{destination_path}' -CreateFullPath -FileSource Host"
    await run_ps(cmd)
    return f"Файл '{source_path}' успешно скопирован в '{destination_path}' на ВМ '{vm_name}'."

@server.tool(
    name="run_command_in_guest",
    description="Запустить команду или PowerShell-скрипт внутри гостевой ОС (PowerShell Direct)."
)
async def run_command_in_guest(
    vm_name: Annotated[str, Field(description="Имя ВМ")],
    command: Annotated[str, Field(description="Команда для выполнения внутри ВМ (например, python C:\\test.py)")],
    username: Annotated[str | None, Field(description="Имя пользователя гостевой ОС (опционально)")] = None,
    password: Annotated[str | None, Field(description="Пароль пользователя гостевой ОС (опционально)")] = None
) -> str:
    if username and password is not None:
        ps_cmd = (
            f"$sec = ConvertTo-SecureString '{password}' -AsPlainText -Force; "
            f"$cred = New-Object System.Management.Automation.PSCredential('{username}', $sec); "
            f"Invoke-Command -VMName '{vm_name}' -Credential $cred -ScriptBlock {{ {command} }}"
        )
    else:
        ps_cmd = f"Invoke-Command -VMName '{vm_name}' -ScriptBlock {{ {command} }}"
    data = await run_ps(ps_cmd)
    if isinstance(data, (dict, list)):
        return json.dumps(data, indent=2, ensure_ascii=False)
    return str(data) if data else "Команда выполнена успешно (без вывода)."

async def main():
    await server.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())