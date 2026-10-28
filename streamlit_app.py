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
URL_NORMATIVA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Normativa"

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

# --- PANTALLA 2: MENÚ PRINCIPAL Y NAVEGACIÓN ---
else:
    rol = st.session_state.user_role
    
    # Creamos el control de pantallas si no existe todavía
    if "pantalla" not in st.session_state:
        st.session_state.pantalla = "PRINCIPAL"

    # === 1. MENÚ PRINCIPAL ===
    if st.session_state.pantalla == "PRINCIPAL":
        st.title("MENÚ PRINCIPAL")
        st.write(f"Bienvenido, **{st.session_state.user_alias}**")
        st.write(f"Cargo: **{st.session_state.user_role}**")
        
        if st.button("CLUB"):
            st.session_state.pantalla = "CLUB_MENU"
            st.rerun()

        if st.button("SALIDAS"):
            st.subheader("Calendario de Rutas")
            try:
                df_salidas = pd.read_csv(URL_SALIDAS)
                st.dataframe(df_salidas)
            except:
                st.write("No hay rutas programadas todavía.")
                
        if rol in ["Presidente", "Vicepresidente", "Tesorero", "Secretario", "Administrador"]:
            if st.button("ECONOMÍA"):
                st.subheader("Control Financiero del Club")
                try:
                    df_economia = pd.read_csv(URL_ECONOMIA)
                    st.dataframe(df_economia)
                except:
                    st.write("No hay registros financieros.")
                    
        if st.button("MERCHANDISING"):
            st.subheader("Tienda y Pedidos")
            st.write("Gestión de stock, chalecos, parches y camisetas.")
            
        if st.button("Cerrar Sesión"):
            st.session_state.authenticated = False
            st.session_state.pantalla = "PRINCIPAL"
            st.rerun()

    # === 2. PANTALLA: CLUB (La de tu foto) ===
    elif st.session_state.pantalla == "CLUB_MENU":
        st.title("CLUB")
        
        if st.button("REUNIONES"):
            st.subheader("Sección de Reuniones")
            st.write("Aquí irán las actas y próximas reuniones.")
            
        if st.button("OLD RAIDERS"):
            st.session_state.pantalla = "OLD_RAIDERS_MENU"
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.pantalla = "PRINCIPAL"
            st.rerun()

    # === 3. PANTALLA: MENÚ OLD RAIDERS (Normativa e Historia) ===
    elif st.session_state.pantalla == "OLD_RAIDERS_MENU":
        st.title("OLD RAIDERS")
        
        # Enllaç a la nova pestanya de Normativa al teu Google Sheets
        URL_NORMATIVA = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Normativa"
        
        if st.button("NORMATIVA"):
            st.session_state.pantalla = "NORMATIVA_VER"
            st.rerun()
            
        if st.button("HISTORIA"):
            st.session_state.pantalla = "HISTORIA_VER"
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.pantalla = "CLUB_MENU"
            st.rerun()

      # === 3.1 PANTALLA: VISUALITZAR NORMATIVA ===
    elif st.session_state.pantalla == "NORMATIVA_VER":
        st.title("NORMATIVA INTERNA")
        
        # Permís especial per a l'oficialat per afegir noves regles (Pantalla 8 de l'esbós)
        if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
            if st.button("➕ AÑADIR NUEVA NORMA"):
                st.session_state.pantalla = "NORMATIVA_CREAR"
                st.rerun()
        
        st.write("---")
        
        # Llegir i mostrar les normes des de Google Sheets
        try:
            URL_NORMATIVA = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Normativa"
            #URL_ECONOMIA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Economia"
            df_normativa = pd.read_csv(URL_NORMATIVA)
            df_normativa.columns = df_normativa.columns.str.strip()
            
            if not df_normativa.empty:
                for index, row in df_normativa.iterrows():
                    st.markdown(f"### 📌 {row['Tipo']}")
                    st.write(row['Descripcion'])
                    # Mostrar el tiempo/vigencia con un estilo destacado
                    if 'Tiempo' in df_normativa.columns and pd.notna(row['Tiempo']):
                        st.markdown(f"⏱️ **Tiempo / Vigencia:** *{row['Tiempo']}*")
                    st.write("---")
            else:
                st.write("No hay normas registradas todavía.")
        except:
            st.write("⚠️ Para ver las normas, crea una pestaña llamada 'Normativa' en tu Google Sheets con las columnas: Tipo, Descripcion y Tiempo.")

        if st.button("VOLVER"):
            st.session_state.pantalla = "OLD_RAIDERS_MENU"
            st.rerun()

    # === 3.2 PANTALLA: CREAR NORMATIVA ===
    elif st.session_state.pantalla == "NORMATIVA_CREAR":
        st.title("NUEVA NORMA")
        
        # Camps del formulari actualitzats amb la teva nova columna
        tipo_norma = st.text_input("TIPO (Categoría de la norma)")
        descripcion_norma = st.text_area("DESCRIPCION")
        tiempo_norma = st.text_input("TIEMPO (Ej: Permanente, 6 meses, Solo 2026...)")
        fecha_norma = st.date_input("FECHA DE REGISTRO")
        
        if st.button("GUARDAR NORMA"):
            if tipo_norma and descripcion_norma and tiempo_norma:
                # Aquí anirà la connexió per desar-ho a Google Sheets automàticament
                st.success(f"Norma '{tipo_norma}' con tiempo '{tiempo_norma}' preparada para guardar.")
            else:
                st.error("Por favor, rellena todos los campos (Tipo, Descripción y Tiempo).")
                
        if st.button("VOLVER"):
            st.session_state.pantalla = "NORMATIVA_VER"
            st.rerun()


    # === 3.3 PANTALLA: HISTÒRIA DEL CLUB (Text de la Pantalla 1 de l'esbós) ===
    elif st.session_state.pantalla == "HISTORIA_VER":
        st.title("HISTORIA DEL CLUB")
        
        # Text literal extret del teu esbós original
        st.markdown("""
        ### **Fundación**
        Fundado un **16 de septiembre del 2017** por un grupo de 8 antiguos motoristas de diferentes moto clubs y algún otro. 
        
        Después de un tiempo, algunos nos dejaron y otros se fueron a recorrer las autopistas del cielo.
        
        ### **Evolución**
        Tras unos años de andadura nos convertimos en **MC en 2026** bajo los valores de:
        * 🤝 Amistad
        * 🛣️ Rutas
        * 🦅 Libertad
        * 🪵 Hermandad
        * 🏍️ Pasión por las motos.
        
        ---
        ### 🖤 In memoriam
        **Sebas 1967-2022**
        """)
        
        if st.button("VOLVER"):
            st.session_state.pantalla = "OLD_RAIDERS_MENU"
            st.rerun()


    # === 4. PANTALLA: TEXTO DE LA HISTORIA (Con un único botón para volver) ===
    elif st.session_state.pantalla == "PANTALLA_HISTORIA":
        st.title("HISTORIA")
        
        # Texto oficial extraído de tu PDF
        st.markdown("""
        Fundado un **16 de septiembre del 2017** por un grupo de 8 antiguos motoristas de diferentes moto clubs y algún otro.
        
        Después de un tiempo, algunos nos dejaron y otros se fueron a recorrer las autopistas del cielo.
        
        Tras unos años de andadura nos convertimos en **MC en 2026** bajo los valores de amistad, rutas, libertad, hermandad, y pasión por las motos.
        
        *(In memori Sebas 1967-2022)*
        """)
        
        # Único botón para regresar al menú anterior
        if st.button("VOLVER"):
            st.session_state.pantalla = "OLD_RAIDERS_MENU"
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


