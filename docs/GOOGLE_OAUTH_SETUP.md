# Configuración de Google OAuth para 10Code Intranet

Este documento describe cómo configurar Google OAuth 2.0 para la autenticación en la Intranet de 10Code.

## Requisitos previos

- Acceso a [Google Cloud Console](https://console.cloud.google.com/)
- Cuenta de Google Workspace para 10Code (@10code.es)
- Permisos de administrador del proyecto en Google Cloud

## Paso 1: Crear un proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente:
   - Click en el selector de proyectos (arriba izquierda)
   - Click en "Nuevo proyecto"
   - Nombre: `10Code Intranet`
   - Organización: 10Code
   - Click en "Crear"

## Paso 2: Habilitar la API de Google+

1. En el menú lateral, ve a "APIs y servicios" > "Biblioteca"
2. Busca "Google+ API"
3. Click en "Google+ API"
4. Click en "Habilitar"

**Nota**: Aunque Google+ está deprecado, la API sigue siendo necesaria para obtener información del perfil.

Alternativamente, habilita:
- **Google People API** (recomendado)
- **Google Identity Toolkit API**

## Paso 3: Configurar la pantalla de consentimiento OAuth

1. Ve a "APIs y servicios" > "Pantalla de consentimiento de OAuth"
2. Selecciona el tipo de usuario:
   - **Interno** (recomendado): Solo usuarios de 10code.es
   - Si seleccionas Externo, deberás configurar usuarios de prueba
3. Completa la información de la aplicación:

   **Información de la aplicación**:
   - Nombre de la aplicación: `10Code Intranet`
   - Correo electrónico de asistencia: `admin@10code.es`
   - Logo de la aplicación: (opcional) Sube el logo de 10Code

   **Dominio de la aplicación**:
   - Dominio de aplicación: `intranet.10code.es` (o tu dominio)
   - Enlace a la Política de privacidad: `https://10code.es/privacy` (si existe)
   - Enlace a las Condiciones del servicio: `https://10code.es/terms` (si existe)

   **Información de contacto del desarrollador**:
   - Correo electrónico: `jmarquez@10code.es`

4. Click en "Guardar y continuar"

5. **Alcances (Scopes)**:
   - Click en "Agregar o quitar alcances"
   - Selecciona los siguientes alcances:
     - `.../auth/userinfo.email`
     - `.../auth/userinfo.profile`
     - `openid`
   - Click en "Actualizar"

6. **Usuarios de prueba** (solo si es Externo):
   - Agrega los emails @10code.es que necesiten acceso inicial
   - Ejemplo: `jmarquez@10code.es`

7. Click en "Guardar y continuar"

8. Revisa el resumen y click en "Volver al panel"

## Paso 4: Crear credenciales OAuth 2.0

1. Ve a "APIs y servicios" > "Credenciales"
2. Click en "Crear credenciales" > "ID de cliente de OAuth"
3. Configura el cliente OAuth:

   **Tipo de aplicación**: Aplicación web

   **Nombre**: `10Code Intranet - Web Client`

   **Orígenes de JavaScript autorizados**:
   - Desarrollo: `http://localhost:8000`
   - Producción: `https://intranet.10code.es`

   **URIs de redirección autorizados**:
   - Desarrollo: `http://localhost:8000/accounts/google/login/callback/`
   - Producción: `https://intranet.10code.es/accounts/google/login/callback/`

   **IMPORTANTE**: La URL de callback DEBE terminar en `/` y seguir el formato exacto de django-allauth.

4. Click en "Crear"

5. Guarda las credenciales:
   - **ID de cliente**: Cópialo (ejemplo: `123456789-abcdef.apps.googleusercontent.com`)
   - **Secreto del cliente**: Cópialo (ejemplo: `GOCSPX-abc123...`)

   **IMPORTANTE**: Guarda estas credenciales en un lugar seguro.

## Paso 5: Configurar credenciales en Django

### Opción A: Variables de entorno (Desarrollo)

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Google OAuth Credentials
GOOGLE_CLIENT_ID=123456789-abcdef.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123...
```

### Opción B: Secrets (Recomendado para Producción)

Crea archivos en `secrets/`:

```bash
mkdir -p secrets
chmod 700 secrets

# Crear archivo con Client ID
echo "123456789-abcdef.apps.googleusercontent.com" > secrets/google_client_id.txt
chmod 600 secrets/google_client_id.txt

# Crear archivo con Client Secret
echo "GOCSPX-abc123..." > secrets/google_client_secret.txt
chmod 600 secrets/google_client_secret.txt
```

**IMPORTANTE**: Asegúrate de que `secrets/` esté en `.gitignore`.

## Paso 6: Configurar Social App en Django Admin

1. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

2. Ve a `http://localhost:8000/admin/`

3. Inicia sesión con un superusuario (créalo si no existe):
   ```bash
   python manage.py createsuperuser --email admin@10code.es
   ```

4. Ve a "Sites" (django.contrib.sites):
   - Edita el sitio con ID=1
   - Cambiar el dominio: `localhost:8000` (desarrollo) o `intranet.10code.es` (producción)
   - Cambiar el nombre: `10Code Intranet`
   - Guardar

5. Ve a "Social applications" (allauth):
   - Click en "Agregar Social application"
   - Provider: `Google`
   - Name: `Google OAuth - 10Code`
   - Client id: (pega el ID de cliente de Google)
   - Secret key: (pega el secreto de cliente de Google)
   - Sites: Selecciona `localhost:8000` o `intranet.10code.es`
   - Guardar

## Paso 7: Probar la autenticación

1. Cierra sesión del admin
2. Ve a `http://localhost:8000/login/`
3. Click en "Login con Google"
4. Selecciona tu cuenta @10code.es
5. Autoriza la aplicación
6. Deberías ser redirigido al dashboard

## Solución de problemas

### Error: `redirect_uri_mismatch`

**Causa**: La URI de redirección no coincide con las configuradas en Google Cloud Console.

**Solución**:
1. Verifica que la URI en Google Cloud Console sea exactamente:
   ```
   http://localhost:8000/accounts/google/login/callback/
   ```
2. Asegúrate de que termine con `/`
3. Verifica que el protocolo sea correcto (`http` vs `https`)

### Error: `invalid_client`

**Causa**: Client ID o Secret incorrecto.

**Solución**:
1. Verifica que las credenciales en Django Admin coincidan exactamente con las de Google Cloud Console
2. Revisa que no haya espacios en blanco al inicio o final

### Error: `access_denied` - Dominio no autorizado

**Causa**: El email no es de @10code.es.

**Solución**:
- Solo se permiten usuarios con email @10code.es
- Verifica que estés usando la cuenta correcta

### No redirige después del login

**Causa**: `SITE_ID` incorrecto o sitio no configurado.

**Solución**:
1. Verifica `SITE_ID = 1` en settings
2. Asegúrate de que el sitio con ID=1 esté configurado en Django Admin

## Producción

Para producción:

1. **Actualiza las URIs en Google Cloud Console**:
   - Origen: `https://intranet.10code.es`
   - Redirect URI: `https://intranet.10code.es/accounts/google/login/callback/`

2. **Configura el sitio en Django Admin**:
   - Dominio: `intranet.10code.es`
   - Nombre: `10Code Intranet`

3. **Usa Docker Secrets** para credenciales:
   ```yaml
   # compose.yml
   secrets:
     google_client_id:
       file: ./secrets/google_client_id.txt
     google_client_secret:
       file: ./secrets/google_client_secret.txt
   ```

## Referencias

- [Django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
