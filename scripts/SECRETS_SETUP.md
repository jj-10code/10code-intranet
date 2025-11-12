# 🔐 Guía de Gestión de Secretos - 10Code Intranet

## ✅ Configuración Completada

La gestión de secretos ha sido optimizada siguiendo el patrón **KISS** (Keep It Simple, Stupid) con seguridad de nivel producción.

---

## 📁 Estructura de Archivos

```bash
10code-intranet/
├── config/
│   └── secrets.py          # ✅ Módulo simplificado de gestión de secretos
├── scripts/                # 🔧 Scripts auxiliares
│   └── validate_secrets.py # 🔍 Script de validación
├── secrets/                # ✅ Carpeta para secretos (permisos 700)
│   ├── secret_key.txt      # ✅ Django SECRET_KEY (permisos 600)
│   ├── db_password.txt     # ✅ PostgreSQL password (permisos 600)
│   └── README.md           # 📖 Documentación de secretos
├── .env                    # ✅ Variables de entorno NO sensibles
└── .gitignore              # ✅ Incluye secrets/ y .env
```

---

## 🎯 Filosofía de Implementación

### ✅ Por qué ARCHIVOS > Variables de Entorno

Para nuestro caso específico (VPS OVHCloud + Docker):

1. **Seguridad en Docker**: Las env vars son visibles con `docker inspect`, los archivos NO
2. **Docker Secrets**: Estándar compatible con Docker Swarm y Kubernetes
3. **No aparecen en procesos**: `ps auxe` no mostrará el contenido de archivos
4. **Permisos granulares**: `chmod 400` (solo lectura) para máxima seguridad
5. **Rotación fácil**: Cambias el archivo sin reconstruir contenedores

### ✅ Simplificación Implementada

**ANTES** (Sobre-ingenierizado):

- ❌ 3 fuentes simultáneas (Docker Secrets, `_FILE` pattern, env vars)
- ❌ Parsing de 5 tipos (string, bool, int, list, json) - NO USADOS
- ❌ Validaciones de DB/Redis URL - NUNCA LLAMADAS
- ❌ ~190 líneas de código complejo

**AHORA** (KISS):

- ✅ 3 fuentes claras con prioridad: Docker → Archivos → Env vars → Default
- ✅ Solo strings (parsing manual si es necesario)
- ✅ Validación mínima pero efectiva del SECRET_KEY
- ✅ ~160 líneas, código limpio y mantenible

---

## 🚀 Cómo Usar

### 1. Desarrollo Local

Los secretos se cargan **automáticamente** desde `secrets/*.txt`:

```python
# config/settings/base.py
from config.secrets import read_secret

# Cargar SECRET_KEY (requerido, sin fallback)
SECRET_KEY = read_secret("secret_key", required=True)

# Cargar DB password (opcional, con fallback)
db_password = read_secret("db_password", required=False, default="postgres")
```

### 2. Producción (Docker)

#### Opción A: Docker Compose con Secrets

```yaml
# docker-compose.yml
version: "3.8"

services:
  web:
    image: 10code-intranet:latest
    secrets:
      - secret_key
      - db_password
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production

secrets:
  secret_key:
    file: ./secrets/secret_key.txt
  db_password:
    file: ./secrets/db_password.txt
```

Los secretos se montarán automáticamente en `/run/secrets/` dentro del contenedor.

#### Opción B: Volumen Montado (VPS)

```yaml
services:
  web:
    image: 10code-intranet:latest
    volumes:
      - /opt/10code/secrets:/run/secrets:ro  # Read-only
```

En el VPS:

```bash
# Crear carpeta de secretos en el VPS
sudo mkdir -p /opt/10code/secrets
sudo chmod 700 /opt/10code/secrets

# Copiar secretos (usa scp, ansible, o copia manual segura)
sudo vim /opt/10code/secrets/secret_key
sudo vim /opt/10code/secrets/db_password

# Permisos restrictivos
sudo chmod 400 /opt/10code/secrets/*
sudo chown root:root /opt/10code/secrets/*
```

---

## 🔄 Prioridad de Carga

El sistema `config/secrets.py` busca secretos en este orden:

```bash
1. /run/secrets/{nombre}        # Docker Secrets (producción)
   ↓ no encontrado
2. secrets/{nombre}.txt         # Archivos locales (desarrollo)
   ↓ no encontrado
3. Variable de entorno {NOMBRE}  # Fallback
   ↓ no encontrado
4. Default (si se especifica)   # Valor por defecto
   ↓ no especificado
5. Error (si required=True)     # Falla con mensaje claro
```

---

## 🛡️ Seguridad

### Permisos Recomendados

```bash
# Carpeta secrets/
chmod 700 secrets/

# Archivos de secretos
chmod 600 secrets/*.txt  # rw------- (solo owner lee/escribe)
# O más restrictivo:
chmod 400 secrets/*.txt  # r-------- (solo owner lee)
```

### Validación

Antes de desplegar, valida la configuración:

```bash
python scripts/validate_secrets.py
```

Salida esperada:

