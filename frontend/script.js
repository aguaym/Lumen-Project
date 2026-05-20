const AppState = {
  IDLE: 'idle',
  RUNNING: 'running',
  FINISHED: 'finished'
};

const state = {
  status: AppState.IDLE,
  runTimer: null,
  autoImageTimer: null,
  imageCount: 6,
  images: []
};

const startBtn = document.getElementById('startBtn');
const cancelBtn = document.getElementById('cancelBtn');
const refreshBtn = document.getElementById('refreshBtn');
const statusLabel = document.getElementById('statusLabel');
const statusMessage = document.getElementById('statusMessage');
const loader = document.getElementById('loader');
const gallery = document.getElementById('gallery');
const modal = document.getElementById('modal');
const modalImage = document.getElementById('modalImage');
const closeModalBtn = document.getElementById('closeModalBtn');

function nowTime() {
  const d = new Date();
  return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function createMockImage(id = null) {
  const nextId = id ?? state.imageCount + 1;
  const stamp = Date.now();

  return {
    id: nextId,
    label: `Captura #${nextId} - ${nowTime()}`,
    src: `https://picsum.photos/seed/negativo-${nextId}-${stamp}/640/480`
  };
}

function seedGallery() {
  for (let i = 1; i <= state.imageCount; i += 1) {
    state.images.push(createMockImage(i));
  }
}

function renderGallery() {
  gallery.innerHTML = '';

  if (!state.images.length) {
    const empty = document.createElement('p');
    empty.className = 'hint';
    empty.textContent = 'Nenhuma imagem disponível no momento.';
    gallery.appendChild(empty);
    return;
  }

  state.images.forEach((image) => {
    const fig = document.createElement('figure');
    fig.className = 'card';

    const img = document.createElement('img');
    img.src = image.src;
    img.alt = image.label;
    img.loading = 'lazy';

    const caption = document.createElement('figcaption');
    caption.textContent = image.label;

    fig.appendChild(img);
    fig.appendChild(caption);
    fig.addEventListener('click', () => openModal(image));
    gallery.appendChild(fig);
  });
}

function setUiByState() {
  statusLabel.classList.remove('idle', 'running', 'finished');

  if (state.status === AppState.IDLE) {
    statusLabel.textContent = 'Parado';
    statusLabel.classList.add('idle');
    statusMessage.textContent = 'Sistema pronto.';
    startBtn.disabled = false;
    cancelBtn.disabled = true;
    loader.classList.add('hidden');
  }

  if (state.status === AppState.RUNNING) {
    statusLabel.textContent = 'Em execução';
    statusLabel.classList.add('running');
    statusMessage.textContent = 'Digitalizando...';
    startBtn.disabled = true;
    cancelBtn.disabled = false;
    loader.classList.remove('hidden');
  }

  if (state.status === AppState.FINISHED) {
    statusLabel.textContent = 'Finalizado';
    statusLabel.classList.add('finished');
    statusMessage.textContent = 'Processo finalizado.';
    startBtn.disabled = false;
    cancelBtn.disabled = true;
    loader.classList.add('hidden');
  }
}

function stopRunTimers() {
  if (state.runTimer) {
    clearTimeout(state.runTimer);
    state.runTimer = null;
  }

  if (state.autoImageTimer) {
    clearInterval(state.autoImageTimer);
    state.autoImageTimer = null;
  }
}

function addNewCapture() {
  state.imageCount += 1;
  state.images.unshift(createMockImage(state.imageCount));
}

function startScan() {
  if (state.status === AppState.RUNNING) {
    return;
  }

  state.status = AppState.RUNNING;
  setUiByState();

  state.autoImageTimer = setInterval(() => {
    addNewCapture();
    renderGallery();
  }, 1800);

  state.runTimer = setTimeout(() => {
    stopRunTimers();
    addNewCapture();
    renderGallery();
    state.status = AppState.FINISHED;
    setUiByState();
  }, 5000);
}

function cancelScan() {
  if (state.status !== AppState.RUNNING) {
    return;
  }

  stopRunTimers();
  state.status = AppState.IDLE;
  setUiByState();
}

function refreshGallery() {
  addNewCapture();
  renderGallery();

  if (state.status === AppState.FINISHED) {
    state.status = AppState.IDLE;
    setUiByState();
  }
}

function openModal(image) {
  modalImage.src = image.src;
  modalImage.alt = image.label;
  modal.classList.remove('hidden');
  modal.setAttribute('aria-hidden', 'false');
}

function closeModal() {
  modal.classList.add('hidden');
  modal.setAttribute('aria-hidden', 'true');
  modalImage.src = '';
}

startBtn.addEventListener('click', startScan);
cancelBtn.addEventListener('click', cancelScan);
refreshBtn.addEventListener('click', refreshGallery);
closeModalBtn.addEventListener('click', closeModal);
modal.addEventListener('click', (event) => {
  if (event.target === modal) {
    closeModal();
  }
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !modal.classList.contains('hidden')) {
    closeModal();
  }
});

seedGallery();
setUiByState();
renderGallery();
