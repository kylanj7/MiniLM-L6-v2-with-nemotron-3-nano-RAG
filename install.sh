#!/bin/bash

# --- Variable Assignments ---
VENV_DIR="rag_env"
PROGRAM_NAME="ollama"
PACKAGE_CURL="curl" 
PACKAGE_PIP="python3-pip"
PACKAGE_VENV="python3.10-venv"
MODEL_TINYLLAMA="tinyllama:latest"
MODEL_GEMMA="embeddinggemma:latest"



# --- System Update ---
sudo apt update



# --- Check and install pip ---
echo "****************Installing Pip****************"
if command -v python3-pip &>/dev/null; then
    echo "pip is is already installed."
else
    echo "pip is not installed. Installing now..."
    sudo apt install -y "$PACKAGE_PIP"
fi



# --- Check and install curl ---
echo "****************Installing Curl****************"
if command -v curl &>/dev/null; then
    echo "curl is already installed."
else
    echo "curl is not installed. Installing now..."
    sudo apt install -y "$PACKAGE_CURL"
fi



# --- Check and install python3.10-venv ---
echo "****************Installing Python3.10-venv****************"
if dpkg -l | grep -q python3.10-venv; then
    echo "python3.10-venv is already installed."
else
    echo "python3.10-venv is not installed. Installing now..."
    sudo apt install -y "$PACKAGE_VENV"
fi



# --- Make Python Environment ---
echo "****************Creating the Python Virtual Environmant****************"
echo "Creating Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment '$VENV_DIR' created."
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi



# --- Activate Virtual Environment ---
echo "****************Activating the Python Virtual Envoronment****************"
source "$VENV_DIR/bin/activate"



# --- PyMuPDF dependency installation ---
echo "****************Installing required system dependencies for PyMuPDF...****************"
sudo apt install -y build-essential python3-dev libopenjp2-7 libpng16-16 libtiff5



# --- Install Requirements ---
echo "****************Installing the Requirments for the Virtual Environment****************"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Python requirements installed."
else
    echo "requirements.txt file not found."
fi



# ---Install Ollama---
echo "****************Installing Ollama****************"
if command -v "$PROGRAM_NAME" &>/dev/null; then
  echo "$PROGRAM_NAME is already installed."
else
  echo "$PROGRAM_NAME is not installed. Running installation script..."
  curl -fsSL https://ollama.ai/install.sh | sh
fi



# --- Inline Check for MODEL_TINYLLAMA ---
echo "****************Pulling TinyLlama1.1b****************"
echo "Checking for model: $MODEL_TINYLLAMA"
if ollama list | grep -q "^$MODEL_TINYLLAMA\s"; then
    echo "$MODEL_TINYLLAMA is already installed."
else
    echo "$MODEL_TINYLLAMA is not installed. Pulling now..."
    ollama pull "$MODEL_TINYLLAMA"
fi
echo "---"



# --- Inline Check for GEMMA_EMBED ---
echo "****************Pulling Gemma Embedded 300m Model****************"
echo "Checking for model: $MODEL_GEMMA"
if ollama list | grep -q "^$MODEL_GEMMA\s"; then
    echo "$MODEL_GEMMA is already installed."
else
    echo "$MODEL_GEMMA is not installed. Pulling now..."
    ollama pull "$MODEL_GEMMA"
fi

ollama list

echo "****************INSTALLATION COMPLETE!****************"
