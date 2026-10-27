import streamlit as st
import pandas as pd
import base64

# Configuración de la página estilo móvil
st.set_page_config(page_title="Old Raiders MC", page_icon="🏍️", layout="centered")

# --- 1. FUNCIÓN PARA CARGAR LA IMAGEN DE FONDO EN BASE64 ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Intentamos cargar 'Log.png' para el fondo completo
try:
    img_base64 = get_base64_image("Log.png")
    background_style = f"""
    <style>
    /* Fondo de pantalla completa con la imagen del club */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center top;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* Cabecera transparente para que no corte el logo superior */
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
    """
except FileNotFoundError:
    # Si por alguna razón borras la imagen, se queda en fondo negro plano
    background_style = """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    </style>
    """

# --- 2. ESTILOS VISUALES PERSONALIZADOS ---
st.markdown(background_style, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Estilos globales de texto (Blanco e importante) */
    h1, h2, h3, p, label { 
        color: #FFFFFF !important; 
        font-family: 'Arial Black', Gadget, sans-serif !important;
    }
    
    /* Forzar mayúsculas y espaciado en las etiquetas de los inputs */
    div[data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    
    /* Botón Dorados estilo Old Raiders */
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
    
    /* Inputs oscuros con borde dorado fino */
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

# URL base de tu Google Sheets (transformada para exportar en CSV automáticamente)
SHEET_ID = "1GXjpYr5nCrRH4wHI9RtKJQ3YUSv2sXcjZqWWL0kPoQA"
URL_USUARIOS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Usuarios"
URL_SALIDAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Salidas"
URL_ECONOMIA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Economia"

# Control de estado de la aplicación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_alias" not in st.session_state:
    st.session_state.user_alias = None

# --- PANTALLA 1: LOGIN ---
if not st.session_state.authenticated:
    # Espaciadores transparentes para empujar las cajas hacia abajo de la calavera
    st.write("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    
    usuario_input = st.text_input("Usuario (Email)").strip().lower()
    contrasena_input = st.text_input("Contraseña", type="password")
    
    if st.button("ENTRAR"):
        try:
            # Leemos los usuarios en tiempo real desde tu Google Sheets
            df_usuarios = pd.read_csv(URL_USUARIOS)
            
            # Limpiamos nombres de columnas por si acaso hay espacios en blanco
            df_usuarios.columns = df_usuarios.columns.str.strip()
            
            # Buscamos si el usuario introducido existe en la columna 'Usuario' o 'Email'
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
    
    # 1. BOTÓN CLUB (Visible para todos)
    if st.button("CLUB"):
        st.subheader("Información del Club")
        st.write("Sección de historia, estatutos y datos internos.")

    # 2. BOTÓN SALIDAS (Visible para todos)
    if st.button("SALIDAS"):
        st.subheader("Calendario de Rutas")
        try:
            df_salidas = pd.read_csv(URL_SALIDAS)
            st.dataframe(df_salidas)
        except:
            st.write("No hay rutas programadas todavía.")
            
    # 3. BOTÓN ECONOMÍA (Estricto: Solo Directiva y Tesorero)
    if rol in ["Presidente", "Vicepresidente", "Tesorero", "Secretario", "Administrador"]:
        if st.button("ECONOMÍA"):
            st.subheader("Control Financiero del Club")
            try:
                df_economia = pd.read_csv(URL_ECONOMIA)
                st.dataframe(df_economia)
            except:
                st.write("No hay registros financieros.")
                
    # 4. BOTÓN MERCHANDISING (Visible para todos)
    if st.button("MERCHANDISING"):
        st.subheader("Tienda y Pedidos")
        st.write("Gestión de stock, chalecos, parches y camisetas.")
        
    if st.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.user_alias = None
        st.rerun()

