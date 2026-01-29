/**
 * CaptionFlow - App Logic
 * Handles form submission, N8N webhook integration, and Snake mini-game
 */

// ============================================
// CONFIGURATION
// ============================================

// N8N Webhook URL
const WEBHOOK_URL = '/api/proxy-caption-flow';

// ============================================
// DOM ELEMENTS
// ============================================

const elements = {
  form: document.getElementById('captionForm'),
  ideaInput: document.getElementById('ideaInput'),
  socialSelect: document.getElementById('socialSelect'),
  toneSelect: document.getElementById('toneSelect'),
  audienceSelect: document.getElementById('audienceSelect'),
  submitBtn: document.getElementById('submitBtn'),
  // Popup Elements
  popupOverlay: document.getElementById('popupOverlay'),
  popupCloseBtn: document.getElementById('popupCloseBtn'),
  loadingState: document.getElementById('loadingState'),
  successState: document.getElementById('successState'),
  errorState: document.getElementById('errorState'),
  errorMessage: document.getElementById('errorMessage'),
  popupNewCaptionBtn: document.getElementById('popupNewCaptionBtn'),
  retryBtn: document.getElementById('retryBtn'),
  // Legacy elements (kept for compatibility)
  newCaptionContainer: document.getElementById('newCaptionContainer'),
  newCaptionBtn: document.getElementById('newCaptionBtn'),
  // Preview Elements
  postPreview: document.getElementById('postPreview'),
  previewImage: document.getElementById('previewImage'),
  previewCaptionText: document.getElementById('previewCaptionText'),
  // Bloom Return Elements
  returnBtn: document.getElementById('returnToBloomBtn'),
  bloomLoader: document.getElementById('bloomLoader'),
  // Snake Game Elements
  snakeCanvas: document.getElementById('snakeCanvas'),
  snakeScore: document.getElementById('snakeScore'),
  snakeRestartBtn: document.getElementById('snakeRestartBtn'),
  // Progress Elements
  progressSteps: document.querySelectorAll('.progress-step'),
  progressLines: document.querySelectorAll('.progress-line'),
  formatToggle: document.getElementById('formatToggle')
};

// ============================================
// STATE MANAGEMENT
// ============================================

const state = {
  isSubmitting: false
};

// ============================================
// SNAKE GAME
// ============================================

