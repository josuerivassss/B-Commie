"""
Utilidad para parsear y formatear tiempos relativos
Soporta múltiples unidades: ms, s, m, h, d, w, mo, y
"""
import re
 
# Constantes de conversión
s = 1000
m = s * 60
h = m * 60
d = h * 24
w = d * 7
mo = d * 30
y = d * 365.25
 
# Diccionario de unidades
dic = {
    "ms": {"value": 1, "full": "milisecond"},
    "s": {"value": s, "full": "second"},
    "m": {"value": m, "full": "minute"},
    "h": {"value": h, "full": "hour"},
    "d": {"value": d, "full": "day"},
    "w": {"value": w, "full": "week"},
    "mo": {"value": mo, "full": "month"},
    "y": {"value": y, "full": "year"}
}
 
 
def parse(string: str) -> float | None:
    """
    Parsear string de tiempo a milisegundos
    
    Args:
        string: String de tiempo (ej: "30m", "1h30m", "2d12h")
    
    Returns:
        Milisegundos o None si inválido
    
    Examples:
        >>> parse("30m")
        1800000.0
        >>> parse("1h30m")
        5400000.0
        >>> parse("2d12h")
        216000000.0
        >>> parse("invalid")
        None
    """
    r = re.findall(r'(\d+\.\d+|\d+)(ms|s|mo|m|h|d|w|y)', string, flags=re.IGNORECASE)
    if not r:
        return None
    
    final = 0
    for datuple in r:
        TIME, TYPE = datuple
        final += float(TIME) * dic[TYPE.lower()]["value"]
    
    return final
 
 
def ms_to_short(number: float) -> str:
    """
    Convertir milisegundos a formato corto
    
    Args:
        number: Milisegundos
    
    Returns:
        String en formato corto (ej: "30m", "2h", "1d")
    
    Examples:
        >>> ms_to_short(1800000)
        '30m'
        >>> ms_to_short(7200000)
        '2h'
    """
    absed = abs(number)
    for key in list(dic.keys())[::-1]:
        if absed >= dic[key]["value"]:
            return f'{round(number / dic[key]["value"])}{key}'
    
    # Fallback si es menor que 1ms
    return f'{round(number)}ms'
 
 
def ms_to_long(number: float) -> str:
    """
    Convertir milisegundos a formato largo
    
    Args:
        number: Milisegundos
    
    Returns:
        String en formato largo (ej: "30 minutes", "2 hours", "1 day")
    
    Examples:
        >>> ms_to_long(1800000)
        '30 minutes'
        >>> ms_to_long(3600000)
        '1 hour'
        >>> ms_to_long(5400000)
        '1 hours'  # Nota: pluraliza si >= 1.5x
    """
    absed = abs(number)
    for key in list(dic.keys())[::-1]:
        if absed >= dic[key]["value"]:
            return pluralify(number, absed, dic[key]["value"], dic[key]["full"])
    
    # Fallback
    return f'{round(number)} miliseconds'
 
 
def pluralify(ms: float, absed: float, x: float, name: str) -> str:
    """
    Helper para pluralizar correctamente
    
    Args:
        ms: Milisegundos originales
        absed: Valor absoluto de ms
        x: Valor de la unidad
        name: Nombre de la unidad
    
    Returns:
        String formateado con plural si corresponde
    """
    see = absed >= x * 1.5
    return f'{round(ms / x)} {name}{"s" if see else ""}'
 
 
def load(time: str | int | float, long: bool = False) -> float | str | None:
    """
    Función unificada para parsear o formatear tiempo
    
    Args:
        time: String a parsear o número a formatear
        long: Si True, usa formato largo para números
    
    Returns:
        - Si time es string: milisegundos (float) o None
        - Si time es número: string formateado
    
    Examples:
        >>> load("30m")
        1800000.0
        >>> load(1800000)
        '30m'
        >>> load(1800000, long=True)
        '30 minutes'
    """
    if isinstance(time, str):
        return parse(time)
    else:
        return ms_to_long(time) if long else ms_to_short(time)
 
 
# Alias para compatibilidad
parse_time = parse
format_time = ms_to_short
format_time_long = ms_to_long