import json
from openai import OpenAI

# api_base = "http://80.251.213.24:9001/v1"
api_base = "http://localhost:9001/v1"
api_key = "EMPTY"  # vLLM 默认不使用 API key，或设置 VLLM_API_KEY 后此处与之匹配

client = OpenAI(api_key=api_key, base_url=api_base)

resp = client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好，请告诉我人工智能的未来发展方向。"}
    ],
    temperature=0.6,
    max_tokens=2048,
    timeout=20,
    extra_body={"top_k": 40}
)

print("resp", resp)
print(json.dumps(resp.dict(), indent=2, ensure_ascii=False))