const snakeGame = {
  canvas: null,
  ctx: null,
  snake: [],
  food: { x: 0, y: 0 },
  direction: 'RIGHT',
  nextDirection: 'RIGHT',
  gridSize: 14,
  tileCount: 20,
  score: 0,
  gameLoop: null,
  isRunning: false,
  colors: {
    background: '#0a0a0a',
    snake: '#F97316',
    snakeHead: '#FDBA74',
    food: '#10B981',
    grid: 'rgba(255,255,255,0.03)'
  },

  init() {
    this.canvas = elements.snakeCanvas;
    if (!this.canvas) return;

    this.ctx = this.canvas.getContext('2d');
    this.tileCount = Math.floor(this.canvas.width / this.gridSize);

    // Event listeners
    document.addEventListener('keydown', (e) => this.handleKeydown(e));
    elements.snakeRestartBtn?.addEventListener('click', () => this.restart());

    // Touch support for mobile
    this.setupTouchControls();
  },

  setupTouchControls() {
    if (!this.canvas) return;

    let touchStartX = 0;
    let touchStartY = 0;

    this.canvas.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
      e.preventDefault();
    }, { passive: false });

    this.canvas.addEventListener('touchend', (e) => {
      const touchEndX = e.changedTouches[0].clientX;
      const touchEndY = e.changedTouches[0].clientY;

      const deltaX = touchEndX - touchStartX;
      const deltaY = touchEndY - touchStartY;

      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        if (deltaX > 30 && this.direction !== 'LEFT') {
          this.nextDirection = 'RIGHT';
        } else if (deltaX < -30 && this.direction !== 'RIGHT') {
          this.nextDirection = 'LEFT';
        }
      } else {
        if (deltaY > 30 && this.direction !== 'UP') {
          this.nextDirection = 'DOWN';
        } else if (deltaY < -30 && this.direction !== 'DOWN') {
          this.nextDirection = 'UP';
        }
      }
      e.preventDefault();
    }, { passive: false });
  },

  start() {
    if (this.isRunning) return;

    this.reset();
    this.isRunning = true;
    this.gameLoop = setInterval(() => this.update(), 100);
  },

  stop() {
    if (this.gameLoop) {
      clearInterval(this.gameLoop);
      this.gameLoop = null;
    }
    this.isRunning = false;
  },

  reset() {
    const center = Math.floor(this.tileCount / 2);
    this.snake = [
      { x: center, y: center },
      { x: center - 1, y: center },
      { x: center - 2, y: center }
    ];
    this.direction = 'RIGHT';
    this.nextDirection = 'RIGHT';
    this.score = 0;
    this.updateScore();
    this.spawnFood();
  },

  restart() {
    this.stop();
    this.start();
  },

  spawnFood() {
    let validPosition = false;
    while (!validPosition) {
      this.food.x = Math.floor(Math.random() * this.tileCount);
      this.food.y = Math.floor(Math.random() * this.tileCount);

      validPosition = !this.snake.some(segment =>
        segment.x === this.food.x && segment.y === this.food.y
      );
    }
  },

  handleKeydown(e) {
    if (!this.isRunning) return;

    switch (e.key) {
      case 'ArrowUp':
      case 'w':
      case 'W':
        if (this.direction !== 'DOWN') this.nextDirection = 'UP';
        e.preventDefault();
        break;
      case 'ArrowDown':
      case 's':
      case 'S':
        if (this.direction !== 'UP') this.nextDirection = 'DOWN';
        e.preventDefault();
        break;
      case 'ArrowLeft':
      case 'a':
      case 'A':
        if (this.direction !== 'RIGHT') this.nextDirection = 'LEFT';
        e.preventDefault();
        break;
      case 'ArrowRight':
      case 'd':
      case 'D':
        if (this.direction !== 'LEFT') this.nextDirection = 'RIGHT';
        e.preventDefault();
        break;
    }
  },

  update() {
    this.direction = this.nextDirection;

    const head = { ...this.snake[0] };

    switch (this.direction) {
      case 'UP': head.y--; break;
      case 'DOWN': head.y++; break;
      case 'LEFT': head.x--; break;
      case 'RIGHT': head.x++; break;
    }

    // Wall collision (wrap around)
    if (head.x < 0) head.x = this.tileCount - 1;
    if (head.x >= this.tileCount) head.x = 0;
    if (head.y < 0) head.y = this.tileCount - 1;
    if (head.y >= this.tileCount) head.y = 0;

    // Self collision
    if (this.snake.some(segment => segment.x === head.x && segment.y === head.y)) {
      this.reset();
      return;
    }

    this.snake.unshift(head);

    // Food collision
    if (head.x === this.food.x && head.y === this.food.y) {
      this.score += 10;
      this.updateScore();
      this.spawnFood();
    } else {
      this.snake.pop();
    }

    this.draw();
  },

  draw() {
    const ctx = this.ctx;
    const gridSize = this.gridSize;

    // Clear canvas
    ctx.fillStyle = this.colors.background;
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw subtle grid
    ctx.strokeStyle = this.colors.grid;
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= this.tileCount; i++) {
      ctx.beginPath();
      ctx.moveTo(i * gridSize, 0);
      ctx.lineTo(i * gridSize, this.canvas.height);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, i * gridSize);
      ctx.lineTo(this.canvas.width, i * gridSize);
      ctx.stroke();
    }

    // Draw food with glow
    ctx.shadowColor = this.colors.food;
    ctx.shadowBlur = 10;
    ctx.fillStyle = this.colors.food;
    ctx.beginPath();
    ctx.arc(
      this.food.x * gridSize + gridSize / 2,
      this.food.y * gridSize + gridSize / 2,
      gridSize / 2 - 2,
      0, Math.PI * 2
    );
    ctx.fill();
    ctx.shadowBlur = 0;

    // Draw snake
    this.snake.forEach((segment, index) => {
      ctx.fillStyle = index === 0 ? this.colors.snakeHead : this.colors.snake;
      ctx.shadowColor = this.colors.snake;
      ctx.shadowBlur = index === 0 ? 8 : 4;

      const padding = 1;
      ctx.fillRect(
        segment.x * gridSize + padding,
        segment.y * gridSize + padding,
        gridSize - padding * 2,
        gridSize - padding * 2
      );
    });
    ctx.shadowBlur = 0;
  },

  updateScore() {
    if (elements.snakeScore) {
      elements.snakeScore.textContent = this.score;
    }
  }
};

