import logging
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import Log, Usuari 
from django.db import transaction

import logging

def generarLog(request, tipo, mensaje):
    # Accede a la sesión del usuario
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key
    
    # Obtiene o crea la lista de registros en la sesión del usuario
    logs = request.session.get('logs', [])
    
    # Agrega el registro a la lista
    nuevo_log = {
        'timestamp': timezone.now().isoformat(),
        'tipo': tipo,  # Asegúrate de agregar el tipo de registro correctamente aquí
        'mensaje': mensaje
    }
    logs.append(nuevo_log)
    
    # Guarda la lista de registros de nuevo en la sesión del usuario
    request.session['logs'] = logs
    
    # Imprime todos los logs por la consola
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Imprime todos los logs almacenados en la sesión
    for log in logs:
        log_message = f"{log['timestamp']} - {log['tipo'].upper()}: {log['mensaje']}"
        getattr(logger, log['tipo'].lower())(log_message)

    return f"{tipo.upper()}: {mensaje}"



def subir_logs_a_bd(request):
    # Obtiene todos los registros de logs almacenados en la sesión del usuario
    logs = request.session.get('logs', [])
    
    # Obtener el nombre de usuario si está autenticado
    usuario = None
    if request.user.is_authenticated:
        usuario = request.user.username

    # Utilizar una transacción para garantizar la integridad de la base de datos
    with transaction.atomic():
        # Itera sobre cada log y los inserta en la base de datos
        for log in logs:
            tipo = log['tipo']
            mensaje = log['mensaje']
            # Inserta el log en la base de datos
            log_obj = Log(accio=mensaje, data_accio=timezone.now(), tipus=tipo, usuari=usuario)
            log_obj.save()

        # Limpia la lista de logs de la sesión del usuario
        request.session['logs'] = []

        # Ejecuta las migraciones pendientes
        from django.core.management import call_command
        call_command('migrate')

    # Retorna un mensaje indicando que los logs han sido guardados en la base de datos
    return "Todos los logs han sido guardados en la base de datos y las migraciones se han ejecutado correctamente."