import math

class Agente:
    def __init__(self, op: int, recep: float, inf: float):
        self.op = op
        self.recep = recep
        self.inf = inf
        
        # Reducción de extremismo al moderar (Beneficio)
        self.beneficio = (op ** 2) * inf
        
        # Esfuerzo necesario para moderar (Costo)
        if op == 0:
            self.costo = 0
        else:
            self.costo = math.ceil(abs(op) * (1.0 - recep) * inf)

def calcular_extremismo(agentes, estrategia):
    """Calcula el extremismo de la red dada una estrategia E."""
    suma_ext = 0.0
    n = len(agentes)
    for i in range(n):
        if estrategia[i] == 0:  # No moderado
            suma_ext += (agentes[i].op ** 2) * agentes[i].inf
        # Si estrategia[i] == 1, op pasa a 0 y la suma suma 0
    return math.sqrt(suma_ext) / n

def calcular_esfuerzo(agentes, estrategia):
    """Calcula el esfuerzo total de una estrategia E."""
    esfuerzo_total = 0
    for i in range(len(agentes)):
        if estrategia[i] == 1:
            esfuerzo_total += agentes[i].costo
    return esfuerzo_total

# 1. FUERZA BRUTA
def modexFB(agentes, R_max, callback_progreso=None):
    n = len(agentes)
    mejor_estrategia = [0] * n
    mejor_extremismo = float('inf')
    mejor_esfuerzo = 0
    total_combinaciones = 1 << n
    
    # Evaluar las 2^n combinaciones
    for i in range(total_combinaciones):
        estrategia_actual = [(i >> j) & 1 for j in range(n)]
        esfuerzo_actual = calcular_esfuerzo(agentes, estrategia_actual)
        
        if esfuerzo_actual <= R_max:
            ext_actual = calcular_extremismo(agentes, estrategia_actual)
            if ext_actual < mejor_extremismo:
                mejor_extremismo = ext_actual
                mejor_estrategia = estrategia_actual
                mejor_esfuerzo = esfuerzo_actual
                
        # Actualizar progreso cada 10,000 iteraciones
        if callback_progreso and (i % 10000 == 0 or i == total_combinaciones - 1):
            porcentaje = (i + 1) / total_combinaciones * 100
            callback_progreso(porcentaje)
                
    return mejor_estrategia, mejor_esfuerzo, mejor_extremismo

# 2. ALGORITMO VORAZ
def modexV(agentes, R_max):
    n = len(agentes)
    # Ordenar por ratio beneficio / costo descendente
    indices = list(range(n))
    indices.sort(
        key=lambda i: (agentes[i].beneficio / agentes[i].costo) if agentes[i].costo > 0 else 0,
        reverse=True
    )
    
    estrategia = [0] * n
    esfuerzo_acumulado = 0
    
    for idx in indices:
        c = agentes[idx].costo
        if c > 0 and esfuerzo_acumulado + c <= R_max:
            estrategia[idx] = 1
            esfuerzo_acumulado += c
            
    ext_final = calcular_extremismo(agentes, estrategia)
    return estrategia, esfuerzo_acumulado, ext_final

# 3. PROGRAMACIÓN DINÁMICA
def modexPD(agentes, R_max):
    n = len(agentes)
    # Matriz DP de (n+1) x (R_max + 1)
    dp = [[0.0] * (R_max + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        ag = agentes[i - 1]
        c = ag.costo
        b = ag.beneficio
        for w in range(R_max + 1):
            if c <= w and c > 0:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - c] + b)
            else:
                dp[i][w] = dp[i - 1][w]
                
    # Reconstrucción de la solución óptima
    estrategia = [0] * n
    w = R_max
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            estrategia[i - 1] = 1
            w -= agentes[i - 1].costo
            
    esfuerzo_total = calcular_esfuerzo(agentes, estrategia)
    ext_final = calcular_extremismo(agentes, estrategia)
    
    return estrategia, esfuerzo_total, ext_final