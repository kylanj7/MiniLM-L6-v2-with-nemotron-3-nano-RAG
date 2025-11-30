  GNU nano 6.2                                                       install.sh *                                                               
VENV_DIR="rag_env"
PROGRAM_NAME="ollama"
MODEL_TINYLLAMA="tinyllama:1.1b"
MODEL_NOMIC="nomic-embed-text"

# ---Make Python env & install requirements---
echo "Creating Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi

echo "Activating virtual environment and installing requirements..."
source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Python requirements installed."
else
    echo "Warning: requirements.txt file not found."
fi

# ---Function Definition for ---
check_and_install_model() {
    local model_name=$1
    echo "Checking for model: $model_name"
    
    if ollama list | grep -q "^$model_name\s"; then
        echo "$model_name is already installed."
    else
        echo "$model_name is not installed. Pulling now..."
        ollama pull "$model_name"
    fi
    echo "---"
}

# ---Check for and Install Ollama executable---
if command -v "$PROGRAM_NAME" &>/dev/null; then
  echo "$PROGRAM_NAME is already installed."
else
  echo "$PROGRAM_NAME is not installed. Running installation script..."
  # Execute the installation command directly
  curl -fsSL ollama.ai | sh
fi

# ---Check for and Install Models---

check_and_install_model "$MODEL_TINYLLAMA"
check_and_install_model "$MODEL_NOMIC"

echo "Assuming there are no errors, INSTALLATION COMPLETE!"
