# AI Desktop Assistant Setup Script for PowerShell
# Run this script to install dependencies and verify setup

Write-Host "=== AI Desktop Assistant Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check pip
Write-Host "Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip found" -ForegroundColor Green
} catch {
    Write-Host "✗ pip not found. Please install pip" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Some dependencies failed to install" -ForegroundColor Red
    Write-Host "You may need to install dependencies manually" -ForegroundColor Yellow
}

# Check for .env file
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file found" -ForegroundColor Green
    
    # Check if GROQ_API_KEY is set
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "GROQ_API_KEY\s*=") {
        if ($envContent -match "GROQ_API_KEY\s*=\s*your_groq_api_key_here") {
            Write-Host "⚠ GROQ_API_KEY needs to be set in .env file" -ForegroundColor Yellow
        } else {
            Write-Host "✓ GROQ_API_KEY appears to be configured" -ForegroundColor Green
        }
    } else {
        Write-Host "⚠ GROQ_API_KEY not found in .env file" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ .env file not found" -ForegroundColor Yellow
    Write-Host "Creating .env.example file..." -ForegroundColor Yellow
    
    # Create .env file template
    @"
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=change_this_to_a_random_secret_key
DEBUG=False
PORT=5000
"@ | Out-File -FilePath ".env" -Encoding UTF8
    
    Write-Host "✓ Created .env file. Please edit it and add your GROQ_API_KEY" -ForegroundColor Green
}

# Test imports
Write-Host ""
Write-Host "Testing module imports..." -ForegroundColor Yellow
$modules = @("groq_agent", "voice_module", "memory_module", "automation_module", "scheduler_module")

foreach ($module in $modules) {
    try {
        python -c "import $module; print('OK')" 2>&1 | Out-Null
        Write-Host "✓ $module" -ForegroundColor Green
    } catch {
        Write-Host "✗ $module - import failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your GROQ_API_KEY from https://console.groq.com/" -ForegroundColor White
Write-Host "2. Run: python app.py" -ForegroundColor White
Write-Host "3. Open http://localhost:5000 in your browser" -ForegroundColor White
Write-Host ""

