"""
Coleta informações do sistema relacionadas ao uso da CPU e memória RAM,
bem como a temperatura da CPU.
"""

import os
from datetime import datetime
from time import sleep

def ler_cpu_usagem():
    """
    Calcula o uso da CPU com base nos dados de /proc/stat.
    """
    
    with open("/proc/stat", "r") as f:
        linha = f.readline()
    partes = linha.split()
    if partes[0] != "cpu":
        raise ValueError("Formato inesperado no /proc/stat.")

    valores = list(map(int, partes[1:]))
    idle = valores[3] + valores[4]
    total = sum(valores)

    return idle, total

def calcular_uso_cpu(idle_ant, total_ant, idle_atual, total_atual):
    """
    Calcula a porcentagem de uso da CPU entre duas leituras.
    """
    
    total_diferenca = total_atual - total_ant
    idle_diferenca = idle_atual - idle_ant
    if total_diferenca == 0:
        return 0.0
    return 100.0 * (1 - idle_diferenca / total_diferenca)

def coletar_informacoes(idle_ant, total_ant):
    """
    Coleta informações do sistema e exibe na tela.
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    idle_atual, total_atual = ler_cpu_usagem()
    cpu_use = calcular_uso_cpu(idle_ant, total_ant, idle_atual, total_atual)

    try:
        cpu_temp = os.popen("vcgencmd measure_temp").readline()
        cpu_temp = cpu_temp.replace("temp=", "").replace("'C", "").strip()
    except Exception as e:
        cpu_temp = f"Erro: {e}"

    try:
        mem_info = os.popen("free -m | grep Mem").readline().split()
        mem_used = mem_info[2]
        mem_total = mem_info[1]
    except Exception as e:
        mem_used = mem_total = f"Erro: {e}"

    print(
        f"[{timestamp}] CPU Use: {cpu_use:.2f}% | "
        f"CPU Temp: {cpu_temp}°C | "
        f"Mem Used: {mem_used} MB de {mem_total} MB"
    )

    return idle_atual, total_atual

idle_ant, total_ant = ler_cpu_usagem()

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"[{timestamp}] Iniciado teste da placa.")

for _ in range(4):
    sleep(1)
    idle_ant, total_ant = coletar_informacoes(idle_ant, total_ant)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"[{timestamp}] Encerrado teste da placa.")