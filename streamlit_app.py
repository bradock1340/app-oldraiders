import streamlit as st
import pandas as pd
import base64

# Configuración de la página estilo móvil
st.set_page_config(page_title="Old Raiders MC", page_icon="🏍️", layout="centered")

# --- 1. FUNCIÓN PARA EL FONDO ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Control de las pantallas
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_alias" not in st.session_state:
    st.session_state.user_alias = None
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "PRINCIPAL"

# --- 2. PONER LA IMAGEN DE FONDO MÁS OPACA ---
try:
    img_base64 = get_base64_image("Log.png")
    if not st.session_state.authenticated:
        # Login: Imagen normal al fondo
        bg_style = f'background-image: url("data:image/png;base64,{img_base64}"); background-size: contain; max-width: 450px !important;'
    else:
        # Menú: Imagen oscurecida al fondo para poder leer bien
        bg_style = f'background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("data:image/png;base64,{img_base64}"); background-size: contain; max-width: 800px !important;'
    
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{ {bg_style} background-position: center top; background-repeat: no-repeat; background-color: #000000; background-attachment: fixed; }}
        [data-testid="stHeader"] {{ background: rgba(0,0,0,0) !important; }}
        h1, h2, h3, p, label {{ color: #FFFFFF !important; font-family: 'Arial Black', Gadget, sans-serif !important; }}
        div[data-testid="stWidgetLabel"] p {{ font-size: 16px !important; letter-spacing: 2px !important; text-transform: uppercase !important; }}
        .stButton>button {{ background-color: #D4AF37 !important; color: #000000 !important; font-weight: bold !important; border-radius: 8px !important; border: none !important; width: 100% !important; height: 50px !important; margin-top: 10px !important; margin-bottom: 10px !important; }}
        .stButton>button:hover {{ background-color: #FFFFFF !important; color: #000000 !important; }}
        div[data-baseweb="input"] {{ background-color: #000000 !important; border: 2px solid #D4AF37 !important; border-radius: 8px !important; }}
        input {{ color: #FFFFFF !important; background-color: #000000 !important; }}
        </style>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("<style>[data-testid='stAppViewContainer'] { background-color: #000000; }</style>", unsafe_allow_html=True)

# Enlaces a tu base de datos de Google Sheets
SHEET_ID = "1GXjpYr5nCrRH4wHI9RtKJQ3YUSv2sXcjZqWWL0kPoQA"
URL_USUARIOS = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Usuarios"

# --- PANTALLA 1: EL LOGIN ---
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

# --- PANTALLA 2: EL MENÚ PRINCIPAL CON LA HISTORIA ---
else:
    rol = st.session_state.user_role

    if st.session_state.current_menu == "PRINCIPAL":
        st.title("MENÚ PRINCIPAL")
        st.write(f"Bienvenido, **{st.session_state.user_alias}** — ({rol})")
        
        if st.button("HISTORIA DEL CLUB"):
            st.session_state.current_menu = "HISTORIA"
            st.rerun()
            
        if st.button("CERRAR SESIÓN"):
            st.session_state.authenticated = False
            st.rerun()

    elif st.session_state.current_menu == "HISTORIA":
        st.title("HISTORIA")
        st.markdown("""
        **Fundado un 16 de septiembre del 2017** por un grupo de 8 antiguos motoristas de diferentes moto clubs y algún otro. 
        
        Después de un tiempo, algunos nos dejaron y otros se fueron a recorrer las autopistas del cielo. 
        
        Tras unos años de andadura nos convertimos en **MC en 2026** bajo los valores de amistad, rutas, libertad, hermandad, y pasión por las motos.
        
        *⭐ In memori Sebas 1967-2022*
        """)
        
        if st.button("VOLVER AL MENÚ"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()
