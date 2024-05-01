// Función para validar un campo específico con jQuery
function validarCampo(inputName, errorId, validationFunction, mensajeError) {
    var campo = $('[name="' + inputName + '"]').val(); // Obtener valor del campo por el atributo name
    var errorCampo = $('#' + errorId);
    
    // Validar el campo con la función de validación proporcionada
    console.log('Campo:', campo); // Verificar el valor del campo en la consola
    if (!validationFunction(campo)) {
        errorCampo.html(mensajeError).css('color', 'red'); // Establecer color rojo al mensaje de error
        return false; // Evitar envío del formulario si hay errores
    } else {
        errorCampo.html('').css('color', ''); // Limpiar mensaje de error si es válido y restablecer color
    }
    return true; // Envía el formulario si pasa todas las validaciones
}

// Función para validar el formulario completo con jQuery
function validarFormulario() {
    // Realiza todas las validaciones necesarias
    console.log('Validando formulario...'); // Verificar si la función se está llamando
    var nombreValido = validarCampo('first_name', 'error_first_name', noContieneNumeros, 'El nombre no puede contener números.');
    var apellidoValido = validarCampo('last_name', 'error_last_name', noContieneNumeros, 'El apellido no puede contener números.');
    var telefonoValido = validarCampo('telefon', 'error_telefon', contieneSoloNumeros, 'El teléfono solo puede contener números.');
    
    // Envía el formulario solo si todas las validaciones son válidas
    return nombreValido && apellidoValido && telefonoValido;
}

// Función para validar que un campo no contenga números
function noContieneNumeros(valor) {
    // Expresión regular para validar que no haya números en el campo
    var regex = /^[^\d]+$/;
    return regex.test(valor);
}

// Función para validar que un campo contenga solo números
function contieneSoloNumeros(valor) {
    // Expresión regular para validar que solo haya números en el campo
    var regex = /^[0-9]+$/;
    return regex.test(valor);
}
