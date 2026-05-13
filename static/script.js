let interval;
let startTime;
let running = false;
let emotionChart;
let reportChart;

const emotionLabels = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"];
let emotionData = new Array(emotionLabels.length).fill(0);

document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("emotionChart").getContext("2d");
  emotionChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: emotionLabels,
      datasets: [{
        label: "Emotion Intensity (%)",
        data: emotionData,
        backgroundColor: [
          "#e53935", "#8e24aa", "#3949ab",
          "#43a047", "#1e88e5", "#fbc02d", "#757575"
        ],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      scales: { x: { min: 0, max: 100 } },
      plugins: { legend: { display: false } }
    }
  });
});

function updateTimer() {
  if (!running) return;
  const elapsed = Math.floor((Date.now() - startTime) / 1000);
  document.getElementById("timer").textContent = `Session Time: ${elapsed}s`;
}

function updateGraph(data) {
  emotionLabels.forEach((label, i) => {
    emotionData[i] = data[label] || 0;
  });
  emotionChart.data.datasets[0].data = emotionData;
  emotionChart.update();
}

async function startCamera() {
  await fetch("/start");
  running = true;
  startTime = Date.now();
  interval = setInterval(async () => {
    const res = await fetch("/analyze");
    const data = await res.json();
    updateGraph(data);
    updateTimer();
  }, 2000);
}

async function stopCamera() {
  await fetch("/stop");
  running = false;
  clearInterval(interval);
}

async function showReport() {
  const res = await fetch("/report");
  const data = await res.json();
  if (!data.average) {
    alert("No data recorded yet!");
    return;
  }

  document.getElementById("reportDuration").textContent =
    `Session Duration: ${data.duration}s`;

  const ctx = document.getElementById("reportChart").getContext("2d");
  if (reportChart) reportChart.destroy();
  reportChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: Object.keys(data.average),
      datasets: [{
        data: Object.values(data.average),
        backgroundColor: [
          "#ef5350", "#ab47bc", "#5c6bc0",
          "#66bb6a", "#42a5f5", "#ffca28", "#9e9e9e"
        ]
      }]
    },
    options: {
      plugins: {
        legend: { position: 'bottom' },
        title: { display: true, text: 'Average Emotion Distribution' }
      }
    }
  });

  document.getElementById("reportModal").style.display = "block";
}

function closeReport() {
  document.getElementById("reportModal").style.display = "none";
}
