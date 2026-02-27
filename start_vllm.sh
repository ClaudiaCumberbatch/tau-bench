vllm serve Qwen/Qwen3-8B \
    --host 0.0.0.0  \
    --port 8000  \
    --dtype float16  \
    --tensor-parallel-size 4  \
    --gpu-memory-utilization 0.85  \
    --max-model-len 8192  \
    --enable-auto-tool-choice  \
    --tool-call-parser hermes \
    --enforce-eager