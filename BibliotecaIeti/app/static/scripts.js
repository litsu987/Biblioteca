// Definición de la función GenerarLogs
function GenerarLogs(tipo, mensaje) {
    // Implementación de GenerarLogs
    if (typeof(Storage) !== "undefined") {
        let logs = JSON.parse(localStorage.getItem('logs')) || [];
        let nuevoLog = {
            tipo: tipo,
            mensaje: mensaje,
            fecha: new Date().toISOString()
        };
        logs.push(nuevoLog);
        localStorage.setItem('logs', JSON.stringify(logs));
        console.log("Log generado y guardado correctamente en el localStorage.");
        
        // Mostrar los logs en la consola
        console.log("Logs almacenados en el localStorage:", logs);
    } else {
        console.log("Lo siento, tu navegador no soporta el almacenamiento local.");
    }
}

  
  document.addEventListener('DOMContentLoaded', function() {
    const btnCerca = document.getElementById('btnCerca');
    const btnEntra = document.getElementById('btnEntra');
  
    btnCerca.onclick = function() {
      GenerarLogs('info', 'El usuario ha realizado una búsqueda en el catálogo');
    };
  
    btnEntra.onclick = function() {
      GenerarLogs('info', 'El usuario ha iniciado sesión');
    };
  });
  
  