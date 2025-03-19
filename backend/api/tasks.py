from celery import shared_task
from datetime import datetime
from celery import shared_task
import time
from prometheus_client import Counter

@shared_task
def soma_assincrona(a, b):
    """Tarefa assíncrona que simula um cálculo demorado"""
    time.sleep(5)  # Simula um processo demorado
    return a + b

@shared_task
def tarefa_recorrente():
    """Tarefa que roda diariamente para demonstrar o uso do Celery Beat"""
    print(f'Tarefa automática executada em {datetime.now()}')
    return 'Tarefa concluída'

tarefa_executada = Counter('tarefa_executada_total', 'Número de tarefas executadas')
@shared_task
def tarefa_com_monitoramento():
    """Tarefa que será monitorada pelo Prometheus"""
    tarefa_executada.inc()  # Incrementa o contador
    return "Tarefa monitorada concluída"