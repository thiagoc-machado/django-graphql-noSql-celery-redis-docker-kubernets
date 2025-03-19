import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Configurações do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir tarefas automaticamente em apps registrados
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'tarefa_recorrente': {
        'task': 'api.tasks.tarefa_recorrente',
        'schedule': crontab(minute=0, hour=0),  # Executa diariamente à meia-noite
    },
}