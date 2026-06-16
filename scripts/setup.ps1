# Basic Windows setup script for the AKS AI Troubleshooting Agent

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Creating Python virtual environment..."
python -m venv .venv

Write-Host "Activating virtual environment..."
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
. .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete."
Write-Host "Now set your OpenAI API key:"
Write-Host '$env:OPENAI_API_KEY = "paste-your-key-here"'
Write-Host ""
Write-Host "Then run:"
Write-Host 'python .\agent.py "Use the kubectl tool and check the health of my AKS lab"'
