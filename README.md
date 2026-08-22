# 🚀 Hyper-V Sandbox MCP Server for Antigravity 2.0

<p align="center">
  <img src="https://img.shields.io/badge/Protocol-Model%20Context%20Protocol-blue.svg?style=for-the-badge&logo=anthropic" alt="MCP Protocol" />
  <img src="https://img.shields.io/badge/Agent-Antigravity%202.0-8E75FF.svg?style=for-the-badge&logo=google" alt="Antigravity 2.0" />
  <img src="https://img.shields.io/badge/Deploy%20Path-C%3A%5CMCP--Hyper--V-0078D7.svg?style=for-the-badge&logo=windows" alt="Path C:\MCP-Hyper-V" />
  <img src="https://img.shields.io/badge/Python-.venv%203.10+-3776AB.svg?style=for-the-badge&logo=python" alt="Python .venv" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License MIT" />
</p>

> **Secure agentic sandbox for autonomous testing, validation, and debugging of PowerShell, CMD/BAT scripts, and system utilities inside isolated Hyper-V virtual machines.**
>
> **Hyper-V Sandbox MCP Server** is a Model Context Protocol (MCP) server that turns your local Microsoft Hyper-V hypervisor into an AI-agent-managed testing ground for code. The agent (Antigravity 2.0, Claude Desktop, etc.) gains the ability to autonomously revert VMs to clean snapshots, transfer files out-of-band via VMBus, execute commands inside the guest OS using PowerShell Direct, analyze output, and self-correct on errors (Self-Healing Loop).
>
> - 🌟 Key Features
> - 🛡️ 100% Host Protection (Zero-Risk Sandbox): Potentially destructive scripts (system service modifications, registry edits, network adapter changes, file deletions) execute strictly inside an isolated virtual machine.
> - ⚡ PowerShell Direct (Zero-Network Dependency): Guest OS management operates via the hypervisor's internal VMBus. No network setup, open RDP/SSH/WinRM ports, or firewall tweaks required.
> - 🔄 Deterministic Rollback (CleanBase Checkpoint): Instant VM resets to a clean baseline snapshot before every run ensure fully reproducible tests without leftover state.
> - 📦 Seamless File Transfer (Guest Integration Services): Native Copy-VMFile usage to transfer scripts, libraries, and utilities (e.g., PsExec) directly from host to guest.
> - 🤖 Self-Healing Code Loop: The agent captures real ExitCode, stdout, and stderr outputs alongside exception stack traces to autonomously patch code and re-test until green.
