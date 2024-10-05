function showAlert(type, message) {
    const alertId = type === 'success' ? 'success-alert' : 'error-alert';
    const messageId = type === 'success' ? 'success-message' : 'error-message';

    // Ocultar cualquier alerta activa
    document.getElementById('success-alert').classList.add('hidden');
    document.getElementById('error-alert').classList.add('hidden');

    // Mostrar la alerta correcta
    const alertElement = document.getElementById(alertId);
    alertElement.classList.remove('hidden');
    document.getElementById(messageId).innerText = message;

    // Ocultar la alerta después de 5 segundos
    setTimeout(() => {
        hideAlert(alertId);
    }, 10000);
}

function hideAlert(alertId) {
    document.getElementById(alertId).classList.add('hidden');
}