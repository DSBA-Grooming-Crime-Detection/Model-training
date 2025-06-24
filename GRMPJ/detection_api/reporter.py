from openai import OpenAI
import os

API_KEY = os.environ.get("GROK_API_KEY")
BASE_URL = os.environ.get("GROK_API_BASE_URL")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def generate_report(room_id, messages, risk):
    system_prompt = (
        "[역할]\n"
        "너는 온라인 대화를 분석하는 디지털 범죄 수사관이자 전문가야.\n"
        "사용자의 대화 기록을 바탕으로 그루밍 범죄 가능성을 평가하고, 수사 참고용 보고서를 작성한다.\n"
        "보고서는 간결하면서도 중요한 내용을 요약해야 하고, 위험한 발언은 반드시 인용한다.."
        "작성한 내용에 강조표시는 하지않는다."
    )

    history_prompt = f"[채팅방 ID: {room_id}]\n[위험도: {risk * 100}%]\n[대화 기록]\n"
    for turn in messages:
        role = turn.get("sender") or turn.get("speaker")  # 둘 중 있는 키
        speaker = "사용자" if role == "user" else "상대방"
        history_prompt += f"{speaker}: {turn['text']}\n"

    answer_prompt = (
        "[요청]\n"
        "위의 대화 내용을 분석하여 다음 정보를 포함하는 보고서를 작성해줘:\n"
        "- 대화 요약\n"
        "- 수상한 대화 흐름\n"
        "- 위험 발언 인용\n"
        "- 결론 및 권고사항\n"
    )

    try:
        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": history_prompt},
                {"role": "system", "content": answer_prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"보고서 생성 실패: {e}")
        return "보고서 생성에 실패했습니다."
