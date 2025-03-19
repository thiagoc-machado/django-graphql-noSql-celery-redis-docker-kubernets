# Usar uma imagem base do Python
FROM python:3.9-slim

# Variáveis de ambiente para não gerar arquivos __pycache__ e log
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requirements e instalar dependências
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar o código da aplicação
COPY . /app/

# Expor a porta que o Django vai rodar
EXPOSE 8000

# Comando padrão (para o serviço Django)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
