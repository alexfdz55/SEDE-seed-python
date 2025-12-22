# 🚀 Deployment - Streamlit App

## Opciones de Deployment

### 1️⃣ Railway (Recomendado - Más Fácil)

**Pasos:**

1. **Crear cuenta en Railway**: https://railway.app

2. **Conectar repositorio Git:**
   - Push tu proyecto a GitHub
   - En Railway: New Project > Deploy from GitHub repo
   - Selecciona tu repositorio

3. **Railway detectará automáticamente:**
   - `requirements.txt` ✓
   - `Procfile` ✓

4. **Configurar variable de entorno PORT:**
   - En Railway dashboard: Variables → Add Variable
   - Nombre: `PORT`
   - Valor: `8501` (o el puerto que Railway asigne automáticamente)
   - **Importante**: Railway asignará automáticamente el puerto correcto. Si hay error, verifica que Railway haya asignado la variable `PORT`.

5. **Deploy automático:**
   - Railway construirá y desplegará automáticamente
   - Te dará una URL pública: `https://tu-app.railway.app`
   - Si ves errores de puerto, ve a Settings → Networking y verifica el puerto público

**Costo:** ~$5/mes después de créditos gratuitos

---

### 2️⃣ Dokploy (Self-Hosted)

**Prerrequisitos:**
- VPS con Ubuntu (DigitalOcean, Hetzner, AWS, etc.)
- Dokploy instalado: https://dokploy.com/docs/get-started/installation

**Pasos:**

1. **Instalar Dokploy en tu VPS:**
   ```bash
   curl -sSL https://dokploy.com/install.sh | sh
   ```

2. **Acceder al panel de Dokploy:**
   - http://tu-vps-ip:3000

3. **Crear nueva aplicación:**
   - Type: Docker
   - Git Repository: Conecta tu repo de GitHub
   - Build Type: Dockerfile
   - Port: 8501

4. **Deploy:**
   - Dokploy construirá usando el `Dockerfile`
   - Configurar dominio con Traefik (incluido)

**Costo:** VPS $5-10/mes (la app es gratis)

---

### 3️⃣ Streamlit Cloud (Más Fácil - Gratis)

**Pasos:**

1. **Crear cuenta**: https://share.streamlit.io

2. **Deploy directo desde GitHub:**
   - New app
   - Conectar repositorio
   - Seleccionar `app_streamlit.py`
   - Deploy!

3. **URL pública automática:**
   - `https://usuario-repo.streamlit.app`

**Limitaciones:**
- Debe ser repositorio público (o pagar)
- Recursos limitados (1 CPU, 800 MB RAM)

**Costo:** Gratis para repos públicos

---

### 4️⃣ Render

**Similar a Railway:**

1. Cuenta en: https://render.com
2. New Web Service > Conectar GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0`

**Costo:** Free tier disponible (lento), Paid desde $7/mes

---

## 📋 Checklist antes de Deploy

- [x] `requirements.txt` actualizado
- [x] `Procfile` creado (Railway/Render)
- [x] `Dockerfile` creado (Dokploy/Docker)
- [x] `.dockerignore` configurado
- [x] `.streamlit/config.toml` configurado
- [ ] Push a GitHub
- [ ] Archivo Excel de prueba (si quieres incluir uno de ejemplo)

---

## 🔐 Seguridad en Producción

### Agregar autenticación (opcional):

1. **Instalar:**
   ```bash
   pip install streamlit-authenticator
   ```

2. **Agregar al `app_streamlit.py`:**
   ```python
   import streamlit_authenticator as stauth
   
   # Configurar usuarios
   names = ['Admin', 'Usuario']
   usernames = ['admin', 'user']
   passwords = ['admin123', 'user123']  # Usar hashes en producción
   
   hashed_passwords = stauth.Hasher(passwords).generate()
   
   authenticator = stauth.Authenticate(
       names, usernames, hashed_passwords,
       'app_name', 'secret_key', cookie_expiry_days=30
   )
   
   name, authentication_status, username = authenticator.login('Login', 'main')
   
   if authentication_status:
       # Tu app aquí
       pass
   elif authentication_status == False:
       st.error('Usuario/contraseña incorrectos')
   ```

---

## 🌐 URLs de Ejemplo

Según la plataforma elegida tendrás:

- **Railway**: `https://seed-validator-production.up.railway.app`
- **Streamlit Cloud**: `https://usuario-seed-python.streamlit.app`
- **Dokploy**: `https://validator.tudominio.com`
- **Render**: `https://seed-validator.onrender.com`

---

## 📊 Comparación Rápida

| Plataforma | Dificultad | Setup | Costo | Mejor para |
|---|:---:|---|---|---|
| **Streamlit Cloud** | ⭐ | 5 min | Gratis | Demos, prototipos |
| **Railway** | ⭐⭐ | 10 min | $5/mes | Producción pequeña |
| **Render** | ⭐⭐ | 10 min | Free/7$ | Alternativa a Railway |
| **Dokploy** | ⭐⭐⭐ | 30 min | VPS | Control total |

---

## 🆘 Soporte

Si tienes problemas con el deployment:
1. Verificar logs en la plataforma
2. Verificar que `requirements.txt` tenga todas las dependencias
3. Verificar que el puerto sea configurable (variable `$PORT`)

---

**¡Listo para producción! 🚀**
