import "./styles.css";

const POLL_MS = 4000;
const root = document.querySelector("[data-info]");
const initial = JSON.parse(root.dataset.info);
let uptime = initial.uptime_seconds;

function formatUptime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return h ? `${h}h ${m}m` : m ? `${m}m ${s}s` : `${s}s`;
}

function formatAgo(iso) {
  const seconds = Math.max(0, Math.round((Date.now() - Date.parse(iso)) / 1000));
  if (seconds < 60) return "just now";
  if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} h ago`;
  return `${Math.floor(seconds / 86400)} d ago`;
}

function setField(name, value) {
  for (const el of document.querySelectorAll(`[data-field="${name}"]`)) {
    el.textContent = value;
  }
}

function render(info) {
  setField("slot", info.slot);
  setField("hostname", info.hostname);
  setField("pid", info.pid);
  document.body.dataset.slot = info.slot;
  if (initial.build.built_at) setField("built-at", formatAgo(initial.build.built_at));
  if (info.build.commit !== initial.build.commit) {
    document.body.classList.add("has-new-release");
    document.querySelector(".release-banner").hidden = false;
    setField("new-commit", info.build.commit.slice(0, 7));
  }
}

async function poll() {
  try {
    const response = await fetch("/api/info", { cache: "no-store" });
    const info = await response.json();
    uptime = info.uptime_seconds;
    render(info);
    document.body.classList.remove("is-offline");
  } catch {
    document.body.classList.add("is-offline");
  }
}

setInterval(() => setField("uptime", formatUptime(++uptime)), 1000);
setInterval(poll, POLL_MS);
setField("uptime", formatUptime(uptime));
render(initial);
