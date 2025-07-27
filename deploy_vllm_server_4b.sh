
export CUDA_VISIBLE_DEVICES=1

vllm serve Qwen/Qwen3-4B \
    --host 0.0.0.0 \
    --port 9002 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 40000 \
    --chat-template ./qwen3_nonthinking.jinja \
    --trust-remote-code
