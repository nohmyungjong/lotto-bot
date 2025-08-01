import requests
import random
import json
from datetime import datetime

# ✔ Access Token
ACCESS_TOKEN = "Lrlp4zZ7kVPxYEdXDDbVuJQqcFmYV2KmAAAAAQoNGVMAAAGYHcT_bqbXH4eeWQ3B"

# ✔ 로또 번호 5세트 생성
def generate_lotto_numbers():
    return sorted(random.sample(range(1, 46), 6))

lotto_sets = [generate_lotto_numbers() for _ in range(5)]

# ✔ 메시지 구성
message = "[이번주 로또 추천 번호]\n\n"
for idx, numbers in enumerate(lotto_sets, start=1):
    message += f"{idx}세트: {numbers}\n"

# ✔ 메시지 전송
url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}
template_object = {
    "object_type": "text",
    "text": message,
    "link": {
        "web_url": "https://www.dhlottery.co.kr",
        "mobile_web_url": "https://www.dhlottery.co.kr"
    },
    "button_title": "로또 확인하기"
}
data = {
    "template_object": json.dumps(template_object)
}

response = requests.post(url, headers=headers, data=data)

# ✔ 추천 번호 저장 (토요일 비교용)
with open("lotto_recommend.json", "w", encoding="utf-8") as f:
    json.dump(lotto_sets, f, ensure_ascii=False, indent=2)

# ✔ 로그 기록
with open("lotto_log.txt", "a", encoding="utf-8") as f:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"[{now}] 추천 번호 전송 응답 코드: {response.status_code}, 결과: {response.text}\n")
