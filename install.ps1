### NEEDS DEBUGGING ###

$VENV_DIR = "rag_env"
$PROGRAM_NAME = "ollama"
$MODEL_TINYLLAMA = "tinyllama:1.1b"
$MODEL_NOMIC = "nomic-embed-text"

Write-Host "--- STEP 1: Make Python env & install requirements ---"
Write-Host "Creating Python virtual environment..."

# Check if the virtual env already exists using Test-Path
if (-Not (Test-Path -Path $VENV_DIR -PathType Container)) {
    python3 -m venv $VENV_DIR
} else {
    Write-Host "Virtual environment '$VENV_DIR' already exists."
}

Write-Host "Activating virtual environment and installing requirements..."

$ActivateScript = Join-Path -Path $VENV_DIR -ChildPath "Scripts\Activate.ps1"
if (Test-Path -Path $ActivateScript) {

    . $ActivateScript

    if (Test-Path -Path "requirements.txt") {
        pip install -r requirements.txt
        Write-Host "Python requirements installed."
    } else {
        Write-Host "Warning: requirements.txt file not found."
    }
} else {
    Write-Host "Error: Virtual environment activation script not found."
    exit 1
}

# Function Definition for checking/installing models
function Check-AndInstall-Model {
    param([string]$model_name)

    Write-Host "Checking for model: $model_name"
    
    $modelList = ollama list
    if ($modelList -match "^$model_name\s") {
        Write-Host "$model_name is already installed."
    } else {
        Write-Host "$model_name is not installed. Pulling now..."
        ollama pull "$model_name"
    }
    Write-Host "---"
}

# Check for and Install Ollama executable
Write-Host "--- Checking for Ollama executable ---"

# Use Get-Command to check for the program existence. SilentlyContinue suppresses errors.
if (Get-Command $PROGRAM_NAME -ErrorAction SilentlyContinue) {
  Write-Host "$PROGRAM_NAME is already installed."
} else {
  Write-Host "$PROGRAM_NAME is not installed. Running installation script..."

  Write-Host "Please download and run the Ollama installer for Windows manually from ollama.ai"
  exit 1 # Exit because we can't automatically run the Windows installer via sh pipe
}

# Check for and Install Models
Check-AndInstall-Model $MODEL_TINYLLAMA
Check-AndInstall-Model $MODEL_NOMIC

Write-Host "Setup script finished."
