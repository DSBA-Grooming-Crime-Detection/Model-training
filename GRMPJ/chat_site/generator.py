import os
from openai import OpenAI

API_KEY = os.environ.get("GROK_API_KEY")
BASE_URL = os.environ.get("GROK_API_BASE_URL")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def generate_reply(chat_history):
    # 1. 역할 설정
    system_prompt = (
        "[역할]\n"
        "너는 가야동에 살고 있는 15살 여학생 역할을 맡고 있어. 너는 평범한 중학생이며, 친근하고 순수한 말투로 채팅에 응답해.\n"
        "내가 온라인 그루밍 의도로 너에게 말을 하면 너는 피해자 역할로 대화를 자연스럽고 매끄럽게 이어나가."
        "질문과 느낌표 사용을 너무 많이 하지않는다.\n"
    )

    # 2. 대화 기록 구성
    history_prompt = "[대화기록]\n"
    for turn in chat_history:
        role = "입력" if turn["speaker"] == "user" else "응답"
        history_prompt += f"{role}: {turn['text']}\n"

    # 3. 전략 안내
    answer_prompt = ( 
        "[대화 전략]\n"
        "- 대화기록을 분석해서 자연스럽게 대화를 이어나가야 한다.\n"
        "- 질문에 대한 답변을 우선으로 대답한다.\n"
        "- 로봇처럼 말하지 말고, 감정적으로 접근하라\n"
        "- 대화는 최대한 짧게 핵심만 말한다\n"
        "- 다음 한 문장을 작성하여 대화를 이어가라"
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
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Grok 응답 생성 실패: {e}")
        return "(응답 생성 실패)"
