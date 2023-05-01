
import socket
import requests
import re
import random
import json
import string

from typing import Dict

class BardError(Exception):
    pass



class BardChat:
    def __init__(self, session_id:str, url:str="https://bard.google.com/"):
        self.url:str = url
        headers: Dict[str, str] = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": url,
            "Referer": url,
        }
        self._reqid: int = int("".join(random.choices(string.digits, k=4)))
        self.conversation_id: str = ""
        self.response_id: str = ""
        self.choice_id: str = ""
        self.session: requests.Session = requests.Session()
        self.session.headers: Dict[str, str] = headers
        self.session.cookies.set("__Secure-1PSID", session_id)
        self.SNlM0e: str = self.get_snlm0e()

    def get_snlm0e(self) -> str:
        resp: requests.Response = self.session.get(url=self.url, timeout=10)
        # Find "SNlM0e":"<ID>"
        if resp.status_code != 200:
            raise BardError("Could not get Google Bard")
        SNlM0e: str = re.search(r"SNlM0e\":\"(.*?)\"", resp.text).group(1)
        return SNlM0e

    def ask(self, prompt: str) -> dict:
        params: Dict[str, str] = {
            "bl": "boq_assistant-bard-web-server_20230419.00_p1",
            "_reqid": str(self._reqid),
            "rt": "c",
        }

        message_struct = [
            [prompt],
            None,
            [self.conversation_id, self.response_id, self.choice_id],
        ]
        data: Dict[str, str] = {
            "f.req": json.dumps([None, json.dumps(message_struct)]),
            "at": self.SNlM0e,
        }

        resp: requests.Response = self.session.post(
            f"{self.url}/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
            params=params,
            data=data,
            timeout=120,
        )

        chat_data: str = json.loads(resp.content.splitlines()[3])[0][2]
        if not chat_data:
            raise BardError(f"Google Bard encountered an error: {resp.content}")
        json_chat_data = json.loads(chat_data)
        results: Dict[str, str] = {
            "content": json_chat_data[0][0],
            "conversation_id": json_chat_data[1][0],
            "response_id": json_chat_data[1][1],
            "factualityQueries": json_chat_data[3],
            "textQuery": json_chat_data[2][0] if json_chat_data[2] is not None else "",
            "choices": [{"id": i[0], "content": i[1]} for i in json_chat_data[4]],
        }
        self.conversation_id: str = results["conversation_id"]
        self.response_id: str = results["response_id"]
        self.choice_id: str = results["choices"][0]["id"]
        self._reqid += 100000
        return results