import re
from datetime import datetime


#-----------------------------------------------------------
# Módulo de Validaciones
#------------------------------------------------------------
# Este módulo contiene funciones auxiliares para:
# - Validar formato de campos (email, patente)
# - Cálculos de negocio (total a cobrar)
#
# Separamos estas funciones del modelo y controlador
# para mantener el código organizado (principio de responsabilidad única)
#------------------------------------------------------------


# ============================================================
# VALIDACIÓN DE PATENTE - Solo alfanuméricos
# ============================================================
# El profesor pide validar con regex para admitir solo alfanuméricos.
# Patrón sugerido: ^[A-Za-z]+(?:[_-][A-Za-z]+)*$
# 
# Usamos un patrón más flexible que acepta:
# - Patentes argentinas viejas: ABC123
# - Patentes argentinas nuevas: AB123CD
# - Solo letras y números, sin espacios ni caracteres especiales
# ============================================================

def validar_patente(patente):
    """
    Valida que la patente contenga solo caracteres alfanuméricos.
    
    Parámetros:
        patente: string con la patente a validar
    
    Retorna:
        True si es válida, False si contiene caracteres inválidos
    
    Ejemplos válidos:
        - "ABC123"
        - "AB123CD"
        - "AA123BB"
    
    Ejemplos inválidos:
        - "ABC-123" (tiene guión)
        - "ABC 123" (tiene espacio)
        - "" (vacía)
    """
    # Patrón: solo letras (mayúsculas/minúsculas) y números
    # ^ = inicio, $ = fin, + = uno o más caracteres
    patron = r'^[A-Za-z0-9]+$'
    
    # Si la patente está vacía, no es válida
    if not patente:
        return False
    
    # re.match verifica si el patrón coincide
    return re.match(patron, patente) is not None


# ============================================================
# VALIDACIÓN DE EMAIL
# ============================================================

def aux_email_formato(email):
    """
    Verifica que el email tenga formato válido.
    
    Parámetros:
        email: string con el email a validar
    
    Retorna:
        True si tiene formato válido, False si no
    
    Ejemplos válidos:
        - "usuario@dominio.com"
        - "nombre.apellido@empresa.com.ar"
    
    Ejemplos inválidos:
        - "usuario@" (falta dominio)
        - "usuario.com" (falta @)
    """
    # Patrón de email básico:
    # [\w\.-]+ = uno o más caracteres de palabra, puntos o guiones
    # @ = arroba obligatoria
    # [\w\.-]+ = dominio
    # \. = punto obligatorio
    # \w+ = extensión (com, ar, etc.)
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None


# ============================================================
# CÁLCULO DE TOTAL A COBRAR
# ============================================================

def aux_calcular_total(hora_ingreso, valor_hora):
    """
    Calcula el total a cobrar según el tiempo estacionado.
    
    Parámetros:
        hora_ingreso: string con formato "HH:MM"
        valor_hora: precio por hora (float o int)
    
    Retorna:
        El monto total a cobrar (float)
    
    Reglas de cobro:
        - Hasta 60 minutos: se cobra 1 hora completa
        - Más de 60 minutos: se prorratea por el tiempo exacto
    
    Ejemplo:
        - Si valor_hora = 100 y pasaron 30 minutos: cobra 100
        - Si valor_hora = 100 y pasaron 90 minutos: cobra 150
    """
    formato = "%H:%M"
    
    # Obtengo la fecha de hoy
    hoy = datetime.now().date()
    
    # Convierto el string de hora a objeto datetime
    hora_ingreso_dt = datetime.strptime(hora_ingreso, formato).time()
    
    # Combino fecha de hoy con hora de ingreso
    inicio = datetime.combine(hoy, hora_ingreso_dt)
    
    # Hora actual
    fin = datetime.now()
    
    # Calculo los minutos transcurridos
    minutos = int((fin - inicio).total_seconds() / 60)
    
    # Aplico la regla de cobro
    if minutos <= 60:
        # Hasta 1 hora: cobra hora completa
        return valor_hora
    else:
        # Más de 1 hora: prorratea
        return round((minutos / 60) * valor_hora, 2)