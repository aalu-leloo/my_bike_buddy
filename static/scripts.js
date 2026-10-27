// ── Elements ──────────────────────────────────────────────────
const form       = document.getElementById("form");
const queryEl    = document.getElementById("query");
const btn        = document.getElementById("btn");
const btnIcon    = document.getElementById("btnIcon");
const btnText    = document.getElementById("btnText");
const loadingBar = document.getElementById("loadingBar");
const result     = document.getElementById("result");
const answerEl   = document.getElementById("answer");
const sourceEl   = document.getElementById("source");
const historyEl  = document.getElementById("history");
const copyBtn    = document.getElementById("copyBtn");
const statusPill = document.getElementById("statusPill");
const statusDot  = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

// ── Connection status ──────────────────────────────────────────
async function checkConnection() {
  try {
    const res = await fetch("/api/history", { signal: AbortSignal.timeout(3000) });
    if (res.ok) setConnected(true);
    else        setConnected(false);
  } catch {
    setConnected(false);
  }
}

function setConnected(ok) {
  statusPill.className = "status-pill " + (ok ? "connected" : "disconnected");
  statusText.textContent = ok ? "Connected" : "Disconnected";
}

checkConnection();
setInterval(checkConnection, 10000);

// ── Ctrl+Enter to submit ───────────────────────────────────────
queryEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
    e.preventDefault();
    form.requestSubmit();
  }
});

// ── Typewriter effect ──────────────────────────────────────────
function typewrite(el, text, speed = 12) {
  el.textContent = "";
  let i = 0;
  const tick = () => {
    if (i < text.length) {
      el.textContent += text[i++];
      setTimeout(tick, speed);
    }
  };
  tick();
}

// ── Form submit ────────────────────────────────────────────────
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  setLoading(true);
  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: queryEl.value }),
    });
    const data = await res.json();

    // Source badge
    const src = data.source || "database";
    sourceEl.textContent = src === "web" ? "🌐 Web Search" : "🗄️ Knowledge Base";
    sourceEl.className = "source-badge " + (src === "web" ? "web" : "database");

    result.hidden = false;
    result.scrollIntoView({ behavior: "smooth", block: "nearest" });
    typewrite(answerEl, data.answer);
    loadHistory();
  } catch (err) {
    result.hidden = false;
    sourceEl.textContent = "❌ Error";
    sourceEl.className = "source-badge";
    answerEl.textContent = "Something went wrong. Please try again.";
  } finally {
    setLoading(false);
  }
});

function setLoading(on) {
  btn.disabled     = on;
  btnIcon.textContent = on ? "⏳" : "🔍";
  btnText.textContent = on ? "Analysing…" : "Diagnose";
  loadingBar.classList.toggle("active", on);
}

// ── Copy button ────────────────────────────────────────────────
copyBtn.addEventListener("click", () => {
  const text = answerEl.textContent;
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    copyBtn.textContent = "✅ Copied!";
    setTimeout(() => (copyBtn.textContent = "📋 Copy"), 2000);
  });
});

// ── History ────────────────────────────────────────────────────
async function loadHistory() {
  try {
    const res  = await fetch("/api/history");
    const rows = await res.json();
    historyEl.innerHTML = "";

    if (!rows.length) {
      historyEl.innerHTML = '<li class="empty-state">No history yet</li>';
      return;
    }

    rows.forEach((r) => {
      const li = document.createElement("li");
      li.textContent = r.query;
      li.title = "Click to view saved answer";
      li.onclick = () => {
        sourceEl.textContent = r.source === "web" ? "🌐 Web Search" : "🗄️ Knowledge Base";
        sourceEl.className   = "source-badge " + (r.source === "web" ? "web" : "database");
        result.hidden = false;
        typewrite(answerEl, r.answer);
        result.scrollIntoView({ behavior: "smooth", block: "nearest" });
      };
      historyEl.appendChild(li);
    });
  } catch {
    // silently ignore history load errors
  }
}

loadHistory();

loadHistory();