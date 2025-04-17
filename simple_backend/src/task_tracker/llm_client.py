import requests

class LLMClient:
    def __init__(self, api_key: str, account_id: str):
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct-fast"
        self.headers = {"Authorization": f"Bearer {self.api_key}",
                       "Content-Type": "application/json"}
        
    def ask(self, task_text: str) -> str|None:
        payload = {
            "messages": [
                        {"role": "system", "content": "Отвечай кратко в виде списка пунктов"}, 
                        {"role": "user", "content": f"Объясни, как решить задачу: {task_text}"}
                        ]
                    }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("result", {}).get("response")
        except Exception as e:
            print(f"[LLMClient Error] Ошибка при обращении к LLM: {e}")
            return None
