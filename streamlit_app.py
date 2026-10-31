import streamlit as st
import pandas as pd
import base64

# Configuración de la página estilo móvil
st.set_page_config(page_title="Old Riders MC", page_icon="🏍️", layout="centered")

# --- 1. FUNCIÓN PARA CARGAR LA IMAGEN DE FONDO EN BASE64 ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Inicialización del control de estado de la aplicación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_alias" not in st.session_state:
    st.session_state.user_alias = None
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "PRINCIPAL"

# --- 2. CONFIGURACIÓN DINÁMICA DEL FONDO (IMAGEN PERSISTENTE CON OPACIDAD) ---
try:
    img_base64 = get_base64_image("Log.png")
    
    if not st.session_state.authenticated:
        background_style = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: contain;
            background-position: center top;
            background-repeat: no-repeat;
            background-color: #000000;
            background-attachment: fixed;
        }}
        [data-testid="stMainBlockContainer"] {{
            max-width: 450px !important;
            margin: auto;
        }}
        </style>
        """
    else:
        background_style = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), url("data:image/png;base64,{img_base64}");
            background-size: contain;
            background-position: center top;
            background-repeat: no-repeat;
            background-color: #000000;
            background-attachment: fixed;
        }}
        [data-testid="stMainBlockContainer"] {{
            max-width: 800px !important;
        }}
        </style>
        """
except FileNotFoundError:
    background_style = """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    </style>
    """

st.markdown(background_style, unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stHeader"] { 
        background: rgba(0,0,0,0) !important; 
    }
    h1, h2, h3, p, label { 
        color: #FFFFFF !important; 
        font-family: 'Arial Black', Gadget, sans-serif !important;
    }
    
    div[data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }

    div[data-testid="stButton"] button {
        background-color: #000000 !important; 
        color: #FFFFFF !important;            
        font-weight: bold !important;
        font-size: 16px !important;           
        border-radius: 6px !important;        
        border: 3px solid #FFD700 !important; 
        width: 100% !important;               
        padding: 10px 15px !important;        
        margin-top: 8px !important;
        margin-bottom: 8px !important;
        text-transform: uppercase !important; 
        box-shadow: none !important;          
    }

