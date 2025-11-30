VENV_DIR="rag_env"
PROGRAM_NAME="ollama"
MODEL_TINYLLAMA="tinyllama:1.1b"
MODEL_NOMIC="nomic-embed-text"

sudo apt update
sudo apt install python3.10-venv
sudo apt install curl

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

# ---Install ollama---
if command -v "$PROGRAM_NAME" &>/dev/null; then
  echo "$PROGRAM_NAME is already installed."
else
  echo "$PROGRAM_NAME is not installed. Running installation script..."
  curl -fsSL https://ollama.ai/install.sh | sh
fi

# --- Inline Check for MODEL_TINYLLAMA ---
echo "Checking for model: $MODEL_TINYLLAMA"
if ollama list | grep -q "^$MODEL_TINYLLAMA\s"; then
    echo "$MODEL_TINYLLAMA is already installed."
else
    echo "$MODEL_TINYLLAMA is not installed. Pulling now..."
    ollama pull "$MODEL_TINYLLAMA"
fi
echo "---"

# --- Inline Check for MODEL_NOMIC ---
echo "Checking for model: $MODEL_NOMIC"
if ollama list | grep -q "^$MODEL_NOMIC\s"; then
    echo "$MODEL_NOMIC is already installed."
else
    echo "$MODEL_NOMIC is not installed. Pulling now..."
    ollama pull "$MODEL_NOMIC"
fi
echo "---"

echo "INSTALLATION COMPLETE!"

ollama list
