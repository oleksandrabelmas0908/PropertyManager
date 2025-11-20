#!/bin/sh
set -e

echo "🟡 Starting Ollama server..."
/bin/ollama serve &
pid=$!

# Pause for Ollama to start and become ready
echo "⏳ Waiting for Ollama to initialize..."
sleep 5

# Check if model already exists
if ollama list | grep -q "^phi3\b"; then
  echo "✅ PHI3 model already present, skipping pull"
else
  echo "🔴 Pulling PHI3 model (this may take several minutes)..."
  echo "📊 Progress will be shown below:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  # Pull with full output visible (no redirection)
  ollama pull phi3
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🟢 PHI3 model downloaded successfully!"
fi

echo "✅ Ollama is ready and serving on port 11434"

# Keep the server running
wait $pid
