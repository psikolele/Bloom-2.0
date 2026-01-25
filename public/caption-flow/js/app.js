/**
 * CaptionFlow - App Logic
 * Handles form submission and N8N webhook integration
 */

// ============================================
// CONFIGURATION
// ============================================

// N8N Webhook URL - Replace with your actual webhook URL
const WEBHOOK_URL = 'https://emanueleserra.app.n8n.cloud/webhook/caption-flow';

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
  loadingState: document.getElementById('loadingState'),
  successState: document.getElementById('successState'),
  errorState: document.getElementById('errorState'),
  errorMessage: document.getElementById('errorMessage'),
  newCaptionContainer: document.getElementById('newCaptionContainer'),
  newCaptionBtn: document.getElementById('newCaptionBtn'),
  // Bloom Return Elements
  returnBtn: document.getElementById('returnToBloomBtn'),
  bloomLoader: document.getElementById('bloomLoader')
};

// ============================================
// STATE MANAGEMENT
// ============================================

const state = {
  isSubmitting: false
};

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Shows a specific state element and hides others
 * @param {string} stateName - 'loading', 'success', 'error', or 'form'
 */
function showState(stateName) {
  // Hide all states
  elements.loadingState.classList.add('hidden');
  elements.successState.classList.add('hidden');
  elements.errorState.classList.add('hidden');
  elements.newCaptionContainer.classList.add('hidden');

  // Show form by default
  elements.form.classList.remove('hidden');
  elements.submitBtn.disabled = false;

  switch (stateName) {
    case 'loading':
      elements.loadingState.classList.remove('hidden');
      elements.submitBtn.disabled = true;
      break;
    case 'success':
      elements.form.classList.add('hidden');
      elements.successState.classList.remove('hidden');
      elements.newCaptionContainer.classList.remove('hidden');
      break;
    case 'error':
      elements.errorState.classList.remove('hidden');
      break;
    case 'form':
    default:
      // Form is already shown
      break;
  }
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
 * Shows an error message
 * @param {string} message - The error message to display
 */
function showError(message) {
  elements.errorMessage.textContent = message;
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

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  // Try to parse JSON response, but don't fail if it's not JSON
  try {
    return await response.json();
  } catch {
    return { success: true };
  }
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
    timestamp: new Date().toISOString(),
    source: 'CaptionFlow Web App'
  };

  try {
    // Send to webhook
    await sendToWebhook(data);

    // Show success state
    showState('success');

    // Save last used platform to localStorage
    localStorage.setItem('captionflow_last_platform', data.social_platform);

  } catch (error) {
    console.error('Submission error:', error);

    // Show user-friendly error
    let errorMsg = 'Impossibile inviare i dati. Verifica la connessione e riprova.';

    if (error.message.includes('Failed to fetch')) {
      errorMsg = 'Connessione al server non riuscita. Verifica che il webhook sia attivo.';
    } else if (error.message.includes('HTTP error')) {
      errorMsg = `Errore del server: ${error.message}`;
    }

    showError(errorMsg);
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
  elements.bloomLoader.classList.add('active');

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
  elements.newCaptionBtn.addEventListener('click', handleNewCaption);

  // Bloom Return Listener
  if (elements.returnBtn) {
    elements.returnBtn.addEventListener('click', handleReturnToBloom);
  }

  // Restore last used platform from localStorage
  const lastPlatform = localStorage.getItem('captionflow_last_platform');
  if (lastPlatform) {
    elements.socialSelect.value = lastPlatform;
  }

  // Focus on idea input
  elements.ideaInput.focus();

  console.log('CaptionFlow initialized');
  console.log('Webhook URL:', WEBHOOK_URL);
}

// Run initialization when DOM is ready
document.addEventListener('DOMContentLoaded', init);
