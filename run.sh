# Set base URL for local vLLM server
export OPENAI_API_BASE="http://localhost:8000/v1"
export OPENAI_API_KEY="EMPTY"

# python run.py \
#   --agent-strategy tool-calling \
#   --env retail \
#   --model Qwen/Qwen3-8B \
#   --model-provider openai \
#   --start-index 0 \
#   --end-index 5 \
#   --user-model Qwen/Qwen3-8B \
#   --user-model-provider openai \
#   --user-strategy llm \
#   --max-concurrency 1


  python run.py \
  --task-split think \
  --env retail \
  --model Qwen/Qwen3-8B \
  --model-provider openai \
  --start-index 0 \
  --end-index 1 \
  --user-model Qwen/Qwen3-8B \
  --user-model-provider openai \
  --user-strategy llm \
  --max-concurrency 1