<#
.SYNOPSIS
  One-click startup script for Pune Water Network AI (Backend + Frontend).
#>

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Starting Pune Water Network AI Platform..." -ForegroundColor Cyan

# 1. Start FastAPI Backend in a new PowerShell window
$BackendCmd = "Set-Location '$Root\backend'; Write-Host 'Starting FastAPI Backend on http://localhost:8000 ...' -ForegroundColor Green; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $BackendCmd

# 2. Start Vite Frontend in a new PowerShell window
$FrontendCmd = "Set-Location '$Root\frontend'; Write-Host 'Starting React/Vite Frontend on http://localhost:5173 ...' -ForegroundColor Blue; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $FrontendCmd

Write-Host ""
Write-Host "Launched both servers in separate windows!" -ForegroundColor Green
Write-Host "  -> Backend API & Swagger Docs : http://localhost:8000/docs"
Write-Host "  -> Frontend Operations UI     : http://localhost:5173"

