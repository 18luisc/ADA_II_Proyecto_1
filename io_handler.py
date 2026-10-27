from algoritmos import Agente

def leer_archivo_entrada(ruta_archivo):
    """Lee el archivo de entrada con formato n+2 lineas."""
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
        
    n = int(lineas[0])
    agentes = []
    
    for i in range(1, n + 1):
        partes = lineas[i].split(',')
        op = int(partes[0].strip())
        recep = float(partes[1].strip())
        inf = float(partes[2].strip())
        agentes.append(Agente(op, recep, inf))
        
    R_max = int(lineas[n + 1])
    return n, agentes, R_max

def escribir_archivo_salida(ruta_archivo, estrategia, esfuerzo, extremismo):
    """Escribe el archivo de salida con formato n+2 lineas."""
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(f"{extremismo:.2f}\n")
        f.write(f"{esfuerzo}\n")
        for e in estrategia:
            f.write(f"{e}\n")