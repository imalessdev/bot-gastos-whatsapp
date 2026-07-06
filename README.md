123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116
Paso 2: Crear entorno virtual
Crea un entorno aislado para el proyecto:
bash
1234
Paso 3: Activar el entorno virtual
Actívalo antes de trabajar:
bash
123456
✅ Verás (venv) al inicio de tu terminal.
Paso 4: Instalar las dependencias
Instala todas las librerías necesarias:
bash
1
⏳ Espera a que termine. Solo se hace la primera vez.
Paso 5: Configurar el archivo .env
Crea tu archivo de configuración personal:
bash
1
Edita .env con tus credenciales reales:
env
12345678
⚠️ Nunca subas .env a GitHub.
Paso 6: Ejecutar el bot
bash
1
Verás:
1234
Paso 7: Detener el bot
Presiona Ctrl + C en la terminal.
🔄 Flujo de Uso Diario
Primera vez:
bash
12345
Siguientes veces:
bash
12
⚙️ Configuración
Antes de ejecutar, verifica:
✅ Entorno virtual activado ((venv) en la terminal)
✅ Dependencias instaladas
✅ .env configurado correctamente
✅ Ya enviaste el código join desde WhatsApp a Twilio
🚀 Uso
El bot revisa tu correo cada 5 minutos automáticamente. No necesitas interactuar con él. Solo déjalo corriendo en una terminal.
Para ejecutar en segundo plano:
Windows: start /B python bot.py
Mac/Linux: nohup python bot.py &
📱 Ejemplo de mensaje
12345678
🏦 Bancos soportados
Interbank Perú (servicioalcliente@netinterbank.com.pe)
Lemon Cash (notificaciones@lemoncash.com.ar)
Yape (notificaciones@yape.pe)
Puedes agregar más editando remitentes_bancos en bot.py.
📂 Estructura del proyecto
12345678
🔒 Seguridad
NUNCA subas .env a GitHub (ya está en .gitignore)
Usa contraseñas de aplicación, no tu contraseña real
Mantén tus API keys en secreto
Revoca credenciales si se filtran
⚠️ Limitaciones
Twilio Sandbox solo funciona con números registrados previamente
Groq tiene límite de 14,400 solicitudes/día (suficiente para uso personal)
Ejecución local requiere mantener la terminal abierta
Depende del formato de correos de cada banco
🔧 Personalización
Cambiar frecuencia de revisión
Edita bot.py línea ~180:
python
1
Personalizar mensaje
Edita la función enviar_whatsapp() en bot.py.
Agregar más bancos
Edita remitentes_bancos en obtener_correos_pendientes().
🐛 Solución de problemas
Error
Solución
Model decommissioned
Cambia el modelo en bot.py a llama-3.3-70b-versatile
Quota exceeded
Espera unos minutos o reduce la frecuencia
Authentication failed
Usa contraseña de aplicación, no la normal
No llegan WhatsApps
Envía join [código] al sandbox de Twilio
No such file or directory
Verifica que estés en la carpeta correcta
ModuleNotFoundError
Ejecuta pip install -r requirements.txt
Error PowerShell al activar venv
Usa CMD o ejecuta: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
🤝 Contribuciones
Fork el proyecto
Crea una rama (git checkout -b feature/nueva-funcion)
Commit (git commit -m 'Add nueva función')
Push (git push origin feature/nueva-funcion)
Abre un Pull Request
📝 Licencia
Este proyecto está bajo la Licencia MIT. Ver LICENSE para más detalles.
📧 Contacto
Alessandro - @tu-usuario
Repo: https://github.com/tu-usuario/bot-gastos-whatsapp
⭐ Si te fue útil, ¡dale una estrella! ⭐
<p align="center">Hecho con ❤️ y mucho ☕</p>
```
