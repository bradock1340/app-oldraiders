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
            st.session_state.pantalla = "REUNIONES_MENU"
            st.rerun()
            
        if st.button("OLD RAIDERS"):
            st.session_state.pantalla = "OLD_RAIDERS_MENU"
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.pantalla = "PRINCIPAL"
            st.rerun()

    # === 3. PANTALLA: MENÚ OLD RAIDERS (Normativa e Historia) ===
    elif st.session_state.pantalla == "OLD_RAIDERS_MENU":
        st.title("OLD RAIDERS")

        URL_NORMATIVA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Normativa"
        if st.button("NORMATIVA"):
            st.session_state.pantalla = "NORMATIVA_VER"
            st.rerun()
            
        if st.button("HISTORIA"):
            st.session_state.pantalla = "HISTORIA_VER"
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.pantalla = "CLUB_MENU"
            st.rerun()
 
       # === 3.1 PANTALLA: VISUALIZAR NORMATIVA ===
    elif st.session_state.pantalla == "NORMATIVA_VER":
        st.title("NORMATIVA INTERNA")
        
        # Creamos dos columnas en la parte superior para agrupar los botones de navegación
        col_botones1, col_botones2 = st.columns(2)
        
        with col_botones1:
            if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                if st.button("➕ AÑADIR NORMA"):
                    st.session_state.edit_norma_data = None
                    st.session_state.pantalla = "NORMATIVA_CREAR"
                    st.rerun()
                    
        with col_botones2:
            if st.button("⬅️ VOLVER"):
                st.session_state.pantalla = "OLD_RAIDERS_MENU"
                st.rerun()
        
        st.write("---")
        
        try:
            df_cat = pd.read_csv(URL_CAT_NORMAS)
            df_cat.columns = df_cat.columns.str.strip()
            categorias_principales = list(df_cat.columns)
            
            df_normativa = pd.read_csv(URL_NORMATIVA)
            df_normativa.columns = df_normativa.columns.str.strip()
            
            st.subheader("🔍 BUSCADOR DE REGLAS")
            busqueda = st.text_input("Escribe una palabra clave...").strip().lower()
            
            opciones_filtro = ["MOSTRAR TODAS"] + categorias_principales
            categoria_filtrada = st.selectbox("Filtrar por Categoría Principal", opciones_filtro)
            
            st.write("---")
            
            df_filtrado = df_normativa.copy()
            if categoria_filtrada != "MOSTRAR TODAS":
                df_filtrado = df_filtrado[df_filtrado['Tipo'].str.strip() == categoria_filtrada.strip()]
                
            if busqueda:
                condicion_tipo = df_filtrado['Tipo'].astype(str).str.lower().str.contains(busqueda)
                condicion_subtipo = df_filtrado['Subtipo'].astype(str).str.lower().str.contains(busqueda)
                condicion_desc = df_filtrado['Descripcion'].astype(str).str.lower().str.contains(busqueda)
                df_filtrado = df_filtrado[condicion_tipo | condicion_subtipo | condicion_desc]
            
            if not df_filtrado.empty:
                for index, row in df_filtrado.iterrows():
                    st.markdown(f"### 📌 {row['Subtipo']}")
                    st.caption(f"Categoría: {row['Tipo']}")
                    st.write(row['Descripcion'])
                    if 'Tiempo' in df_filtrado.columns and pd.notna(row['Tiempo']):
                        st.markdown(f"⏱️ **Vigencia:** *{row['Tiempo']}*")
                    
                    if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                        if st.button(f"📝 EDITAR REGLA", key=f"edit_{index}"):
                            st.session_state.edit_norma_data = {
                                "indice_fila": int(index),  # Guardamos la fila numérica real
                                "tipo": row['Tipo'],
                                "subtipo": row['Subtipo'],
                                "descripcion": row['Descripcion'],
                                "tiempo": row['Tiempo']
                            }
                            st.session_state.pantalla = "NORMATIVA_CREAR"
                            st.rerun()
                            
                    st.write("<hr style='border:1px dashed #D4AF37'>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ No se encontraron normas con esos criterios.")
                
        except Exception as e:
            st.error(f"Error de conexión o lectura: {e}")

        if st.button("VOLVER"):
            st.session_state.pantalla = "OLD_RAIDERS_MENU"
            st.rerun()


    # === 3.2 PANTALLA: CREAR / EDITAR NORMATIVA ===
         # === 3.2 PANTALLA: CREAR / EDITAR NORMATIVA ===
    elif st.session_state.pantalla == "NORMATIVA_CREAR":
        es_edicion = st.session_state.edit_norma_data is not None
        
        if es_edicion:
            st.title("📝 EDITAR NORMA")
            datos_previos = st.session_state.edit_norma_data
        else:
            st.title("➕ NUEVA NORMA")
            datos_previos = {"tipo": None, "subtipo": None, "descripcion": "", "tiempo": ""}
            
        import requests
        import json
        
        try:
            df_cat = pd.read_csv(URL_CAT_NORMAS)
            df_cat.columns = df_cat.columns.str.strip()
            categorias_principales = list(df_cat.columns)
            
            idx_tipo = categorias_principales.index(datos_previos["tipo"]) if datos_previos["tipo"] in categorias_principales else 0
            tipo_seleccionado = st.selectbox("TIPO (Categoría Principal)", categorias_principales, index=idx_tipo)
            
            subtipos_disponibles = list(df_cat[tipo_seleccionado].dropna().astype(str).unique())
            idx_sub = subtipos_disponibles.index(datos_previos["subtipo"]) if datos_previos["subtipo"] in subtipos_disponibles else 0
            subtipo_seleccionado = st.selectbox("SUBTIPO (Regla Específica)", subtipos_disponibles, index=idx_sub)
            
            descripcion_norma = st.text_area("DESCRIPCION DE LA NORMA", value=datos_previos["descripcion"])
            tiempo_norma = st.text_input("TIEMPO / VIGENCIA (Ej: Permanente)", value=datos_previos["tiempo"])
            
            texto_boton = "ACTUALIZAR CAMBIOS" if es_edicion else "GUARDAR NORMA"
            
            if st.button(texto_boton):
                if descripcion_norma and tiempo_norma:
                    
                    URL_PROCESADOR_GOOGLE = f"https://script.google.com/macros/s/AKfycby2x4Fz5QDCkRWnQR6NoEIM_4gMRbGA9OjBSWp2R1DC91ABQKTuV7pXFIcsQyrlPe6B/exec"
                    
                    if es_edicion:
                        payload = {
                            "accion": "editar",  # Corregido a "editar" para que coincida con tu Script
                            "indice_fila": int(datos_previos["indice_fila"]), # Obligamos a que sea un número entero limpio
                            "tipo": tipo_seleccionado,
                            "subtipo": subtipo_seleccionado,
                            "descripcion": descripcion_norma,
                            "tiempo": tiempo_norma
                        }
                    else:
                        payload = {
                            "accion": "crear",
                            "tipo": tipo_seleccionado,
                            "subtipo": subtipo_seleccionado,
                            "descripcion": descripcion_norma,
                            "tiempo": tiempo_norma
                        }
                    
                    respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                    
                    if "OK_CREAR" in respuesta.text:
                        st.success("✔️ ¡Nueva norma guardada con éxito!")
                        st.balloons()
                    elif "OK_EDITAR" in respuesta.text:
                        st.success("✔️ ¡Norma modificada y actualizada con éxito!")
                       # st.balloons()
                    else:
                        st.error("Google rechazó la operación.")
                else:
                    st.error("Por favor, rellena todos los campos antes de continuar.")
                    
        except Exception as e:
            st.error(f"Error en el módulo de datos: {e}")
            
        if st.button("VOLVER"):
            st.session_state.edit_norma_data = None
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
        * Amistad
        * Rutas
        * Libertad
        * Hermandad
        * Pasión por las motos.
        
        ---
        ###  In memoriam
        **Sebas 1967-2022**
        """)
        
        if st.button("VOLVER"):
            st.session_state.pantalla = "OLD_RAIDERS_MENU"
            st.rerun()


    # === 4. PANTALLA: TEXTO DE LA HISTORIA (Con un único botón para volver) ===
    elif st.session_state.pantalla == "PANTALLA_HISTORIA":
        st.title("HISTORIA")
        
        # Texto oficial 
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

    # === 2.1 PANTALLA: REUNIONES (Listado con tus Columnas Reales) ===
    elif st.session_state.pantalla == "REUNIONES_MENU":
        st.title("REUNIONES Y ACTAS")
        
        col_reun1, col_reun2 = st.columns(2)
        with col_reun1:
            if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                if st.button("➕ AÑADIR REUNIÓN"):
                    st.session_state.pantalla = "REUNIONES_CREAR"
                    st.rerun()
        with col_reun2:
            if st.button("⬅️ VOLVER"):
                st.session_state.pantalla = "PRINCIPAL"
                st.rerun()
                
        st.write("---")
        
        try:
            #URL_REUNIONES = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Reuniones"
           #URL_REUNIONES = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Reuniones" 
            # Busca esta línea en tu bloque 2.1 de GitHub y cámbiala exactamente por esta:
URL_REUNIONES = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Reuniones"

            df_reuniones = pd.read_csv(URL_REUNIONES)
            df_reuniones.columns = df_reuniones.columns.str.strip()
            
            df_reuniones['Fecha_DT'] = pd.to_datetime(df_reuniones['Fecha'], format='%d/%m/%Y', errors='coerce')
            
            st.subheader("🔍 BUSCADOR E HISTORIAL")
            
            df_reuniones['Año'] = df_reuniones['Fecha_DT'].dt.year.fillna(2026).astype(int)
            lista_años = ["TODOS"] + sorted(list(df_reuniones['Año'].unique()), reverse=True)
            año_sel = st.selectbox("Filtrar por Año", lista_años)
            
            busqueda_tema = st.text_input("Buscar por contenido o resumen...").strip().lower()
            
            st.write("---")
            
            df_filtrado = df_reuniones.copy()
            if año_sel != "TODOS":
                df_filtrado = df_filtrado[df_filtrado['Año'] == int(año_sel)]
            if busqueda_tema:
                df_filtrado = df_filtrado[
                    df_filtrado['Tipo'].astype(str).str.lower().str.contains(busqueda_tema) | 
                    df_filtrado['Resumen'].astype(str).str.lower().str.contains(busqueda_tema)
                ]
            
            if not df_filtrado.empty:
                for index, row in df_filtrado.iterrows():
                    st.markdown(f"### 📅 {row['Fecha']} — {row['Tipo']}")
                    st.write(f"**Resumen / Orden del día:** {row['Resumen']}")
                    
                    if 'Miembros' in df_filtrado.columns and pd.notna(row['Miembros']) and str(row['Miembros']).strip() != "":
                        st.markdown(f"👥 **Asistentes:** *{row['Miembros']}*")
                        
                    if 'Enlace PDF' in df_filtrado.columns and pd.notna(row['Enlace PDF']) and str(row['Enlace PDF']).strip() != "":
                        st.markdown(f"🔗 [📥 Descargar Acta PDF]({row['Enlace PDF']})")
                        
                    if 'Enviar por correo' in df_filtrado.columns and row['Enviar por correo'] == "SÍ":
                        st.caption("📧 *Esta acta fue marcada para difusión por correo electrónico.*")
                        
                    st.write("<hr style='border:1px dashed #D4AF37'>", unsafe_allow_html=True)
            else:
                st.warning("No se encontraron reuniones guardadas.")
                
        except Exception as e:
            st.error(f"Error de lectura en la hoja: {e}")

    # === 2.2 PANTALLA: AÑADIR REUNIÓN (Campos e Inyección a tus Columnas) ===
    elif st.session_state.pantalla == "REUNIONES_CREAR":
        st.title("➕ NUEVA REUNIÓN")
        import requests
        import json
        
        fecha_reunion = st.date_input("FECHA DE LA REUNIÓN")
        tipo_reunion = st.selectbox("TIPO DE REUNIÓN", ["Ordinaria", "Extraordinaria", "Voto de colores", "Asamblea General"])
        descripcion_reunion = st.text_area("RESUMEN / ORDEN DEL DÍA")
        enlace_acta = st.text_input("ENLACE AL PDF DEL ACTA (Opcional)")
        
        enviar_mail_check = st.checkbox("✉️ Enviar copia del acta por correo a todo el club", value=False)
        string_correo = "SÍ" if enviar_mail_check else "NO"
        
        st.subheader("👥 CONTROL DE ASISTENCIA")
        st.write("Selecciona los oficiales y miembros presentes:")
        
        asistentes_lista = []
        try:
            df_usuarios = pd.read_csv(URL_USUARIOS)
            df_usuarios.columns = df_usuarios.columns.str.strip()
            listado_miembros = sorted(df_usuarios['Alias'].dropna().astype(str).unique())
            
            for miembro in listado_miembros:
                if st.checkbox(f"🏍️ {miembro}", value=True, key=f"reun_real_{miembro}"):
                    asistentes_lista.append(miembro)
        except:
            st.warning("No se pudo enlazar la lista de miembros de la pestaña Usuarios.")
            
        string_asistentes_comas = ", ".join(asistentes_lista)
        
        if st.button("GUARDAR REUNIÓN"):
            if descripcion_reunion:
                fecha_formateada = fecha_reunion.strftime('%d/%m/%Y')
                URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycby2x4Fz5QDCkRWnQR6NoEIM_4gMRbGA9OjBSWp2R1DC91ABQKTuV7pXFIcsQyrlPe6B/exec"

                
                payload = {
                    "accion": "crear_reunion_real",
                    "fecha": fecha_formateada,
                    "tipo": tipo_reunion,
                    "miembros": string_asistentes_comas,
                    "resumen": descripcion_reunion,
                    "enlace_pdf": enlace_acta if enlace_acta else "",
                    "enviar_correo": string_correo
                }
                
                try:
                    respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                    if "OK_REUNION" in respuesta.text:
                        st.success("✔️ Acta y asistencia guardadas correctamente.")
                        st.session_state.pantalla = "REUNIONES_MENU"
                        st.rerun()
                    else:
                        st.error("Google rechazó la estructura de las columnas.")
                except Exception as err:
                    st.error(f"Fallo de red: {err}")
            else:
                st.error("Por favor, rellena el resumen u orden del día.")
                
        if st.button("CANCELAR"):
            st.session_state.pantalla = "REUNIONES_MENU"
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
