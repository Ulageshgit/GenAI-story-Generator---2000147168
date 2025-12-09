const API_BASE = "http://127.0.0.1:8000";

function byName(form, name) {
  return form.querySelector(`[name="${name}"]`);
}

document.getElementById("story-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.currentTarget;

  const prefs = {
    name: byName(form, "name").value.trim(),
    age: parseInt(byName(form, "age").value, 10),
    language: byName(form, "language").value.trim() || "en",
    genre: byName(form, "genre").value.trim() || "adventure",
    tone: byName(form, "tone").value.trim() || "whimsical",
    setting: byName(form, "setting").value.trim() || "fantasy forest",
    characters: (byName(form, "characters").value || "")
      .split(",").map(x => x.trim()).filter(Boolean),
    moral_theme: byName(form, "moral_theme").value.trim() || "kindness and courage",
    reading_level: byName(form, "reading_level").value,
    target_length_words: parseInt(byName(form, "target_length_words").value, 10),
    constraints: byName(form, "constraints").value.trim() || null,
  };

  const req = {
    preferences: prefs,
    temperature: parseFloat(byName(form, "temperature").value || "0.8"),
    max_tokens: parseInt(byName(form, "max_tokens").value || "1200", 10),
    seed: byName(form, "seed").value ? parseInt(byName(form, "seed").value, 10) : null,
  };

  const errorEl = document.getElementById("error");
  const outEl = document.getElementById("output");
  errorEl.classList.add("hidden");
  outEl.classList.add("hidden");

  try {
    const res = await fetch(`${API_BASE}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!res.ok) {
      const det = await res.json();
      throw new Error(det.detail || `HTTP ${res.status}`);
    }
    const data = await res.json();
    renderStory(data);
  } catch (err) {
    errorEl.textContent = `Error: ${err.message}`;
    errorEl.classList.remove("hidden");
  }
});

function renderStory(data) {
  document.getElementById("title").textContent = data.title || "Untitled Story";
  document.getElementById("lang").textContent = data.language || "en";
  document.getElementById("lvl").textContent = data.reading_level || "child";
  document.getElementById("words").textContent = String(data.words || "");

  const outline = document.getElementById("outline");
  outline.innerHTML = "";
  (data.outline || []).forEach(point => {
    const li = document.createElement("li");
    li.textContent = point;
    outline.appendChild(li);
  });

  document.getElementById("story").textContent = data.story || "";
  document.getElementById("moral").textContent = data.moral || "";

  document.getElementById("output").classList.remove("hidden");
}
