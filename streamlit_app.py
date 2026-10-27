import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Old Raiders MC", page_icon="🏍️", layout="centered")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_alias" not in st.session_state:
    st.session_state.user_alias = None
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "PRINCIPAL"

try:
    img_base64 = get_base64_image("Log.png")
    if not st.session_state.authenticated:
        bg_css = f'background-image: url("data:image/png;base64,{img_base64}"); background-size: contain; max-width: 450px !important;'
    else:
        bg_css = f'background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("data:image/png;base64,{img_base64}"); background-size: contain; max-width: 800px !important;'
    
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{ {bg_css} background-position: center top; background-repeat: no-repeat; background-color: #000000; background-attachment: fixed; }}
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

SHEET_ID = "1GXjpYr5nCrRH4wHI9RtKJQ3YUSv2sXcjZqWWL0kPoQA"
URL_USUARIOS = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Usuarios"
URL_SALIDAS = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Salidas"
URL_ECONOMIA = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Economia"

# --- LOGIN ---
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
                pwd_correcta = str(usuario_valido.iloc[0]['Contrasena']).strip() == contrasena_input if 'Contrasena' in df_usuarios.columns else contrasena_input == "1234"
                if pwd_correcta:
                    st.session_state.authenticated = True
                    st.session_state.user_role = usuario_valido.iloc[0]['Rol'].strip()
                    st.session_state.user_alias = usuario_valido.iloc[0]['Alias']
                    st.session_state.current_menu = "PRINCIPAL"
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")
            else:
                st.error("El usuario no coincide.")
        except Exception as e:
            st.error("Error al conectar con la base de datos.")

# --- MENÚS ---
else:
    rol = st.session_state.user_role

    if st.session_state.current_menu == "PRINCIPAL":
        st.title("MENÚ PRINCIPAL")
        st.write(f"Bienvenido, **{st.session_state.user_alias}** — ({rol})")
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
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    elif st.session_state.current_menu == "CLUB":
        st.title("CLUB")
        if rol in ["Presidente", "Vicepresidente", "Tesorero", "Secretario", "Administrador"]:
            if st.button("ECONOMÍA"):
                st.session_state.current_menu = "ECONOMIA_MENU"
                st.rerun()
        if st.button("REUNIONES"):
            st.subheader("Sección de Reuniones")
        if st.button("OLD RAIDERS"):
            st.session_state.current_menu = "OLD_RAIDERS"
            st.rerun()
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    elif st.session_state.current_menu == "OLD_RAIDERS":
        st.title("OLD RAIDERS")
        tab_normas, tab_historia = st.tabs(["📜 NORMATIVA", "🏍️ HISTORIA"])
        with tab_normas:
            st.subheader("Normativa Interna")
            if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                st.button("AÑADIR NUEVA NORMA", key="add_norma")
        with tab_historia:
            st.subheader("Historia Oficial")
            st.markdown("**Fundado un 16 de septiembre del 2017** por un grupo de 8 antiguos motoristas...")
        if st.button("VOLVER"):
            st.session_state.current_menu = "CLUB"
            st.rerun()

    elif st.session_state.current_menu == "ECONOMIA_MENU":
        st.title("ECONOMÍA")
        if st.button("MENSUALIDADES"): st.subheader("Control de Mensualidades")
        if st.button("OTROS PAGOS"): st.subheader("Otros Pagos (Bar, Colores, etc.)")
        if st.button("TOTAL DINERO"): st.subheader("Balance Económico Total")
        if st.button("VOLVER"):
            st.session_state.current_menu = "CLUB"
            st.rerun()

    elif st.session_state.current_menu == "SALIDAS":
        st.title("SALIDAS")
        if rol in ["Presidente", "Vicepresidente", "Secretario", "Capitán de Ruta", "Administrador"]:
            if st.button("AÑADIR NUEVA RUTA"): st.subheader("Formulario Nueva Ruta")
        if st.button("PRÓXIMAS SALIDAS"): st.subheader("Calendario de Rutas")
        if st.button("SALIDAS REALIZADAS (HISTORIAL)"): st.subheader("Historial")
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    elif st.session_state.current_menu == "USUARIOS":
        st.title("USUARIOS")
        if st.button("DATOS DE LOS MIEMBROS"): st.subheader("Fichas de Socios")
        if st.button("DATOS DE SALIDAS REALIZADAS"): st.subheader("Asistencia")
        if st.button("DATOS DE PAGOS AL DÍA"): st.subheader("Estado Cuentas")
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    elif st.session_state.current_menu == "MERCHANDISING":
        st.title("MERCHANDISING")
        if st.button("NUEVO PRODUCTO"): st.subheader("Alta Inventario")
        if st.button("NUEVO PEDIDO"): st.subheader("Formulario Pedidos")
        if st.button("LISTADO DE PRODUCTOS"): st.subheader("Stock")
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()
