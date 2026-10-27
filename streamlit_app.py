import streamlit as st
import pandas as pd

# Configuración de la página estilo móvil
st.set_page_config(page_title="Old Raiders MC", page_icon="🏍️", layout="centered")

# URL REAL Y TOTALMENTE DIRECTA DE TU ESCUDO EN GITHUB
LOGO_URL = "https://githubusercontent.com"

# Estilos visuales con el escudo de los Old Raiders de fondo de pantalla (AÑADIDO SIN TOCAR LO DEMÁS)
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{LOGO_URL}");
        background-size: 85% auto;
        background-position: center 15%;
        background-repeat: no-repeat;
        background-color: #000000;
    }}
    h1, h2, h3, p, label {{ color: #FFFFFF !important; text-shadow: 2px 2px 4px #000000; }}
    .stButton>button {{
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        height: 50px !important;
        font-size: 18px !important;
        margin-bottom: 15px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.7);
    }}
    .stButton>button:hover {{ background-color: #FFF !important; color: #000 !important; }}
    div[data-baseweb="input"] {{
        background-color: rgba(26, 26, 26, 0.85) !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 8px !important;
    }}
    input {{ color: #FFFFFF !important; }}
    </style>
""", unsafe_allow_html=True)

# URL base de tu Google Sheets (LAS TUYAS ORIGINALES QUE FUNCIONAN PERFECTAMENTE)
SHEET_ID = "1GXjpYr5nCrRH4wHI9RtKJQ3YUSv2sXcjZqWWL0kPoQA"
URL_USUARIOS = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Usuarios"
URL_SALIDAS = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Salidas"
URL_ECONOMIA = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Economia"

# Control de estado de la aplicación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_alias" not in st.session_state:
    st.session_state.user_alias = None

# --- PANTALLA 1: LOGIN ---
if not st.session_state.authenticated:
    # Espacio para empujar las casillas hacia abajo y dejar ver el escudo libre arriba
    st.write("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    
    st.title("Old Raiders MC")
    st.subheader("Catalonia")
    
    usuario_input = st.text_input("USUARIO (EMAIL)").strip().lower()
    contrasena_input = st.text_input("CONTRASEÑA", type="password")
    
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
                # Comprobamos la contraseña (asumiendo que añadas una columna llamada 'Contraseña')
                # Si aún no la tienes, usaremos '1234' por defecto temporalmente
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
            st.error("Vuelve a pulsar enter, para confirmar.")

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
    # Rangos autorizados según tu matriz de permisos
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