// ============================================
// PROGRESS TRACKING
// ============================================

let progressInterval = null;
let currentStep = 1;

function startProgressSimulation() {
  currentStep = 1;
  updateProgressUI(currentStep);

  // Simulate progress steps (adjust timing based on expected workflow duration)
  const stepDurations = [15000, 45000, 20000, 10000]; // ms per step
  let totalElapsed = 0;

  progressInterval = setInterval(() => {
    totalElapsed += 1000;

    let accumulated = 0;
    for (let i = 0; i < stepDurations.length; i++) {
      accumulated += stepDurations[i];
      if (totalElapsed < accumulated) {
        if (currentStep !== i + 1) {
          currentStep = i + 1;
          updateProgressUI(currentStep);
        }
        break;
      }
    }

    // Safety: stop after max time
    if (totalElapsed > 120000) {
      stopProgressSimulation();
    }
  }, 1000);
}

function stopProgressSimulation() {
  if (progressInterval) {
    clearInterval(progressInterval);
    progressInterval = null;
  }
}

function completeProgress() {
  stopProgressSimulation();
  updateProgressUI(5); // Mark all as complete
}

function updateProgressUI(step) {
  elements.progressSteps.forEach((stepEl, index) => {
    const stepNum = index + 1;
    stepEl.classList.remove('active', 'completed');

    if (stepNum < step) {
      stepEl.classList.add('completed');
    } else if (stepNum === step) {
      stepEl.classList.add('active');
    }
  });

  elements.progressLines.forEach((line, index) => {
    line.classList.remove('completed');
    if (index < step - 1) {
      line.classList.add('completed');
    }
  });
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Shows a specific state element and hides others
 * @param {string} stateName - 'loading', 'success', 'error', or 'form'
 * @param {Object} [data] - Optional data for success state (preview)
 */
function showState(stateName, data = null) {
  // Hide all popup content states
  elements.loadingState?.classList.add('hidden');
  elements.successState?.classList.add('hidden');
  elements.errorState?.classList.add('hidden');
  elements.newCaptionContainer?.classList.add('hidden');

  // Reset form state
  elements.submitBtn.disabled = false;

  switch (stateName) {
    case 'loading':
      // Show popup with loading state
      elements.popupOverlay?.classList.remove('hidden');
      elements.loadingState?.classList.remove('hidden');
      elements.submitBtn.disabled = true;
      // Start Snake game and progress
      snakeGame.start();
      startProgressSimulation();
      break;

    case 'success':
      // Show popup with success state
      elements.popupOverlay?.classList.remove('hidden');
      elements.successState?.classList.remove('hidden');
      // Stop Snake game and complete progress
      snakeGame.stop();
      completeProgress();

      // Update message if provided by server (e.g. timeout fallback)
      if (data && data.message) {
        const subtitle = elements.successState.querySelector('.popup-subtitle');
        if (subtitle) subtitle.textContent = data.message;
      }

      // Render preview if data is available
      if (data && data.data) {
        renderPreview(data.data);
      } else {
        // Hide preview card if no data (e.g. in timeout fallback)
        elements.postPreview?.classList.add('hidden');
      }
      break;

    case 'error':
      // Show popup with error state
      elements.popupOverlay?.classList.remove('hidden');
      elements.errorState?.classList.remove('hidden');
      // Stop Snake game
      snakeGame.stop();
      stopProgressSimulation();
      break;

    case 'form':
    default:
      // Close popup and return to form
      elements.popupOverlay?.classList.add('hidden');
      snakeGame.stop();
      stopProgressSimulation();
      break;
  }
}

/**
 * Renders the post preview
 * @param {Object} data - The preview data (caption, image_url, video_url)
 */
function renderPreview(data) {
  if (!data) return;

  const imageContainer = elements.previewImage?.parentElement;

  // Reset visibility
  if (elements.previewImage) elements.previewImage.style.display = 'none';
  if (elements.previewVideo) {
    elements.previewVideo.style.display = 'none';
    elements.previewVideo.pause();
    elements.previewVideo.src = "";
  } else {
    // Dynamically create video element if it doesn't exist
    if (data.video_url && imageContainer) {
      const videoEl = document.createElement('video');
      videoEl.id = 'previewVideo';
      videoEl.className = 'instagram-image';
      videoEl.controls = true;
      videoEl.autoplay = true;
      videoEl.loop = true;
      videoEl.style.objectFit = 'cover';
      imageContainer.appendChild(videoEl);
      elements.previewVideo = videoEl;
    }
  }

  // Handle Video
  if (data.video_url && elements.previewVideo) {
    elements.previewVideo.src = data.video_url;
    elements.previewVideo.style.display = 'block';
  }
  // Handle Image
  else if (data.image_url && elements.previewImage) {
    elements.previewImage.src = data.image_url;
    elements.previewImage.style.display = 'block';
  }

  if (data.caption && elements.previewCaptionText) {
    elements.previewCaptionText.textContent = data.caption;
  }

  elements.postPreview?.classList.remove('hidden');
}

/**
 * Validates the form data
 * @returns {boolean} - Whether the form is valid
 */
function validateForm() {
  const idea = elements.ideaInput.value.trim();
  const social = elements.socialSelect.value;
  const tone = elements.toneSelect.value;
  const audience = elements.audienceSelect.value;

  if (!idea) {
    showError('Per favore, inserisci un\'idea o una frase.');
    elements.ideaInput.focus();
    return false;
  }

  if (!social) {
    showError('Per favore, seleziona una piattaforma social.');
    elements.socialSelect.focus();
    return false;
  }

  if (!tone) {
    showError('Per favore, seleziona un tono di voce.');
    elements.toneSelect.focus();
    return false;
  }

  if (!audience) {
    showError('Per favore, seleziona un target audience.');
    elements.audienceSelect.focus();
    return false;
  }

  return true;
}

/**
 * Shows an error message with optional error code
 * @param {string} message - The error message to display
 * @param {string} [errorCode] - Optional error code
 */
function showError(message, errorCode = null) {
  let fullMessage = message;

  if (errorCode) {
    fullMessage += `<br><span class="error-code">Codice: ${errorCode}</span>`;
    elements.errorMessage.innerHTML = fullMessage;
  } else {
    elements.errorMessage.textContent = message;
  }

  showState('error');
}

/**
 * Resets the form for a new caption
 */
function resetForm() {
  elements.ideaInput.value = '';
  elements.socialSelect.value = '';
  elements.toneSelect.value = '';
  elements.audienceSelect.value = '';
  if (elements.formatToggle) elements.formatToggle.checked = false; // Reset to Image
  showState('form');
  elements.ideaInput.focus();
}

// ============================================
// API FUNCTIONS
// ============================================

/**
 * Sends data to the N8N webhook
 * @param {Object} data - The data to send
 * @returns {Promise<Object>} - The response from the webhook
 */
async function sendToWebhook(data) {
  const response = await fetch(WEBHOOK_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });

  // Parse response body
  let responseData;
  try {
    responseData = await response.json();
  } catch {
    responseData = null;
  }

  // Check for HTTP errors
  if (!response.ok) {
    const error = new Error(`HTTP error! status: ${response.status}`);
    error.status = response.status;
    error.responseData = responseData;
    throw error;
  }

  // Check for application-level errors in response
  if (responseData && responseData.success === false) {
    const error = new Error(responseData.message || 'Errore dal server');
    error.code = responseData.error_code || 'UNKNOWN_ERROR';
    error.responseData = responseData;
    throw error;
  }

  return responseData || { success: true };
}

