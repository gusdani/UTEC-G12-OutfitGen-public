# Política de seguridad

Este repositorio no debe contener credenciales, datos personales, dumps de bases de datos, modelos privados ni configuraciones de infraestructura.

Antes de cada publicación, verifica que no se hayan añadido archivos `.env`, secretos de Streamlit, backups o datos reales. Las integraciones externas deben recibir sus credenciales mediante variables de entorno o el gestor de secretos de la plataforma.

## Servicios externos

La demo pública no realiza llamadas de red. Si se implementa una integración local o privada, mantén el código de conexión separado y configura las credenciales fuera de Git mediante `.env` local, secretos del despliegue o un gestor de secretos. Nunca uses valores reales en `.env.example`, tests, notebooks o mensajes de error.