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

# --- 2. CONFIGURACIÓN DINÁMICA DEL FONDO (IMAGEN PERSISTENTE CON OPACIDAD) ---
try:
    img_base64 = get_base64_image("Log.png")
    
    if not st.session_state.authenticated:
        # PANTALLA DE LOGIN: Imagen al 100% de brillo y contenedor estrecho (estilo móvil)
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
        # MENÚ PRINCIPAL: La misma imagen fija de fondo, pero con una capa negra semi-transparente encima (Opacidad)
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
            max-width: 800px !important; /* Ancho ampliado para leer bien tablas y datos */
        }}
        </style>
        """
except FileNotFoundError:
    background_style = """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    </style>
    """

# Inyectamos el estilo de pantalla correspondiente
st.markdown(background_style, unsafe_allow_html=True)

# Transparencia obligatoria para la barra superior en ambas pantallas
st.markdown("""
    <style>
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ESTILOS VISUALES GENERALES PARA COMPONENTES ---
st.markdown("""
    <style>
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
        margin-top: 15px !important;
        margin-bottom: 15px !important;
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

# --- COMPLETAMENTE CORREGIDO: Enlaces oficiales a Google Sheets ---
SHEET_ID = "1GXjpYr5nCrRH4wHI9RtKJQ3YUSv2sXcjZqWWL0kPoQA"
URL_USUARIOS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Usuarios"
URL_SALIDAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Salidas"
URL_ECONOMIA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Economia"


# --- PANTALLA 1: LOGIN ---
if not st.session_state.authenticated:
    # Genera saltos de línea para empujar las cajas encima de los recuadros blancos de Log.png
    st.write("<br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    
    usuario_input = st.text_input("Usuario (Email)").strip().lower()
    contrasena_input = st.text_input("Contraseña", type="password")
    
    if st.button("ENTRAR"):
        try:
            # Leemos los usuarios en tiempo real desde Google Sheets
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
                    st.session_state.user_role = usuario_valido.iloc[0]['Rol']
                    st.session_state.user_alias = usuario_valido.iloc[0]['Alias']
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")
            else:
                st.error("El usuario no está registrado en el Moto Club")
        except Exception as e:
            st.error("Error al conectar con la base de datos. Verifica el Google Sheets.")

# --- PANTALLA 2: MENÚ PRINCIPAL ---
else:
    st.title("MENÚ PRINCIPAL")
    st.write(f"Bienvenido, **{st.session_state.user_alias}**")
    st.write(f"Cargo: **{st.session_state.user_role}**")
    
    rol = st.session_state.user_role
    
    # 1. BOTÓN CLUB
    if st.button("CLUB"):
        st.subheader("Información del Club")
        st.write("Sección de historia, estatutos y datos internos.")

    # 2. BOTÓN SALIDAS
    if st.button("SALIDAS"):
        st.subheader("Calendario de Rutas")
        try:
            df_salidas = pd.read_csv(URL_SALIDAS)
            st.dataframe(df_salidas)
        except:
            st.write("No hay rutas programadas todavía.")
            
    # 3. BOTÓN ECONOMÍA (Restringido por rol)
    if rol in ["Presidente", "Vicepresidente", "Tesorero", "Secretario", "Administrador"]:
        if st.button("ECONOMÍA"):
            st.subheader("Control Financiero del Club")
            try:
                df_economia = pd.read_csv(URL_ECONOMIA)
                st.dataframe(df_economia)
            except:
                st.write("No hay registros financieros.")
                
    # 4. BOTÓN MERCHANDISING
    if st.button("MERCHANDISING"):
        st.subheader("Tienda y Pedidos")
        st.write("Gestión de stock, chalecos, parches y camisetas.")
        
    # Cerrar Sesión
    if st.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.user_alias = None
        st.rerun()

