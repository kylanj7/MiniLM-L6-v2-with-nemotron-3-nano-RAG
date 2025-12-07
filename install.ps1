Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
$PROGRAM = Get-Command ollama -ErrorAction SilentlyContinue
$PIP_INSTALL = "$env:TEMP\get-pip.py"
$PACKAGE_ENV = "service_agent_wrag_env"
$MODEL_LLM = "tinyllama:latest"
$MODEL_EMBEDDING = "embeddinggemma:latest"

### INSTALL OLLAMA 
if ($PROGRAM) {
    Write-Host "Ollama is already installed at: $($PROGRAM.Source)" -ForegroundColor Green
} else {
    Write-Host "Ollama is not installed. Installing now..." -ForegroundColor Yellow
    winget install Ollama.Ollama
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Ollama installed successfully!" -ForegroundColor Green
        # Refresh PATH after installation
        Write-Host "Refreshing PATH..." -ForegroundColor Yellow
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    } else {
        Write-Host "Installation failed" -ForegroundColor Red
        exit 1
    }
}

### CHECK FOR LLM
Start-Sleep -Seconds 2
$modelCheck = ollama list 2>$null | Select-String "tinyllama"
if ($modelCheck) {
    Write-Host "TinyLlama is already installed" -ForegroundColor Blue
} else {
    Write-Host "TinyLlama is not installed... Pulling now..." -ForegroundColor Yellow
    ollama pull $MODEL_LLM
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "TinyLlama pulled successfully!" -ForegroundColor Green
    } else {
        Write-Host "Pull failed" -ForegroundColor Red
    }
}

### CHECK FOR EMBEDDING MODEL
$modelCheck = ollama list | Select-String "embeddinggemma"
if ($modelCheck) {
    Write-Host "EmbeddingGemma is already installed" -ForegroundColor Blue
} else {
    Write-Host "EmbeddingGemma is not installed... Pulling now..." -ForegroundColor Yellow
    ollama pull $MODEL_EMBEDDING
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "EmbeddingGemma pulled successfully!" -ForegroundColor Green
    } else {
        Write-Host "Pull failed" -ForegroundColor Red
    }
}

### CHECK FOR AND INSTALL PIP 
if (Get-Command pip -ErrorAction SilentlyContinue) {
    Write-Host "pip is already installed" -ForegroundColor Green
    pip --version
} else {
    Write-Host "pip not found. Installing pip..." -ForegroundColor Yellow
    $pipInstaller = "$env:TEMP\get-pip.py"
    wget https://bootstrap.pypa.io/get-pip.py -OutFile $pipInstaller
    python $pipInstaller
    if (Get-Command pip -ErrorAction SilentlyContinue) {
        Write-Host "pip installed successfully!" -ForegroundColor Green
        pip --version
    } else {
        Write-Host "pip installation failed" -ForegroundColor Red
    }
    Remove-Item $pipInstaller
}

### CHECK FOR & ACTIVATE VIRTUAL ENVIRONMENT

if (Test-Path env:VIRTUAL_ENV) {
    Write-Host "Virtual environment is already active: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    if (Test-Path $PACKAGE_ENV) {
        Write-Host "Virtual environment exists. Activating..." -ForegroundColor Yellow
        & ".\$PACKAGE_ENV\Scripts\Activate.ps1"
    } else {
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        python -m venv $PACKAGE_ENV
        Write-Host "Activating virtual environment..." -ForegroundColor Yellow
        & ".\$PACKAGE_ENV\Scripts\Activate.ps1"
    }
}
