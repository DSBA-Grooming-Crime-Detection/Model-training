const chatHist = document.getElementById("chat-hist");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

let donutChart = null;
let barChart = null;

document.addEventListener("DOMContentLoaded", initPage);

async function initPage() {
  try {
    // 한 번에 메시지·위험도 모두 가져오기
    const res   = await fetch(`/chatting/initial?room_id=${roomId}&n_msgs=50&n_risks=5`);
    const data  = await res.json();

    // ① 기존 대화 렌더링
    data.messages.forEach(m => appendMessage(m.speaker, m.text));

    // ② 차트 초기화
    buildCharts(data.risks);     // ← drawCharts 대신
  } catch (e) {
    console.error("초기 데이터 불러오기 실패:", e);
    buildCharts([0.2, 0.4, 0.6, 0.1, 0.8]);   // fallback
  }
}

function buildCharts(risks) {
  const donutCtx = document.getElementById("donutChart").getContext("2d");
  const barCtx   = document.getElementById("barChart").getContext("2d");

  const padded     = Array.from({ length: 5 - risks.length }, () => 0).concat(risks);
  const latestRisk = risks.at(-1) ?? 0.0;

  donutChart = new Chart(donutCtx, {
    type: "doughnut",
    data: {
      labels: ["위험", "정상"],
      datasets: [{
        data: [latestRisk, 1 - latestRisk],
        backgroundColor: ["#FF5500" , "#e9ecef"]
      }]
    },
    options: {
      cutout: "70%",
      plugins: {
        legend:  { display: false },
        tooltip: { enabled: true },
        centerText: { display: true, text: Math.round(latestRisk * 100) + "%" }
      }
    },
    plugins: [centerTextPlugin]
  });

  barChart = new Chart(barCtx, {
    type: "bar",
    data: {
      labels: padded.map((_, i) => `#${5 - i}`),
      datasets: [{
        data: padded,
        backgroundColor: "#FF5500"
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, max: 1, ticks: { stepSize: 0.2 } },
        x: { grid: { display: false } }
      }
    }
  });
}
const centerTextPlugin = {
  id: "centerText",
  beforeDraw(chart) {
    if (!chart.options.plugins.centerText.display) return;
    const { width, height, ctx } = chart;
    const text = chart.options.plugins.centerText.text;
    ctx.save();
    ctx.font = `${(height / 5).toFixed(0)}px sans-serif`;
    ctx.textBaseline = "middle";
    ctx.textAlign = "center";
    ctx.fillStyle = "#333";
    ctx.fillText(text, width / 2, height / 2);
    ctx.restore();
  }
};


async function updateCharts() {
  let risks = [];

  try {
    const res = await fetch(`/chatting/recent_risks?room_id=${roomId}&n=5`);
    risks = await res.json();
  } catch (e) {
    console.warn("위험도 불러오기 실패:", e);
    risks = [0.2, 0.4, 0.6, 0.1, 0.8];
  }

  const padded = Array.from({ length: 5 - risks.length }, () => 0).concat(risks);
  const latestRisk = risks.at(-1) ?? 0.0;

  // 도넛 차트 업데이트
  donutChart.data.datasets[0].data = [latestRisk, 1 - latestRisk];
  donutChart.data.datasets[0].backgroundColor =  ["#FF5500", "#e9ecef"];
  donutChart.options.plugins.centerText.text = Math.round(latestRisk * 100) + "%";
  donutChart.update();

  // 막대 차트 업데이트
  barChart.data.datasets[0].data = padded;
  barChart.data.datasets[0].backgroundColor = "#FF5500";
  barChart.update();
}


chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const userText = userInput.value.trim();
  if (!userText) return;

  setChatEnabled(false);

  appendMessage("user", userText);
  userInput.value = "";

  await fetch("/api/user_message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ room_id: roomId, speaker: "user", text: userText }),
  });

  const userAnalysis = await analyzeRisk();
  console.log("👁 userAnalysis:", userAnalysis);  // 이 줄 추가
  if (userAnalysis?.redirect) {
    window.location.href = userAnalysis.redirect;
    return;
  }

  updateCharts();

  appendMessage("ai", "...");

  const replyRes = await fetch("/api/gpt_reply", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ room_id: roomId }),
  });

  const replyData = await replyRes.json();
  const aiText = replyData.reply || "(응답 없음)";

  removeLastMessage(); // "..." 제거
  appendMessage("ai", aiText);

  const aiAnalysis = await analyzeRisk();
  if (aiAnalysis?.redirect) {
    window.location.href = aiAnalysis.redirect;
    return;
  }

  updateCharts();

  setChatEnabled(true);
});

function appendMessage(speaker, text) {
  const msgWrapper = document.createElement("div");
  msgWrapper.className = `chat-message-wrapper ${speaker}`;

  const bubble = document.createElement("div");
  bubble.className = "chat-bubble";
  bubble.textContent = text;

  msgWrapper.appendChild(bubble);
  chatHist.appendChild(msgWrapper);
  chatHist.scrollTop = chatHist.scrollHeight;
}

function removeLastMessage() {
  const lastWrapper = chatHist.querySelector(".chat-message-wrapper:last-child");
  if (lastWrapper) chatHist.removeChild(lastWrapper);
}

async function analyzeRisk() {
  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ room_id: roomId }),
    });
    return await res.json();
  } catch (e) {
    console.error("위험도 분석 실패:", e);
    return null;
  }
}

function setChatEnabled(enabled) {
  userInput.disabled = !enabled;
  chatForm.querySelector("button").disabled = !enabled;
}

