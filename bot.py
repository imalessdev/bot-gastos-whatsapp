import os
import sqlite3
import json
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
from imap_tools import MailBox, AND
from twilio.rest import Client
from groq import Groq

# Cargar variables de entorno
load_dotenv()

# --- CONFIGURACIÓN ---
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_WHATSAPP = os.getenv("TWILIO_WHATSAPP")
TU_WHATSAPP = os.getenv("TU_WHATSAPP")

# Inicializar Groq
groq_client = Groq(api_key=GROQ_API_KEY)

# Inicializar Twilio
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

# --- 1. BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect('gastos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS gastos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, entidad TEXT, 
                  lugar TEXT, beneficiario TEXT, monto REAL, procesado INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# --- 2. LEER CORREOS ---
def obtener_correos_pendientes():
    correos = []
    try:
        remitentes_bancos = [
            'servicioalcliente@netinterbank.com.pe',
            'notificaciones@yape.pe',
            'nuevo_banco@correo.com'  # Agrega aquí
        ]
        
        with MailBox(IMAP_SERVER).login(EMAIL_USER, EMAIL_PASS) as mailbox:
            for remitente in remitentes_bancos:
                for msg in mailbox.fetch(AND(from_=remitente, seen=False)):
                    correos.append({
                        'uid': msg.uid,
                        'cuerpo': msg.text or msg.html,
                        'remitente': msg.from_
                    })
                    mailbox.flag(msg.uid, ['\\Seen'], True)
                    print(f"   ✓ Correo UID {msg.uid} marcado como leído")
    except Exception as e:
        print(f"Error al leer correos: {e}")
    return correos

# --- 3. EXTRAER DATOS CON GROQ (GRATIS Y RÁPIDO) ---
def extraer_datos_ia(texto_correo):
    prompt = f"""
    Eres un asistente financiero experto. Analiza este correo de transacción bancaria.
    Extrae los datos y devuélvelos ESTRICTAMENTE en formato JSON con estas claves exactas:
    - "entidad": (Nombre del banco o billetera)
    - "lugar": (Dónde se hizo el gasto, comercio o plataforma)
    - "fecha": (Fecha del gasto en formato YYYY-MM-DD. Si dice "hoy", usa la fecha actual: {datetime.now().strftime('%Y-%m-%d')})
    - "beneficiario": (A quién se le pagó o nombre del comercio)
    - "monto": (Solo el número del monto gastado, sin símbolos de moneda)
    - "es_gasto_real": (Booleano true/false. Si es un aviso, retención no cobrada o intento de pago, pon false)
    
    Texto del correo:
    {texto_correo}
    """
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error con Groq: {e}")
        return None

# --- 4. GUARDAR Y CALCULAR TOTAL ---
def procesar_y_calcular(datos):
    if not datos.get('es_gasto_real', True):
        print("   ℹ️ Aviso informativo detectado, no se suma como gasto.")
        return None

    try:
        monto = float(datos['monto'])
    except (ValueError, TypeError):
        print(f"   ❌ Monto inválido: {datos['monto']}")
        return None

    conn = sqlite3.connect('gastos.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO gastos (fecha, entidad, lugar, beneficiario, monto) VALUES (?, ?, ?, ?, ?)",
              (datos['fecha'], datos['entidad'], datos['lugar'], datos['beneficiario'], monto))
    
    mes_actual = datetime.now().strftime("%Y-%m")
    c.execute("SELECT SUM(monto) FROM gastos WHERE fecha LIKE ?", (f'{mes_actual}%',))
    total_mes = c.fetchone()[0] or 0.0
    
    conn.commit()
    conn.close()
    return total_mes

# --- 5. ENVIAR WHATSAPP ---
def enviar_whatsapp(datos, total_mes):
    mensaje = f"""
🚨 *NUEVO GASTO DETECTADO* 🚨
🏢 *Entidad:* {datos['entidad']}
📍 *Lugar:* {datos['lugar']}
👤 *Pagado a:* {datos['beneficiario']}
📅 *Fecha:* {datos['fecha']}
💰 *Monto:* S/ {datos['monto']}

📊 *TOTAL GASTADO ESTE MES:* S/ {total_mes:.2f}
"""
    
    try:
        twilio_client.messages.create(
            from_=TWILIO_WHATSAPP,
            body=mensaje,
            to=TU_WHATSAPP
        )
        print("   ✅ Mensaje enviado a WhatsApp")
    except Exception as e:
        print(f"   ❌ Error al enviar WhatsApp: {e}")

# --- FLUJO PRINCIPAL ---
def ejecutar_revision():
    print(f"\n[{datetime.now()}] Revisando correos...")
    init_db()
    correos = obtener_correos_pendientes()
    
    if not correos:
        print("   ✓ No hay correos nuevos.")
        return

    print(f"   📧 Se encontraron {len(correos)} correos nuevos")
    
    for correo in correos:
        print(f"\n   Procesando correo de {correo['remitente']} (UID: {correo['uid']})...")
        datos_extraidos = extraer_datos_ia(correo['cuerpo'])
        
        if datos_extraidos:
            print(f"   🤖 Datos extraídos: {datos_extraidos}")
            total_actual = procesar_y_calcular(datos_extraidos)
            if total_actual is not None:
                enviar_whatsapp(datos_extraidos, total_actual)
        else:
            print("   ❌ No se pudieron extraer datos del correo")

# --- AUTOMATIZACIÓN ---
if __name__ == "__main__":
    print("Bot de Gastos iniciado. Presiona Ctrl+C para detener.")
    print("=" * 60)
    
    ejecutar_revision()
    
    #Puedes cambiar el intervalo de tiempo según tus necesidades
    schedule.every(5).minutes.do(ejecutar_revision)  # Cada 5 minutos
# schedule.every(15).minutes.do(ejecutar_revision)  # Cada 15 minutos
# schedule.every(1).hours.do(ejecutar_revision)     # Cada hora
    while True:
        schedule.run_pending()
        time.sleep(1)