import json
from openai import OpenAI


api_base = "http://localhost:9001/v1"
api_key = "cfplhys-zgyfjch"  # vLLM 默认不使用 API key，或设置 VLLM_API_KEY 后此处与之匹配

client = OpenAI(api_key=api_key, base_url=api_base)


def llm_single_call(prompt):
    try:
        resp = client.chat.completions.create(
            model="Qwen/Qwen3-8B",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=32000,
            extra_body={"top_k": 40},
            timeout=60
        )
    except Exception as e:
        print("exception", e)
        return None
    content = resp.dict()["choices"][0]["message"]["content"]
    if "</think>\n\n" in content:
        content = content.split("</think>\n\n")[1]
    return content



