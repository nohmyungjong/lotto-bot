import requests
import json
from datetime import datetime

ACCESS_TOKEN = "Lrlp4zZ7kVPxYEdXDDbVuJQqcFmYV2KmAAAAAQoNGVMAAAGYHcT_bqbXH4eeWQ3B"

# 최근 당첨 번호 가져오기
def get_latest_lotto_numbers():
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="
    drwNo = None
    latest = requests.get("https://www.dhlottery.co.kr/gameResult.do?method=byWin")
    if "turn" in latest.text:
        import re
        m = re.search(r"<strong>(\d+)</strong>", latest.text)
        if m:
            drwNo = m.group(1)
    if drwNo:
        response = requests.get(url + drwNo)
        data = response.json()
        if data["returnValue"] == "success":
            return set([data[f"drwtNo{i}"] for i in range(1, 7)])
    return set()

# 저장된 추천 번호 불러오기
try:
    with open("lotto_sets.txt", "r") as f:
        lines = f.readlines()
    recommended_sets = [set(map(int, line.strip().split(','))) for line in lines]
except FileNotFoundError:
    recommended_sets = []

# 비교 메시지 작성
winning_numbers = get_latest_lotto_numbers()
message = "[로또 결과 안내]\n\n"
message += f"당첨 번호: {sorted(winning_numbers)}\n\n"

for idx, rec_set in enumerate(recommended_sets, start=1):
    matched = rec_set & winning_numbers
    message += f"{idx}세트: {sorted(rec_set)} → {len(matched)}개 일치 ({sorted(matched)})\n"

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
    "button_title": "결과 확인"
}
data = {
    "template_object": json.dumps(template_object)
}
response = requests.post(url, headers=headers, data=data)

# 로그 기록
with open("lotto_log.txt", "a", encoding="utf-8") as f:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"[{now}] 결과 전송 응답: {response.status_code}, 결과: {response.text}\n")
