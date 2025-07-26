
export CUDA_VISIBLE_DEVICES=0

vllm serve Qwen/Qwen3-8B \
    --host 0.0.0.0 \
    --port 9001 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 40000 \
    --chat-template ./qwen3_nonthinking.jinja \
    --trust-remote-code
