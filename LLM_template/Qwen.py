import requests

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": "What opportunities and challenges will the Chinese large model industry face in 2025?"
        }
    ]
}
headers = {
    "Authorization": "Bearer sk-knjpxszkelmrrnhhrmkylfbysuvuakodfekvukwumoptzlsh",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)