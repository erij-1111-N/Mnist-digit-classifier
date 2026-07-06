// ── Constants ──────────────────────────────────────────────────────────────
const CANVAS_SIZE = 280;
const CELL = CANVAS_SIZE / 28;

const DIGIT_COLORS = [
  "#00ff88", "#00ccff", "#ff6b6b", "#ffd93d", "#c77dff",
  "#ff9a3c", "#4cc9f0", "#f72585", "#b5e48c", "#90e0ef"
];

// ── State ───────────────────────────────────────────────────────────────────
let isDrawing  = false;
let hasDrawing = false;
let lastPos    = null;

// ── DOM refs ────────────────────────────────────────────────────────────────
const canvas        = document.getElementById("draw-canvas");
const ctx           = canvas.getContext("2d");
const canvasWrapper = document.getElementById("canvas-wrapper");
const btnClear      = document.getElementById("btn-clear");
const btnClassify   = document.getElementById("btn-classify");
const predDisplay   = document.getElementById("prediction-display");
const probSection   = document.getElementById("prob-section");
const topBars       = document.getElementById("top-bars");
const allGrid       = document.getElementById("all-grid");

// ── Canvas init ─────────────────────────────────────────────────────────────
function initCanvas() {
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
}
initCanvas();

// ── Pointer helpers ─────────────────────────────────────────────────────────
function getPos(e) {
  const rect   = canvas.getBoundingClientRect();
  const scaleX = CANVAS_SIZE / rect.width;
  const scaleY = CANVAS_SIZE / rect.height;
  const src    = e.touches ? e.touches[0] : e;
  return {
    x: (src.clientX - rect.left) * scaleX,
    y: (src.clientY - rect.top)  * scaleY,
  };
}

// ── Drawing ──────────────────────────────────────────────────────────────────
function startDraw(e) {
  e.preventDefault();
  isDrawing = true;
  lastPos   = null;
  clearResults();
}

function draw(e) {
  if (!isDrawing) return;
  e.preventDefault();

  const pos = getPos(e);
  ctx.strokeStyle = "#fff";
  ctx.lineWidth   = CELL * 1.6;
  ctx.lineCap     = "round";
  ctx.lineJoin    = "round";

  ctx.beginPath();
  if (lastPos) {
    ctx.moveTo(lastPos.x, lastPos.y);
    ctx.lineTo(pos.x, pos.y);
  } else {
    ctx.moveTo(pos.x, pos.y);
    ctx.lineTo(pos.x + 0.1, pos.y + 0.1);
  }
  ctx.stroke();
  lastPos = pos;

  if (!hasDrawing) {
    hasDrawing = true;
    btnClassify.classList.add("active");
    btnClassify.disabled = false;
  }
}

function stopDraw() {
  isDrawing = false;
  lastPos   = null;
}

// ── Clear ────────────────────────────────────────────────────────────────────
function clearCanvas() {
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
  hasDrawing = false;
  btnClassify.classList.remove("active");
  btnClassify.disabled = true;
  clearResults();
}

function clearResults() {
  predDisplay.innerHTML = `
    <div class="pred-placeholder">
      <span class="pred-blank">_</span>
      <div class="pred-hint">DRAW A DIGIT TO BEGIN</div>
    </div>`;
  probSection.style.display = "none";
}

// ── Classify ─────────────────────────────────────────────────────────────────
async function classify() {
  if (!hasDrawing || btnClassify.disabled) return;

  // Loading state
  predDisplay.innerHTML = `
    <div class="pred-placeholder">
      <span class="pred-loading-char">?</span>
      <div class="pred-loading-text">PROCESSING NEURAL NETWORK...</div>
    </div>`;
  probSection.style.display = "none";
  btnClassify.disabled = true;
  canvasWrapper.classList.add("pulse");

  // Strip data URL prefix → raw base64
  const imageData = canvas.toDataURL("image/png").split(",")[1];

  try {
    const res = await fetch("/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ image: imageData }),
    });

    const result = await res.json();
    if (result.error) throw new Error(result.error);

    renderPrediction(result);
    renderProbabilities(result.probabilities || Array(10).fill(0.1), result.digit);

  } catch (err) {
    predDisplay.innerHTML = `<div class="pred-error">⚠ ${err.message || "Analysis failed. Please try again."}</div>`;
  } finally {
    btnClassify.disabled = false;
    canvasWrapper.classList.remove("pulse");
    setTimeout(() => canvasWrapper.classList.remove("pulse"), 600);
  }
}

// ── Render helpers ────────────────────────────────────────────────────────────
function renderPrediction({ digit, confidence, reasoning }) {
  const color = DIGIT_COLORS[digit];
  predDisplay.innerHTML = `
    <div class="pred-digit" style="color:${color}; text-shadow:0 0 30px ${color}88">${digit}</div>
    <div class="pred-confidence" style="color:${color}aa">${Math.round(confidence * 100)}% CONFIDENCE</div>
    ${reasoning ? `<div class="pred-reasoning">${reasoning}</div>` : ""}
  `;
}

function renderProbabilities(probs, predictedDigit) {
  // Top 5
  const sorted = probs
    .map((p, i) => ({ digit: i, prob: p }))
    .sort((a, b) => b.prob - a.prob)
    .slice(0, 5);

  topBars.innerHTML = sorted.map(({ digit, prob }) => {
    const color = DIGIT_COLORS[digit];
    return `
      <div class="bar-row">
        <div class="bar-labels">
          <span class="bar-digit" style="color:${color}">DIGIT ${digit}</span>
          <span class="bar-pct">${(prob * 100).toFixed(1)}%</span>
        </div>
        <div class="bar-track">
          <div class="bar-fill" style="width:${prob * 100}%; background:linear-gradient(90deg,${color},${color}88); box-shadow:0 0 6px ${color}66"></div>
        </div>
      </div>`;
  }).join("");

  // All classes grid
  allGrid.innerHTML = probs.map((p, i) => {
    const color    = DIGIT_COLORS[i];
    const isActive = i === predictedDigit;
    return `
      <div class="grid-cell ${isActive ? "active" : ""}" style="${isActive ? `border-color:${color}66` : ""}">
        <div class="grid-digit" style="color:${color}">${i}</div>
        <div class="grid-pct">${(p * 100).toFixed(0)}%</div>
      </div>`;
  }).join("");

  probSection.style.display = "block";
}

// ── Event listeners ───────────────────────────────────────────────────────────
canvas.addEventListener("mousedown",  startDraw);
canvas.addEventListener("mousemove",  draw);
canvas.addEventListener("mouseup",    stopDraw);
canvas.addEventListener("mouseleave", stopDraw);

canvas.addEventListener("touchstart", startDraw, { passive: false });
canvas.addEventListener("touchmove",  draw,      { passive: false });
canvas.addEventListener("touchend",   stopDraw);

btnClear.addEventListener("click",    clearCanvas);
btnClassify.addEventListener("click", classify);