// ============================================
// EVENT HANDLERS
// ============================================

/**
 * Handles form submission
 * @param {Event} event - The submit event
 */
async function handleSubmit(event) {
  event.preventDefault();

  // Prevent double submission
  if (state.isSubmitting) return;

  // Validate form
  if (!validateForm()) return;

  // Set submitting state
  state.isSubmitting = true;
  showState('loading');

  // Prepare data
  const data = {
    Topic: elements.ideaInput.value.trim(),
    Platform: elements.socialSelect.value,
    Audience: elements.audienceSelect.value,
    Voice: elements.toneSelect.value,
    format: elements.formatToggle && elements.formatToggle.checked ? 'video' : 'image',
    timestamp: new Date().toISOString(),
    source: 'CaptionFlow Web App'
  };

  try {
    // Send to webhook
    const response = await sendToWebhook(data);

    // Show success state with response data
    showState('success', response);

    // Save last used platform to localStorage
    localStorage.setItem('captionflow_last_platform', data.Platform);

  } catch (error) {
    console.error('Submission error:', error);

    // Determine error message and code
    let errorMsg = 'Impossibile inviare i dati. Verifica la connessione e riprova.';
    let errorCode = null;

    if (error.message.includes('Failed to fetch')) {
      errorMsg = 'Connessione al server non riuscita. Verifica la tua connessione internet.';
      errorCode = 'NETWORK_ERROR';
    } else if (error.status) {
      errorCode = `HTTP_${error.status}`;
      switch (error.status) {
        case 400:
          errorMsg = 'Richiesta non valida. Verifica i dati inseriti.';
          break;
        case 401:
        case 403:
          errorMsg = 'Accesso non autorizzato al servizio.';
          break;
        case 404:
          errorMsg = 'Servizio non trovato. Il webhook potrebbe non essere attivo.';
          break;
        case 500:
        case 502:
        case 503:
          errorMsg = 'Errore del server. Riprova tra qualche minuto.';
          break;
        default:
          errorMsg = `Errore del server: ${error.status}`;
      }
    } else if (error.code) {
      errorCode = error.code;
      errorMsg = error.message;

      // Map known error codes to user-friendly messages
      const errorMessages = {
        'IMAGE_GENERATION_FAILED': 'Generazione immagine fallita. Riprova.',
        'CAPTION_GENERATION_FAILED': 'Generazione caption fallita. Riprova.',
        'CLOUDINARY_UPLOAD_FAILED': 'Upload immagine fallito. Riprova.',
        'EMAIL_SEND_FAILED': 'Invio email di conferma fallito. Riprova.',
        'TIMEOUT': 'Il processo ha impiegato troppo tempo. Riprova.'
      };

      if (errorMessages[error.code]) {
        errorMsg = errorMessages[error.code];
      }
    }

    showError(errorMsg, errorCode);
  } finally {
    state.isSubmitting = false;
  }
}

