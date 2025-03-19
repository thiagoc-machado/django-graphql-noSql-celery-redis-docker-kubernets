FROM python:3.9-slim

# Instala o celery-prometheus-exporter e força a instalação do redis em versão 3.5.3
RUN pip install celery-prometheus-exporter redis==3.5.3

EXPOSE 5555

CMD ["celery-prometheus-exporter"]