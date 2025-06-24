from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os

from generator import generate_reply
from data_manager import load_messages, load_risks, load_report, save_message, save_risk, save_report
from kakao_sender import send_kakao_message

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")

DETECTION_API_URL = os.environ.get("DETECTION_API_URL", "http://detection:6000/analyze")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not session.get('kakao_access_token'):
            return "<h3>카카오 로그인 후 입장 가능합니다.</h3>", 403

        room_id = request.form['room_id']
        user_name = request.form['user_name']
        session['room_id'] = room_id
        session['user_name'] = user_name
        return redirect(url_for('chat'))

    # GET 요청 시: 로그인 여부에 따라 렌더링
    return render_template('index.html')

@app.route('/kakao/login')
def kakao_login():
    CLIENT_ID = os.environ.get("KAKAO_CLIENT_ID")
    REDIRECT_URI = os.environ.get("KAKAO_REDIRECT_URI")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=talk_message"
    )

@app.route('/kakao/callback')
def kakao_callback():
    code = request.args.get("code")
    CLIENT_ID = os.environ.get("KAKAO_CLIENT_ID")
    REDIRECT_URI = os.environ.get("KAKAO_REDIRECT_URI")

    token_url = "https://kauth.kakao.com/oauth/token"
    res = requests.post(token_url, data={
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": code
    })
    token_json = res.json()
    kakao_access_token = token_json.get("access_token")
    session['kakao_access_token'] = kakao_access_token

    # 사용자 정보 조회
    user_info_res = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {kakao_access_token}"}
    )
    user_info = user_info_res.json()
    session['kakao_user_id'] = user_info.get("id")

    return redirect(url_for('index'))

@app.route('/chat')
def chat():
    room_id = session.get('room_id', '')
    user_name = session.get('user_name', '')
    if not room_id or not user_name:
        return redirect(url_for('index'))
    return render_template('chat.html', room_id=room_id, user_name=user_name)

@app.route('/result/<room_id>')
def result(room_id):
    report = load_report(room_id)
    risks = load_risks(room_id, n=5)
    if not report:
        return "<h2>보고서가 존재하지 않습니다.</h2>", 404

    return render_template("result.html", report=report, room_id=room_id, risks=risks)

@app.route('/api/user_message', methods=['POST'])
def api_user_message():
    data = request.get_json()
    room_id = data.get("room_id")
    text = data.get("text", "").strip()
    save_message(room_id, "user", text)
    return jsonify({"ok": True})

@app.route('/api/gpt_reply', methods=['POST'])
def api_gpt_reply():
    data = request.get_json()
    room_id = data.get("room_id")
    history = load_messages(room_id)
    reply = generate_reply(history)
    save_message(room_id, "ai", reply)
    return jsonify({"reply": reply})

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    room_id = data.get("room_id")
    messages = load_messages(room_id)

    try:
        res = requests.post(DETECTION_API_URL, json={
            "room_id": room_id,
            "messages": messages
        })
        res.raise_for_status()
        result = res.json()

        risk = result.get("risk", 0.0)
        save_risk(room_id, risk)

        if "report" in result:
            save_report(room_id, result["report"])

            kakao_access_token = session.get("kakao_access_token")
            print(f"토큰: {kakao_access_token}", flush=True)

            if kakao_access_token:
                response = send_kakao_message(result["report"], kakao_access_token, room_id)
                print(f"카카오톡 전송 결과: {response}", flush=True)
            else:
                print("카카오 액세스 토큰이 세션에 없습니다.", flush=True)

            print("최종 반환 결과:", {"redirect": f"/result/{room_id}"}, flush=True)
            return jsonify({"redirect": f"/result/{room_id}"})

    except Exception as e:
        print(f"⚠️ 분석 API 오류: {e}")

    return jsonify({"ok": True})

@app.route("/chatting/initial")
def chatting_initial():          #  GET /chatting/initial?room_id=xxx&n_msgs=50&n_risks=5
    room_id   = request.args.get("room_id")
    n_msgs    = request.args.get("n_msgs",  type=int)
    n_risks   = request.args.get("n_risks", type=int)

    if not room_id:
        return jsonify({"error": "room_id is required"}), 400

    try:
        messages = load_messages(room_id, n=n_msgs)
        risks    = load_risks(room_id,   n=n_risks)
        return jsonify({"messages": messages, "risks": risks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chatting/history")
def chatting_history():
    room_id = request.args.get("room_id")
    n = request.args.get("n", type=int)

    if not room_id:
        return jsonify({"error": "room_id is required"}), 400

    try:
        messages = load_messages(room_id, n=n)
        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chatting/recent_risks")
def recent_risks():
    room_id = request.args.get("room_id")
    n = request.args.get("n", type=int)

    if not room_id:
        return jsonify({"error": "room_id is required"}), 400

    try:
        risks = load_risks(room_id, n=n)
        return jsonify(risks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
