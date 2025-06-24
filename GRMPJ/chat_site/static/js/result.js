
document.addEventListener("DOMContentLoaded", async () => {
  await drawCharts();
});

async function drawCharts() {
  const donutCtx = document.getElementById("donutChart").getContext("2d");
  const lineCtx = document.getElementById("lineChart").getContext("2d");

  let risks = [];

  try {
    const res = await fetch(`/chatting/recent_risks?room_id=${roomId}&n=5`);
    risks = await res.json();  // [0.2, 0.4, 0.6, 0.1, 0.8] 형식 (0~1)
  } catch (e) {
    console.warn("위험도 불러오기 실패:", e);
    risks = [0.2, 0.4, 0.6, 0.1, 0.8]; // fallback
  }

  const padded = Array.from({ length: 5 - risks.length }, () => 0).concat(risks);
  const latestRisk = risks.at(-1) ?? 0.0;  // 0~1 값 그대로 사용

  new Chart(donutCtx, {
    type: "doughnut",
    data: {
      labels: ["위험", "정상"],
      datasets: [
        {
          data: [latestRisk, 1 - latestRisk],
          backgroundColor: ["#FF5500" , "#e9ecef"]
        }
      ]
    },
    options: {
      cutout: "70%",
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true },
        centerText: {
          display: true,
          text: Math.round(latestRisk * 100) + "%"  // 중앙에만 % 표시
        }
      }
    },
    plugins: [centerTextPlugin]
  });

  new Chart(lineCtx, {
    type: "line",
    data: {
      labels: padded.map((_, i) => `#${5 - i}`),

      datasets: [
        {
          data: padded,
          borderColor: "#FF5500",
          backgroundColor: "#e9ecef",
          borderWidth: 4,
          pointRadius: 5,
        }
      ]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          max: 1,
          ticks: { stepSize: 0.2 }
        },
        x: {
          grid: { display: false }
        }
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
