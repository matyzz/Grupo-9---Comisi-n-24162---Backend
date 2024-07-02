document.getElementById('submitBtn').addEventListener('click', function(event) {
    // Previene el envío del formulario por defecto
    event.preventDefault();

    // Limpia los mensajes de error anteriores
    clearErrorMessages();
    clearSuccessMessages();

    var isValid = true;
    var nombre = document.getElementById('nombre').value.trim();
    var correo = document.getElementById('correo').value.trim();
    var telefono = document.getElementById('telefono').value.trim();
    var domicilio = document.getElementById('domicilio').value.trim();
    var archivo = document.getElementById('archivo').files[0];

    // Validación del nombre
    if (nombre.length < 3) {
        isValid = false;
        showError('El nombre debe tener al menos 3 caracteres.');
    }

    // Validación del correo
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(correo)) {
        isValid = false;
        showError('Por favor, ingrese un correo electrónico válido.');
    }

    // Validación del teléfono
    var telefonoRegex = /^[0-9]{10}$/;
    if (!telefonoRegex.test(telefono)) {
        isValid = false;
        showError('Por favor, ingrese un número de teléfono válido de 10 dígitos.');
    }

    // Validación del domicilio
    if (domicilio === '') {
        isValid = false;
        showError('El domicilio no puede estar vacío.');
    }

    // Validación del archivo
    if (archivo) {
        var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
        if (!allowedExtensions.exec(archivo.name)) {
            isValid = false;
            showError('Por favor, suba un archivo de imagen válido (JPG, JPEG, PNG, GIF).');
        }
    }

    // Si todas las validaciones pasan, se envía el formulario
    if (isValid) {
        var formData = new FormData(document.getElementById('contactForm'));

        fetch('/contacto', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuccess(data.message);
            } else {
                showError(data.message);
            }
        })
        .catch(error => {
            showError('Ocurrió un error al enviar el formulario. Por favor, inténtelo de nuevo.');
        });
    }
});

function showError(message) {
    var errorMessageElement = document.getElementById('error-message');
    errorMessageElement.innerText = message;
    errorMessageElement.style.display = 'block';
}

function showSuccess(message) {
    var successMessageElement = document.getElementById('success-message');
    successMessageElement.innerText = message;
    successMessageElement.style.display = 'block';
}

function clearErrorMessages() {
    var errorMessageElement = document.getElementById('error-message');
    errorMessageElement.innerText = '';
    errorMessageElement.style.display = 'none';
}

function clearSuccessMessages() {
    var successMessageElement = document.getElementById('success-message');
    successMessageElement.innerText = '';
    successMessageElement.style.display = 'none';
}
