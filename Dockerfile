# Usar imagen oficial de Python
FROM python:3.10

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt requirements.txt

# Instalar dependencias
RUN pip install -r requirements.txt
COPY . .

# Expón el puerto que utilizará la aplicación
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]