```txt
✅ Carpeta 'secrets/' existe
✅ Archivo secret_key.txt existe y es válido
✅ Archivo db_password.txt existe y es válido
✅ secrets/ está en .gitignore
✅ ¡TODO CORRECTO! La configuración de secretos es válida.
```

---

## 🔄 Rotación de Secretos

### SECRET_KEY

**Cuándo rotar:**

- Cada 90 días (mínimo)
- Después de una brecha de seguridad
- Cuando un desarrollador con acceso deja el equipo

**Cómo rotar:**

```bash
# Generar nueva SECRET_KEY
python -c "import secrets, string; chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'; print(''.join(secrets.choice(chars) for i in range(60)))"

# Actualizar archivo
echo "NUEVA_SECRET_KEY_AQUI" > secrets/secret_key.txt
chmod 600 secrets/secret_key.txt

# Reiniciar aplicación
docker-compose restart web
```

**⚠️ IMPORTANTE:** Rotar SECRET_KEY invalida todas las sesiones activas.

### DATABASE_PASSWORD

**Cómo rotar:**

```bash
# 1. Cambiar password en PostgreSQL
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'nueva_password_segura';"

# 2. Actualizar archivo
echo "nueva_password_segura" > secrets/db_password.txt
chmod 600 secrets/db_password.txt

# 3. Reiniciar aplicación
docker-compose restart web
```

---

## 📋 Checklist de Seguridad

Antes de desplegar a producción:

- [ ] ✅ Secretos están en `secrets/` con permisos `600` o `400`
- [ ] ✅ Carpeta `secrets/` tiene permisos `700`
- [ ] ✅ `secrets/` está en `.gitignore`
- [ ] ✅ `scripts/validate_secrets.py` pasa sin errores
- [ ] ✅ SECRET_KEY tiene mínimo 50 caracteres en producción
- [ ] ✅ SECRET_KEY NO contiene patrones inseguros
- [ ] ✅ DB password es diferente a desarrollo
- [ ] ✅ Secretos de producción NO están en el repositorio Git
- [ ] ✅ Docker Secrets configurado en `docker-compose.yml`
- [ ] ✅ Plan de rotación de secretos documentado
- [ ] ✅ Backup de secretos en lugar seguro (encriptado)

---

## 🐛 Troubleshooting

### Error: "Secret requerido 'secret_key' no encontrado"

**Causa:** No existe el archivo `secrets/secret_key.txt`

**Solución:**

```bash
python -c "import secrets, string; chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'; print(''.join(secrets.choice(chars) for i in range(60)))" > secrets/secret_key.txt
chmod 600 secrets/secret_key.txt
```

### Error: "SECRET_KEY no cumple requisitos de seguridad"

**Causa:** La SECRET_KEY es demasiado corta o contiene patrones inseguros

**Solución:** Genera una nueva SECRET_KEY segura (ver arriba)

### Warning: "Permisos de secrets/ deberían ser 700"

**Causa:** La carpeta tiene permisos demasiado permisivos

**Solución:**

```bash
chmod 700 secrets/
```

### Error: "Permission denied" al leer secretos

**Causa:** El usuario que ejecuta Django no tiene permisos para leer los archivos

**Solución:**

```bash
# Desarrollo local
chmod 600 secrets/*.txt

# Docker (asegura que el usuario del contenedor puede leer)
chown 1000:1000 secrets/*.txt  # Ajusta UID/GID según tu contenedor
```

---

## 🎓 Mejores Prácticas

### ✅ DO

- ✅ Usa archivos para secretos críticos (SECRET_KEY, passwords)
- ✅ Usa variables de entorno para configuración no sensible (DEBUG, ALLOWED_HOSTS)
- ✅ Rota secretos regularmente (cada 90 días)
- ✅ Usa diferentes secretos para dev/staging/prod
- ✅ Valida secretos antes de desplegar
- ✅ Backup de secretos en lugar seguro encriptado (ansible-vault, sops)

### ❌ DON'T

- ❌ NO commitees archivos de `secrets/` al repositorio
- ❌ NO compartas secretos por Slack, email, o herramientas no encriptadas
- ❌ NO uses la misma SECRET_KEY en múltiples entornos
- ❌ NO dejes secretos con permisos 644 o 777
- ❌ NO uses secretos hardcodeados en el código
- ❌ NO olvides rotar secretos después de una brecha

---

## 📚 Referencias

### Documentación

- [Django Settings Best Practices](https://docs.djangoproject.com/en/5.0/topics/settings/)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

### Herramientas Recomendadas

- **Ansible Vault**: Encriptar secretos en repos
- **SOPS**: Encriptar archivos con KMS
- **1Password/Bitwarden**: Gestionar secretos del equipo
- **git-secrets**: Prevenir commits de secretos

---

## 📞 Soporte

Si tienes dudas sobre la gestión de secretos:

1. Revisa este documento
2. Ejecuta `python scripts/validate_secrets.py`
3. Revisa `secrets/README.md`
4. Consulta la documentación de Django

---

**Última actualización:** 2025-11-12
**Responsable:** 10Code DevOps Team
**Estado:** ✅ Implementado y Validado
