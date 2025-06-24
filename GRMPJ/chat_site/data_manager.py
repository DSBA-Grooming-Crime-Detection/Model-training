import os
import json

BASE_PATH = "./data"

# -------------------- 메시지 관리 --------------------
def get_message_file(room_id):
    os.makedirs(os.path.join(BASE_PATH, room_id), exist_ok=True)
    return os.path.join(BASE_PATH, room_id, "messages.json")

def save_message(room_id, speaker, text):
    """메시지 1개를 저장 (발화자와 텍스트만 저장)"""
    path = get_message_file(room_id)
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    data.append({"speaker": speaker, "text": text})

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_messages(room_id, n=None):
    """room_id에 해당하는 대화 메시지를 불러온다. n이 주어지면 최근 n개만 반환."""
    path = get_message_file(room_id)

    if not os.path.exists(path):
        return []

    with open(path, encoding='utf-8') as f:
        messages = json.load(f)

    return messages[-n:] if n else messages

# -------------------- 위험도 관리 --------------------
def get_risk_file(room_id):
    os.makedirs(os.path.join(BASE_PATH, room_id), exist_ok=True)
    return os.path.join(BASE_PATH, room_id, "risks.json")

def save_risk(room_id, score):
    """위험도 1개를 저장"""
    path = get_risk_file(room_id)
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    data.append(score)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_risks(room_id, n=None):
    """최근 n개의 위험도 점수 불러오기 (없으면 전체)"""
    path = get_risk_file(room_id)
    if not os.path.exists(path):
        return []

    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    return data[-n:] if n else data

# -------------------- 유저 이름 관리 --------------------
def get_user_file(room_id):
    os.makedirs(os.path.join(BASE_PATH, room_id), exist_ok=True)
    return os.path.join(BASE_PATH, room_id, "user.json")

def save_user_name(room_id, user_name):
    path = get_user_file(room_id)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"user_name": user_name}, f, ensure_ascii=False)

def load_user_name(room_id):
    path = get_user_file(room_id)
    if not os.path.exists(path):
        return "Unknown"
    with open(path, encoding='utf-8') as f:
        return json.load(f).get("user_name", "Unknown")


# -------------------- 보고서 관리 --------------------
def get_report_file(room_id):
    os.makedirs(os.path.join(BASE_PATH, room_id), exist_ok=True)
    return os.path.join(BASE_PATH, room_id, "report.txt")

def save_report(room_id, report_text):
    path = get_report_file(room_id)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report_text)

def load_report(room_id):
    path = get_report_file(room_id)
    if not os.path.exists(path):
        return ""
    with open(path, encoding='utf-8') as f:
        return f.read()