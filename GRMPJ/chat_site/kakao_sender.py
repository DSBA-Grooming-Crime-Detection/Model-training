import json
import requests

def send_kakao_message(report_text, access_token, room_id):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    
    full_url = f"https://loyal-serval-distinctly.ngrok-free.app/result/{room_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": f"[그루밍 탐지 보고서]\n{report_text}",
            "link": {
                "web_url": full_url,
                "mobile_web_url": full_url
            },
            "button_title": "결과 확인"
        })
    }

    response = requests.post(url, headers=headers, data=payload)
    print("📨 카카오 응답 코드:", response.status_code, flush=True)
    print("📨 카카오 응답 내용:", response.text, flush=True)

    try:
        return response.json()
    except:
        return {"error": "응답 파싱 실패", "raw": response.text}