/**
 * Handles new caption button click
 */
function handleNewCaption() {
  resetForm();
}

/**
 * Handles return to Bloom AI button click
 */
function handleReturnToBloom() {
  // Show loader
  elements.bloomLoader?.classList.add('active');

  // Simulate loading delay then redirect
  setTimeout(() => {
    window.location.href = '/';
  }, 2500);
}

// ============================================
// INITIALIZATION
// ============================================

/**
 * Initializes the application
 */
function init() {
  // Attach event listeners
  elements.form.addEventListener('submit', handleSubmit);
  elements.newCaptionBtn?.addEventListener('click', handleNewCaption);

  // Popup button listeners
  elements.popupCloseBtn?.addEventListener('click', () => {
    showState('form');
  });
  elements.popupNewCaptionBtn?.addEventListener('click', handleNewCaption);
  elements.retryBtn?.addEventListener('click', handleNewCaption);

  // Bloom Return Listener
  if (elements.returnBtn) {
    elements.returnBtn.addEventListener('click', handleReturnToBloom);
  }

  // Initialize Snake game
  snakeGame.init();

  // Restore last used platform from localStorage
  const lastPlatform = localStorage.getItem('captionflow_last_platform');
  if (lastPlatform) {
    elements.socialSelect.value = lastPlatform;
  }

  // Focus on idea input
  elements.ideaInput.focus();

  console.log('CaptionFlow initialized with Snake mini-game');
  console.log('Webhook URL:', WEBHOOK_URL);
}

// Run initialization when DOM is ready
document.addEventListener('DOMContentLoaded', init);
