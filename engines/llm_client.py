#!/usr/bin/env python3
"""
OMC Resilient LLM Client with Autonomous Loop, Exponential Backoff & Failover
Tự động phục hồi lỗi kết nối, xử lý Rate-Limit (429/503) bằng thuật toán Exponential Backoff + Jitter,
và tự động nhảy sang model dự phòng (Failover Chain) để đảm bảo hệ thống không bao giờ tắc nghẽn.
"""

import os
import sys
import json
import time
import random
import urllib.request
import urllib.error
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "gateway" / "model_config.json"
ENV_FILE = BASE_DIR / "config" / ".env"

def load_env_var(name: str, default: str = "") -> str:
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(f"{name}="):
                    return line.strip().split(f"{name}=", 1)[1].strip().strip("\"'")
    return os.environ.get(name, default)

class ResilientLLMClient:
    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        self.config = self._load_config()
        self.failover_chain = self.config.get("failover_chain", [
            "openrouter/free",
            "openrouter/nousresearch/hermes-3-llama-3.1-70b",
            "deepseek/deepseek-chat",
            "google/gemini-2.5-flash"
        ])

    def _load_config(self) -> dict:
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _get_provider_details(self, model_spec: str):
        """Phân tích model_spec để lấy baseUrl và apiKey thích hợp"""
        openrouter_key = load_env_var("OPENROUTER_API_KEY")
        deepseek_key = load_env_var("DEEPSEEK_API_KEY")
        gemini_key = load_env_var("GEMINI_API_KEY")
        hhtech_key = load_env_var("HHTECH_API_KEY")

        if model_spec.startswith("openrouter/") or model_spec == "openrouter/free":
            clean_model = model_spec.replace("openrouter/", "") if model_spec != "openrouter/free" else "openrouter/free"
            return {
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "key": openrouter_key,
                "model": clean_model,
                "provider": "openrouter"
            }
        elif model_spec.startswith("deepseek/"):
            return {
                "url": "https://api.deepseek.com/chat/completions",
                "key": deepseek_key,
                "model": model_spec.replace("deepseek/", ""),
                "provider": "deepseek"
            }
        elif model_spec.startswith("omniroute/"):
            return {
                "url": "https://hhtechapi.com/v1/chat/completions",
                "key": hhtech_key,
                "model": model_spec.replace("omniroute/", ""),
                "provider": "omniroute"
            }
        elif model_spec.startswith("google/"):
            return {
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "key": openrouter_key,
                "model": model_spec,
                "provider": "openrouter"
            }
        else:
            return {
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "key": openrouter_key,
                "model": model_spec,
                "provider": "openrouter"
            }

    def chat_completion(self, messages: list, preferred_model: str = None, max_retries: int = 3, temperature: float = 0.2) -> dict:
        """
        Gọi API chat completion với vòng lặp tự phục hồi:
        1. Thử model ưu tiên (hoặc model đầu tiên trong chuỗi failover).
        2. Nếu gặp lỗi 429 (Rate Limit) hoặc 503: Áp dụng Exponential Backoff + Jitter và thử lại.
        3. Nếu hết số lần retry: Tự động nhảy sang model tiếp theo trong failover chain.
        """
        chain = list(self.failover_chain)
        if preferred_model and preferred_model in chain:
            chain.remove(preferred_model)
            chain.insert(0, preferred_model)
        elif preferred_model:
            chain.insert(0, preferred_model)

        last_error = None

        for model_target in chain:
            provider = self._get_provider_details(model_target)
            if not provider["key"]:
                continue

            for attempt in range(max_retries):
                try:
                    payload = {
                        "model": provider["model"],
                        "messages": messages,
                        "temperature": temperature
                    }
                    data = json.dumps(payload).encode("utf-8")
                    req = urllib.request.Request(
                        provider["url"],
                        data=data,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {provider['key']}",
                            "HTTP-Referer": "https://github.com/tano2026/omc-fullstack-kit",
                            "X-Title": "OMC Fullstack Autonomous Engine"
                        }
                    )

                    with urllib.request.urlopen(req, timeout=30) as resp:
                        res_json = json.loads(resp.read().decode("utf-8"))
                        content = res_json["choices"][0]["message"]["content"]
                        return {
                            "status": "success",
                            "model_used": model_target,
                            "content": content,
                            "attempt": attempt + 1
                        }

                except urllib.error.HTTPError as e:
                    last_error = f"HTTP {e.code}: {e.reason}"
                    if e.code in (429, 503, 504):
                        # Áp dụng Exponential Backoff + Jitter
                        delay = (2 ** attempt) + random.uniform(0.5, 1.5)
                        print(f"⚠️ [Rate Limit / Server Busy {e.code}] trên '{model_target}'. Đang chờ {delay:.2f}s để thử lại (Attempt {attempt+1}/{max_retries})...")
                        time.sleep(delay)
                    else:
                        print(f"❌ Lỗi HTTP không thể retry trên '{model_target}': {last_error}")
                        break # Chuyển ngay sang model tiếp theo

                except Exception as e:
                    last_error = str(e)
                    delay = 1.0 * (attempt + 1)
                    time.sleep(delay)

            print(f"🔄 Chuyển sang model dự phòng tiếp theo trong chuỗi sau khi '{model_target}' không phản hồi.")

        return {
            "status": "error",
            "message": f"Toàn bộ chuỗi Failover đều thất bại. Lỗi cuối cùng: {last_error}"
        }

if __name__ == "__main__":
    client = ResilientLLMClient()
    test_msgs = [{"role": "user", "content": "Xin chào! Bạn là ai?"}]
    print("Testing Resilient LLM Loop...")
    res = client.chat_completion(test_msgs)
    print(res)
