import requests
import random
import json
from datetime import datetime

ACCESS_TOKEN = "Lrlp4zZ7kVPxYEdXDDbVuJQqcFmYV2KmAAAAAQoNGVMAAAGYHcT_bqbXH4eeWQ3B"

def generate_lotto_numbers():
    return sorted(random.sample(range(1, 46), 6))

lotto_sets = [generate_lotto_numbers() for _ in range(5)]

# 파일로 저장 (토요일에 비교용)
with open("lotto_sets.txt", "w") as f:
    for numbers in lotto_sets:
        f.write(",".join(map(str, numbers)) + "\n")

# 메시지 작성
message = "[이번주 로또 추천 번호]\n\n"
for idx, numbers in enumerate(lotto_sets, start=1):
    message += f"{idx}세트: {numbers}\n"

# 카카오톡 전송
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

# 로그 기록
with open("lotto_log.txt", "a", encoding="utf-8") as f:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"[{now}] 추천 전송 응답: {response.status_code}, 결과: {response.text}\n")