div[data-testid="stButton"] button:hover,
div[data-testid="stButton"] button:hover *,
div[data-testid="stButton"] button:focus *,
div[data-testid="stButton"] button:active * {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-color: #FFD700 !important;
}
    
    div[data-baseweb="input"] {
        background-color: #000000 !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 8px !important;
    }
    input { 
        color: #FFFFFF !important; 
        background-color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Enlaces a Google Sheets
SHEET_ID = "1GXjpYr5nCrRH4wHI9RtKJQ3YUSv2sXcjZqWWL0kPoQA"
URL_USUARIOS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Usuarios"
URL_SALIDAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Salidas"
URL_ECONOMIA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Economia"
URL_NORMATIVA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Normativa"
URL_CAT_NORMAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Cat_Normas" 
URL_REUNIONES = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Reuniones" 

# --- PANTALLA 1: LOGIN ---
if not st.session_state.authenticated:
    st.write("<br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    usuario_input = st.text_input("Usuario (Email)").strip().lower()
    contrasena_input = st.text_input("Contraseña", type="password")
    
    if st.button("ENTRAR"):
        try:
            df_usuarios = pd.read_csv(URL_USUARIOS)
            df_usuarios.columns = df_usuarios.columns.str.strip()
            col_usuario = 'Usuario' if 'Usuario' in df_usuarios.columns else 'Email'
            usuario_valido = df_usuarios[df_usuarios[col_usuario].astype(str).str.strip().str.lower() == usuario_input]
            
            if not usuario_valido.empty:
                pwd_correcta = True
                if 'Contrasena' in df_usuarios.columns:
                    pwd_correcta = str(usuario_valido.iloc[0]['Contrasena']).strip() == contrasena_input
                else:
                    pwd_correcta = contrasena_input == "1234"
                
                if pwd_correcta:
                    st.session_state.authenticated = True
                    st.session_state.user_role = usuario_valido.iloc[0]['Rol'].strip()
                    st.session_state.user_alias = usuario_valido.iloc[0]['Alias']
                    st.session_state.current_menu = "PRINCIPAL"
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")
            else:
                st.error("El usuario no está registrado")
        except Exception as e:
            st.error("Error al conectar con la base de datos.")

# --- PANTALLA 2: NAVEGACIÓN GENERAL (ZONA AUTENTICADA) ---
else:
    rol = st.session_state.user_role

    # === 1. MENÚ PRINCIPAL ===
    if st.session_state.current_menu == "PRINCIPAL":
        st.title("MENÚ PRINCIPAL")
        st.write(f"Bienvenido, **{st.session_state.user_alias}**")
        st.write(f"Cargo: **{st.session_state.user_role}**")
        
        if st.button("CLUB"):
            st.session_state.current_menu = "CLUB_MENU"
            st.rerun()

        if st.button("SALIDAS"):
            st.session_state.current_menu = "PANTALLA_SALIDAS"
            st.rerun()
                
        if rol in ["Presidente", "Vicepresidente", "Tesorero", "Secretario", "Administrador"]:
            if st.button("ECONOMÍA"):
                st.session_state.current_menu = "PANTALLA_ECONOMIA"
                st.rerun()
                    
        if st.button("MERCHANDISING"):
            st.session_state.current_menu = "PANTALLA_MERCHANDISING"
            st.rerun()
            
        if st.button("Cerrar Sesión"):
            st.session_state.authenticated = False
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    # === 2. PANTALLA: MENÚ CLUB ===
    elif st.session_state.current_menu == "CLUB_MENU":
        st.title("CLUB")
        
        if st.button("REUNIONES"):
            st.session_state.current_menu = "REUNIONES_MENU"
            st.rerun()
            
        if st.button("OLD RIDERS"):
            st.session_state.current_menu = "OLD_RIDERS_MENU"
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    # === 3. PANTALLA: SUBMENÚ OLD RIDERS ===
    elif st.session_state.current_menu == "OLD_RIDERS_MENU":
        st.title("OLD RIDERS")
        
        if st.button("NORMATIVA"):
            st.session_state.current_menu = "NORMATIVA_VER"
            st.rerun()
            
        if st.button("HISTORIA"):
            st.session_state.current_menu = "HISTORIA_VER"
            st.rerun()
            
        if st.button("USUARIOS"):
            st.session_state.current_menu = "USUARIOS_FICHA"
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.current_menu = "CLUB_MENU"
            st.rerun()

    # === 4. PANTALLA: DETALLE DE LOS MIEMBROS (USUARIOS) ===
    elif st.session_state.current_menu == "USUARIOS_FICHA":
        st.title("👤 DATOS DE LOS MIEMBROS")
        
        puede_editar = rol in ["Presidente", "Vicepresidente", "Administrador"]
        if puede_editar:
            st.success("🔓 Modo Edición Activado (Tienes permisos para modificar datos)")
        else:
            st.info("🔒 Modo Consulta (Solo los oficiales autorizados pueden modificar datos)")
            
        st.write("---")

        try:
            df_usuarios = pd.read_csv(URL_USUARIOS)
            df_usuarios.columns = df_usuarios.columns.str.strip()
            
            col_identificador = 'Alias' if 'Alias' in df_usuarios.columns else 'Nombre'
            df_usuarios[col_identificador] = df_usuarios[col_identificador].astype(str).str.strip()
            
            lista_miembros = sorted(df_usuarios[col_identificador].unique())
            miembro_sel = st.selectbox("Selecciona un miembro para gestionar su ficha:", ["-- Seleccionar miembro --"] + lista_miembros)
            
            st.write("---")
            
            if miembro_sel != "-- Seleccionar miembro --":
                datos_miembro = df_usuarios[df_usuarios[col_identificador] == miembro_sel].iloc[0]
                bloqueado = not puede_editar
                col1, col2 = st.columns(2)
                with col1:
st.subheader("Datos de Identidad")
nombre = st.text_input("Nombre Real", value=str(datos_miembro.get('Nombre', '')), disabled=bloqueado)
apellido = st.text_input("Apellido", value=str(datos_miembro.get('Apellido', '')), disabled=bloqueado)
alias = st.text_input("Alias en el Club", value=str(datos_miembro.get('Alias', miembro_sel)), disabled=bloqueado)
email = st.text_input("Email / Usuario", value=str(datos_miembro.get('Usuario', datos_miembro.get('Email', ''))), disabled=bloqueado)
telefono = st.text_input("Teléfono", value=str(datos_miembro.get('Telefono', '')), disabled=bloqueado)

if puede_editar:
contrasena = st.text_input("Contraseña Acceso App", value=str(datos_miembro.get('Contrasena', '')), type="password")
with col2:
st.subheader("Estado y Fechas")
lista_cargos = ["Presidente", "Vicepresidente", "Secretario", "Tesorero", "Capitán de Ruta", "Sargento de Armas", "Miembro", "Prospect", "Handground"]
cargo_actual = str(datos_miembro.get('Rol', datos_miembro.get('Cargo', 'Miembro'))).strip()
idx_cargo = lista_cargos.index(cargo_actual) if cargo_actual in lista_cargos else 6
cargo = st.selectbox("Cargo / Rol", lista_cargos, index=idx_cargo, disabled=bloqueado)
inicio = st.text_input("Fecha Inicio (DD/MM/AAAA)", value=str(datos_miembro.get('Inicio', '')), disabled=bloqueado)
final = st.text_input("Fecha Final / Baja", value=str(datos_miembro.get('Final', '')), disabled=bloqueado)
estado = st.text_input("Estado (Activo / Inactivo)", value=str(datos_miembro.get('Estado', 'Activo')), disabled=bloqueado)
saldo = st.text_input("Saldo de Cuentas (€)", value=str(datos_miembro.get('Saldo', '0.00')), disabled=bloqueado)
st.write("---")
st.subheader("Sección de Notas Internas")
observaciones = st.text_area("Observaciones del Miembro", value=str(datos_miembro.get('Observaciones', '')), disabled=bloqueado)
if puede_editar:
if st.button("💾 GUARDAR Y ACTUALIZAR CAMBIOS"):
st.info("Conectando con Google Sheets para aplicar cambios...")
except Exception as e:
st.error(f"Error de lectura en la hoja 'Usuarios': {e}")
if st.button("⬅️ VOLVER"):
st.session_state.current_menu = "OLD_RIDERS_MENU"
st.rerun()
# === VISTAS DE CONTENIDO MACRO (Aisladas para que no rompan botones) ===
elif st.session_state.current_menu == "PANTALLA_SALIDAS":
st.subheader("Calendario de Rutas")
try:
df_salidas = pd.read_csv(URL_SALIDAS)
st.dataframe(df_salidas)
except:
st.write("No hay rutas programadas todavía.")
if st.button("VOLVER"):
st.session_state.current_menu = "PRINCIPAL"
st.rerun()
elif st.session_state.current_menu == "PANTALLA_ECONOMIA":
st.subheader("Control Financiero del Club")
try:
df_economia = pd.read_csv(URL_ECONOMIA)
st.dataframe(df_economia)
except:
st.write("No hay registros financieros.")
if st.button("VOLVER"):
st.session_state.current_menu = "PRINCIPAL"
st.rerun()
elif st.session_state.current_menu == "PANTALLA_MERCHANDISING":
st.subheader("Tienda y Pedidos")
st.write("Gestión de stock, chalecos, parches y camisetas.")
if st.button("VOLVER"):
st.session_state.current_menu = "PRINCIPAL"
st.rerun()
# Marcadores de posición para el resto de pantallas (Normativa, Historia, etc.)
elif st.session_state.current_menu in ["REUNIONES_MENU", "NORMATIVA_VER", "HISTORIA_VER"]:
st.title(st.session_state.current_menu.replace("_", " "))
st.info("Sección temporalmente en desarrollo...")
if st.button("VOLVER"):
st.session_state.current_menu = "OLD_RIDERS_MENU" if "MENU" not in st.session_state.current_menu else "CLUB_MENU"
st.rerun()
