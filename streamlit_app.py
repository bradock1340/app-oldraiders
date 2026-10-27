import streamlit as st
import pandas as pd
import base64

# Configuración de la página estilo móvil
st.set_page_config(page_title="Old Raiders MC", page_icon="🏍️", layout="centered")

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
    [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
    h1, h2, h3, p, label { 
        color: #FFFFFF !important; 
        font-family: 'Arial Black', Gadget, sans-serif !important;
    }
    div[data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    .stButton>button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        height: 50px !important;
        font-size: 18px !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
    }
    .stButton>button:hover { 
        background-color: #FFFFFF !important; 
        color: #000000 !important; 
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

# --- PANTALLA 2: MENÚ PRINCIPAL Y SUBMENÚS ---
else:
    rol = st.session_state.user_role

    # ================= SUBMENÚ: CLUB =================
    if st.session_state.current_menu == "CLUB":
        st.title("CLUB")
        
        # Filtro de seguridad: Secretario y Tesorero no ven rutas ni eventos, pero Directiva ve todo
        if rol in ["Presidente", "Vicepresidente", "Tesorero", "Secretario", "Administrador"]:
            if st.button("ECONOMÍA"):
                st.session_state.current_menu = "ECONOMIA_MENU"
                st.rerun()
                
        if st.button("REUNIONES"):
            st.session_state.current_menu = "REUNIONES"
            st.rerun()
            
        if st.button("OLD RAIDERS"):
            st.session_state.current_menu = "OLD_RAIDERS"
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    # ================= SECCIÓN: ECONOMÍA =================
    elif st.session_state.current_menu == "ECONOMIA_MENU":
        st.title("ECONOMÍA")
        if st.button("MENSUALIDADES"):
            st.subheader("Control de Mensualidades")
            # Aquí irá la lógica de la tabla de mensualidades
        if st.button("OTROS PAGOS"):
            st.subheader("Otros Pagos (Bar, Colores, etc.)")
        if st.button("TOTAL DINERO"):
            st.subheader("Balance Económico Total")
        if st.button("VOLVER"):
            st.session_state.current_menu = "CLUB"
            st.rerun()

    # ================= SUBMENÚ: SALIDAS =================
    elif st.session_state.current_menu == "SALIDAS":
        st.title("SALIDAS")
        
        # Permitido introducir rutas a roles autorizados
        if rol in ["Presidente", "Vicepresidente", "Secretario", "Capitán de Ruta", "Administrador"]:
            if st.button("AÑADIR NUEVA RUTA"):
                st.subheader("Formulario de Nueva Ruta")
                
        if st.button("PRÓXIMAS SALIDAS"):
            st.subheader("Calendario de Próximas Rutas")
            
        if st.button("SALIDAS REALIZADAS (HISTORIAL)"):
            st.subheader("Historial de Rutas Completo")
            
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    # ================= SUBMENÚ: USUARIOS =================
    elif st.session_state.current_menu == "USUARIOS":
        st.title("USUARIOS")
        if st.button("DATOS DE LOS MIEMBROS"):
            st.subheader("Fichas de Socios")
        if st.button("DATOS DE SALIDAS REALIZADAS"):
            st.subheader("Asistencia a Rutas")
        if st.button("DATOS DE PAGOS AL DÍA"):
            st.subheader("Estado de Cuentas")
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    # ================= SUBMENÚ: MERCHANDISING =================
    elif st.session_state.current_menu == "MERCHANDISING":
        st.title("MERCHANDISING")
        if st.button("NUEVO PRODUCTO"):
            st.subheader("Alta de Inventario")
        if st.button("NUEVO PEDIDO"):
            st.subheader("Formulario de Pedidos")
        if st.button("LISTADO DE PRODUCTOS"):
            st.subheader("Stock Actual")
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    # ================= MENÚ PRINCIPAL DE BOTONES =================
    else:
        st.title("MENÚ PRINCIPAL")
        st.write(f"Bienvenido, **{st.session_state.user_alias}** — ({rol})")
        
        # Muestra la navegación principal calcada al PDF
        if st.button("CLUB"):
            st.session_state.current_menu = "CLUB"
            st.rerun()
            
        if st.button("SALIDAS"):
            st.session_state.current_menu = "SALIDAS"
            st.rerun()
            
        if st.button("USUARIOS"):
            st.session_state.current_menu = "USUARIOS"
            st.rerun()
            
        if st.button("MERCHANDISING"):
            st.session_state.current_menu = "MERCHANDISING"
            st.rerun()
            
        if st.button("CERRAR SESIÓN"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.user_alias = None
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()
