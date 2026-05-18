let currentManifest = null;
let selectedBlueprint = null;

const modalityLabels = {
  llm: "LLM",
  image: "Image",
  audio: "Music",
  video: "Video",
};

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

function setPanel(panelId) {
  document.querySelectorAll(".panel").forEach((panel) => panel.classList.remove("active"));
  document.querySelectorAll(".nav-button").forEach((button) => button.classList.remove("active"));
  document.getElementById(panelId).classList.add("active");
  document.querySelector(`[data-panel="${panelId}"]`).classList.add("active");
}

function updatePreview() {
  if (!currentManifest) return;
  currentManifest.name = document.getElementById("capsule-name").value;
  currentManifest.model.base_model = document.getElementById("base-model").value;
  currentManifest.dataset.path = document.getElementById("dataset-path").value;
  currentManifest.dataset.license = document.getElementById("dataset-license").value;
  currentManifest.resources.gpu_memory_gb = Number(document.getElementById("gpu-memory").value);
  currentManifest.resources.max_training_hours = Number(
    document.getElementById("training-hours").value,
  );
  currentManifest.model.trust_remote_code = document.getElementById("remote-code").checked;
  document.getElementById("manifest-preview").textContent = JSON.stringify(currentManifest, null, 2);
}

function hydrateForm(manifest) {
  document.getElementById("capsule-name").value = manifest.name;
  document.getElementById("base-model").value = manifest.model.base_model;
  document.getElementById("dataset-path").value = manifest.dataset.path;
  document.getElementById("dataset-license").value = manifest.dataset.license;
  document.getElementById("gpu-memory").value = manifest.resources.gpu_memory_gb;
  document.getElementById("training-hours").value = manifest.resources.max_training_hours;
  document.getElementById("remote-code").checked = manifest.model.trust_remote_code;
  updatePreview();
}

async function selectBlueprint(name) {
  selectedBlueprint = name;
  currentManifest = await requestJson(`/v1/blueprints/${name}/manifest`);
  hydrateForm(currentManifest);
  document.querySelectorAll(".blueprint-card").forEach((card) => {
    card.classList.toggle("selected", card.dataset.name === name);
  });
  setPanel("manifest");
}

function renderBlueprints(blueprints) {
  const grid = document.getElementById("blueprint-grid");
  grid.innerHTML = "";
  blueprints.forEach((blueprint) => {
    const card = document.createElement("button");
    card.className = "blueprint-card";
    card.dataset.name = blueprint.name;
    card.innerHTML = `
      <div>
        <span class="tag">${modalityLabels[blueprint.modality] || blueprint.modality}</span>
        <h3>${blueprint.name}</h3>
        <p>${blueprint.description}</p>
      </div>
      <strong>${blueprint.method}</strong>
    `;
    card.addEventListener("click", () => selectBlueprint(blueprint.name));
    grid.appendChild(card);
  });
}

function renderFindings(findings) {
  const target = document.getElementById("security-results");
  if (!findings.length) {
    target.className = "results";
    target.innerHTML = "<strong>No security findings.</strong>";
    return;
  }
  target.className = "results";
  target.innerHTML = findings
    .map(
      (finding) => `
        <div class="finding ${finding.severity}">
          <strong>${finding.severity.toUpperCase()} · ${finding.code}</strong>
          <p>${finding.message}</p>
        </div>
      `,
    )
    .join("");
}

function renderPlan(plan) {
  const target = document.getElementById("plan-results");
  target.className = "results";
  target.innerHTML = `
    <h3>${plan.capsule_name}</h3>
    <p>${plan.modality} · ${plan.method} · ${plan.estimated_gpu_memory_gb}GB GPU · ${plan.estimated_training_hours}h</p>
    ${plan.steps.map((step, index) => `<div class="step"><strong>${index + 1}.</strong> ${step}</div>`).join("")}
    ${plan.warnings.map((warning) => `<div class="finding medium"><strong>WARNING</strong><p>${warning}</p></div>`).join("")}
  `;
}

async function init() {
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.addEventListener("click", () => setPanel(button.dataset.panel));
  });
  document.querySelectorAll("#manifest-form input").forEach((input) => {
    input.addEventListener("input", updatePreview);
  });
  document.getElementById("review-button").addEventListener("click", async () => {
    updatePreview();
    const findings = await requestJson("/v1/security-review", {
      method: "POST",
      body: JSON.stringify(currentManifest),
    });
    renderFindings(findings);
    setPanel("security");
  });
  document.getElementById("plan-button").addEventListener("click", async () => {
    updatePreview();
    const plan = await requestJson("/v1/plan", {
      method: "POST",
      body: JSON.stringify(currentManifest),
    });
    renderPlan(plan);
    setPanel("plan");
  });

  const blueprints = await requestJson("/v1/blueprints");
  renderBlueprints(blueprints);
  await selectBlueprint(blueprints[0].name);
  setPanel("blueprints");
}

init().catch((error) => {
  document.body.innerHTML = `<main class="results"><h1>Startup Error</h1><p>${error.message}</p></main>`;
});

