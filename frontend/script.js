const AppState = {
  IDLE: "idle",
  RUNNING: "running",
  FINISHED: "finished",
};

const state = {
  status: AppState.IDLE,
  imageCount: 6,
  images: [],
};

const baseUrl = "localhost:8000";

/** @type {HTMLButtonElement | null} */
const startBtn = /** @type {HTMLButtonElement} */ (
  document.getElementById("startBtn")
);
const cancelBtn = /** @type {HTMLButtonElement} */ (
  document.getElementById("cancelBtn")
);
const refreshBtn = document.getElementById("refreshBtn");
const statusLabel = document.getElementById("statusLabel");
const statusMessage = document.getElementById("statusMessage");
const loader = document.getElementById("loader");
const gallery = document.getElementById("gallery");
const modal = document.getElementById("modal");
const modalImage = /** @type {HTMLImageElement} */ (
  document.getElementById("modalImage")
);
const closeModalBtn = document.getElementById("closeModalBtn");

// API functions
const useFetch = async (url, params) => {
  try {
    const response = await fetch(url, params);

    console.log("response", response);

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const res = await response.json();
    return res;
  } catch (e) {
    console.log("API error: " + e);
    return;
  }
};

const getImages = async () => {
  const res = await useFetch("/api/photos", {
    method: "GET",
  });

  console.log("res", res);

  if (!res) return;

  const images = res.photos.map((img, index) => {
    return {
      id: index + 1,
      label: img,
      src: `/static/photos/${img}`,
    };
  });

  state.imageCount = images.length;
  state.images = images;
};

const startCapture = async () => {
  await useFetch("/api/capture/start", {
    method: "POST",
  });
};

const cancelCapture = async () => {
  await useFetch("/api/capture/cancel", {
    method: "POST",
  });
};

// for test
function renderGallery() {
  gallery.innerHTML = "";

  if (!state.images.length) {
    const empty = document.createElement("p");
    empty.className = "hint";
    empty.textContent = "Nenhuma imagem disponível no momento.";
    gallery.appendChild(empty);
    return;
  }

  state.images.forEach((image) => {
    const fig = document.createElement("figure");
    fig.className = "card";

    const img = document.createElement("img");
    img.src = image.src;
    img.alt = image.label;
    img.loading = "lazy";

    const caption = document.createElement("figcaption");
    caption.textContent = image.label;

    fig.appendChild(img);
    fig.appendChild(caption);
    fig.addEventListener("click", () => openModal(image));
    gallery.appendChild(fig);
  });
}

function setUiByState() {
  statusLabel.classList.remove("idle", "running", "finished");

  if (state.status === AppState.IDLE) {
    statusLabel.textContent = "Parado";
    statusLabel.classList.add("idle");
    statusMessage.textContent = "Sistema pronto.";
    startBtn.disabled = false;
    // cancelBtn.disabled = true;
    loader.classList.add("hidden");
  }

  if (state.status === AppState.RUNNING) {
    statusLabel.textContent = "Em execução";
    statusLabel.classList.add("running");
    statusMessage.textContent = "Digitalizando...";
    startBtn.disabled = true;
    // cancelBtn.disabled = false;
    loader.classList.remove("hidden");
  }

  if (state.status === AppState.FINISHED) {
    statusLabel.textContent = "Finalizado";
    statusLabel.classList.add("finished");
    statusMessage.textContent = "Processo finalizado.";
    startBtn.disabled = false;
    // cancelBtn.disabled = true;
    loader.classList.add("hidden");
  }
}

function startScan() {
  if (state.status === AppState.RUNNING) {
    return;
  }

  startCapture();
}

function cancelScan() {
  // if (state.status !== AppState.RUNNING) {
  //   return;
  // }

  cancelCapture();
}

async function refreshGallery() {
  await getImages();
  renderGallery();

  if (state.status === AppState.FINISHED) {
    state.status = AppState.IDLE;
    setUiByState();
  }
}

function openModal(image) {
  modalImage.src = image.src;
  modalImage.alt = image.label;
  modal.classList.remove("hidden");
  modal.setAttribute("aria-hidden", "false");
}

function closeModal() {
  modal.classList.add("hidden");
  modal.setAttribute("aria-hidden", "true");
  modalImage.src = "";
}

startBtn.addEventListener("click", startScan);
cancelBtn.addEventListener("click", cancelScan);
refreshBtn.addEventListener("click", refreshGallery);
closeModalBtn.addEventListener("click", closeModal);
modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !modal.classList.contains("hidden")) {
    closeModal();
  }
});

refreshGallery();
setUiByState();

// State change
function handleServerStateChange(newState) {
  // Se o estado for o mesmo, não faz nada
  if (state.status === newState) return;

  state.status = newState;

  if (newState === AppState.RUNNING) {
    // Se o servidor manda rodar, limpamos timers antigos e iniciamos a UI
    setUiByState();
    // Opcional: Iniciar o timer de capturas local ou esperar o servidor mandar as fotos?
  } else if (newState === AppState.FINISHED || newState === AppState.IDLE) {
    setUiByState();
  }
}

// Websocket
const socket = new WebSocket(`ws://${baseUrl}/ws`);

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type != "status") return;

  const newState = data.value;

  // Validar se o estado recebido existe no seu objeto AppState
  if (Object.values(AppState).includes(newState)) {
    handleServerStateChange(newState);
  }
};

socket.onerror = (error) => {
  console.error("Erro no WebSocket:", error);
};

const requestStatus = async () => {
  socket.send(
    JSON.stringify({
      type: "get_status",
    }),
  );
};
