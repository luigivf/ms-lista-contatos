# Usa imagem Python official enxuta
FROM python:3.13.3-alpine

# Indica pasta de trabalho
WORKDIR /app

# Copia o conteúdo da pasta do serviço para o container
COPY ./src /app

# Instala dependências
RUN pip install fastapi uvicorn requests ariadne

EXPOSE 8006

# Executa aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006"]
