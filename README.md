# 🤖 Bot de Gastos WhatsApp

Un bot inteligente que monitorea tu correo electrónico, detecta transacciones de billeteras electrónicas y bancos, y te envía notificaciones automáticas por WhatsApp con el detalle de cada gasto y el total acumulado del mes.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Working-success)

## 📖 Tabla de Contenidos

- [🌟 Características](#-características)
- [🎓 Guía para Principiantes](#-guía-para-principiantes)
- [🛠️ Tecnologías utilizadas](#️-tecnologías-utilizadas)
- [📦 Instalación](#-instalación)
- [⚙️ Configuración](#️-configuración)
- [🚀 Uso](#-uso)
- [📱 Ejemplo de mensaje](#-ejemplo-de-mensaje)
- [🏦 Bancos soportados](#-bancos-soportados)
- [📂 Estructura del proyecto](#-estructura-del-proyecto)
- [🔒 Seguridad](#-seguridad)
- [⚠️ Limitaciones](#️-limitaciones)
- [🔧 Personalización](#-personalización)
- [🐛 Solución de problemas](#-solución-de-problemas)
- [🤝 Contribuciones](#-contribuciones)
- [📝 Licencia](#-licencia)

---

## 🌟 Características

- 📧 **Monitoreo automático** de correos de bancos y billeteras electrónicas
- 🧠 **Extracción inteligente de datos** usando IA (Groq con Llama 3.3)
- 💬 **Notificaciones por WhatsApp** con detalles completos de cada transacción
- 📊 **Cálculo automático** del total gastado en el mes
- 💾 **Base de datos local** (SQLite) para historial de gastos
- ⏰ **Ejecución programada** cada 5 minutos
- 🆓 **100% gratuito** - usa APIs gratuitas (Groq, Twilio Sandbox)

### 📋 Información que extrae

Para cada transacción, el bot identifica:
- 🏢 **Entidad** (banco o billetera)
- 📍 **Lugar** (comercio o plataforma)
- 👤 **Beneficiario** (a quién se pagó)
- 📅 **Fecha** de la transacción
- 💰 **Monto** gastado
- 📊 **Total acumulado** del mes

---

## 🎓 Guía para Principiantes

> **¿Es tu primera vez trabajando con APIs, bots o programación?** ¡No te preocupes! Esta guía te explica TODO paso a paso, desde lo más básico.

### 🤔 ¿Qué es este bot y cómo funciona?

Imagina que tienes un asistente personal que:
1. 📬 Revisa tu correo cada 5 minutos
2. 🔍 Busca correos de tus bancos/billeteras
3. 🧠 Usa Inteligencia Artificial para "leer" el correo y entender qué compraste
4. 💾 Guarda la información en una base de datos
5. 📱 Te envía un mensaje de WhatsApp con el detalle
6. 📊 Te dice cuánto has gastado en total este mes

**¡Eso es exactamente lo que hace este bot!**

### 🔑 ¿Qué es una "API Key" y por qué la necesito?

**API Key** = "Llave de acceso"

Piensa en una API como la puerta de un edificio:
- 🏢 **El edificio** = El servicio (Gmail, Groq, Twilio)
- 🚪 **La puerta** = La API (cómo te conectas)
- 🔑 **La llave** = La API Key (te permite entrar)

**Sin la llave (API Key), no puedes usar el servicio.** Cada servicio te da tu propia llave única.

### 📧 PASO 1: Obtener contraseña de Gmail

**¿Por qué necesito esto?** Para que el bot pueda leer tus correos.

#### ⚠️ IMPORTANTE: NO uses tu contraseña normal de Gmail

Google no permite que aplicaciones usen tu contraseña principal por seguridad. Necesitas crear una **"Contraseña de Aplicación"** especial.

#### 📝 Pasos detallados:

1. **Activa la verificación en 2 pasos** (si no la tienes):
   - Ve a: https://myaccount.google.com/security
   - Busca "Verificación en 2 pasos"
   - Haz clic y sigue los pasos (te pedirá tu número de teléfono)

2. **Genera la contraseña de aplicación**:
   - Ve a: https://myaccount.google.com/apppasswords
   - Inicia sesión si te lo pide
   - En "Nombre de la aplicación" escribe: `Bot Gastos`
   - Haz clic en **"Crear"**
   - Google te mostrará una contraseña de **16 caracteres** (ejemplo: `abcd efgh ijkl mnop`)
   - **¡CÓPIALA!** La necesitarás en el archivo `.env`

3. **Guárdala en un lugar seguro** (no la compartas con nadie)

> 💡 **Tip:** Esta contraseña solo funciona para esta aplicación. Si la pierdes, puedes generar otra.

### 🧠 PASO 2: Obtener API Key de Groq (IA Gratuita)

**¿Por qué necesito esto?** Para que el bot use Inteligencia Artificial para "leer" los correos del banco y extraer la información importante.

#### 📝 Pasos detallados:

1. **Crea una cuenta en Groq**:
   - Ve a: https://console.groq.com/
   - Haz clic en **"Sign in with Google"** (es más rápido)
   - Acepta los permisos

2. **Genera tu API Key**:
   - En el menú lateral izquierdo, haz clic en **"API Keys"**
   - Haz clic en el botón **"Create API Key"**
   - En "Name" escribe: `bot-gastos-whatsapp`
   - Haz clic en **"Submit"**
   - Verás una clave que empieza con `gsk_...`
   - **¡CÓPIALA INMEDIATAMENTE!** Solo se muestra una vez

3. **Pégala en tu archivo `.env`**

> 💡 **Tip:** Groq es 100% gratis y tiene límites muy generosos (14,400 solicitudes al día). Para uso personal, es prácticamente imposible agotarlos.

### 💬 PASO 3: Configurar Twilio para WhatsApp

**¿Por qué necesito esto?** Para que el bot pueda enviarte mensajes de WhatsApp.

#### 📝 Pasos detallados:

1. **Crea una cuenta en Twilio**:
   - Ve a: https://www.twilio.com/try-twilio
   - Regístrate con tu correo
   - Verifica tu número de teléfono

2. **Encuentra tus credenciales**:
   - Inicia sesión en: https://console.twilio.com/
   - En la página principal verás:
     - **Account SID** (empieza con `AC...`) ← Cópialo
     - **Auth Token** (cadena larga) ← Haz clic en "Show" y cópialo

3. **Configura WhatsApp Sandbox**:
   - En el menú lateral, ve a: **Messaging** → **Try it out** → **Try WhatsApp**
   - Verás:
     - **Sandbox number**: Un número como `+1 415 523 8886`
     - **Your join code**: Algo como `join happy-panda`

4. **Vincula tu WhatsApp**:
   - Abre WhatsApp en tu teléfono
   - Envía el código (ej: `join happy-panda`) al número del sandbox
   - Recibirás un mensaje de confirmación ✅

5. **Copia todo en tu archivo `.env`**:
   - `TWILIO_SID` = Tu Account SID
   - `TWILIO_TOKEN` = Tu Auth Token
   - `TWILIO_WHATSAPP` = `whatsapp:+14155238886` (el número del sandbox)
   - `TU_WHATSAPP` = `whatsapp:+51987654321` (tu número real con código de país)

> 💡 **Tip:** El Sandbox de Twilio es gratuito pero solo funciona con números que hayas vinculado previamente enviando el código `join`.

### 🐍 PASO 4: ¿Qué es un "Entorno Virtual" y por qué lo uso?

**Entorno Virtual** = "Una caja aislada para tu proyecto"

Imagina que tienes varios proyectos de Python:
- Proyecto A necesita la versión 1.0 de una librería
- Proyecto B necesita la versión 2.0 de la misma librería

**Sin entorno virtual:** ¡Se mezclarían y causarían conflictos!

**Con entorno virtual:** Cada proyecto tiene su propia "caja" con sus propias librerías, sin interferir con los demás.

#### 📝 Cómo crearlo:

```bash
# Crear el entorno virtual (solo una vez)
python -m venv venv

# Activarlo (cada vez que vayas a trabajar)
# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate