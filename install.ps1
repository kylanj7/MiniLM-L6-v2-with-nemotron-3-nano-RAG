winget install Ollama.Ollama

ollama pull tinyllama:latest

ollama pull embeddinggemma:latest

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

python -m venv service_rag_env

. .\\.service_rag_env\\Scripts\\Activate.ps1

pip install -r requirements.txt

ollama list
