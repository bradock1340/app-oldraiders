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
    
    /* Clau tancada correctament al final d'aquesta regla */
    div[data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }

    /* Selector corregit i ultraespecífic per als botons */
    div[data-testid="stButton"] button {
        background-color: #000000 !important; 
        color: #FFFFFF !important;            
        font-weight: bold !important;
        font-size: 16px !important;           
        border-radius: 6px !important;        
        border: 3px solid #FFD700 !important; /* Força el teu contorn groc */
        width: 100% !important;               
        padding: 10px 15px !important;        
        margin-top: 8px !important;
        margin-bottom: 8px !important;
        text-transform: uppercase !important; 
        box-shadow: none !important;          
    }

/* Efecte Hover complet i ultraespecífic per al fons i el text */
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
            st.session_state.current_menu = "REUNIONES_MENU"
            st.rerun()
            
        if st.button("OLD RIDERS"):
            # CORREGIDO: Cambiado .pantalla por .current_menu
            st.session_state.current_menu = "OLD_RIDERS_MENU"
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

    # === 3. PANTALLA: MENÚ OLD RIDERS (Normativa , Historia y usuarios) ===
    elif st.session_state.pantalla == "OLD_RIDERS_MENU":
        st.title("OLD RIDERS")

        URL_NORMATIVA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Normativa"
        if st.button("NORMATIVA"):
            st.session_state.pantalla = "NORMATIVA_VER"
            st.rerun()
        if st.button("HISTORIA"):
            st.session_state.pantalla = "HISTORIA_VER"
            st.rerun()
            
        if st.button("USUARIOS"):  
            st.session_state.pantalla = "USUARIOS_FICHA" 
            st.rerun()
            
        if st.button("VOLVER"):
            st.session_state.pantalla = "CLUB_MENU"
            st.rerun()
# === 4. PANTALLA: DATOS DE LOS MIEMBROS (USUARIOS) ===
    elif st.session_state.current_menu == "USUARIOS_FICHA":
        st.title("👤 DATOS DE LOS MIEMBROS")
        
        # 1. Verificar si el usuario conectado tiene permisos de edición (Presidente, Vicepresidente, Administrador)
        puede_editar = rol in ["Presidente", "Vicepresidente", "Administrador"]
        
        if puede_editar:
            st.success("🔓 Modo Edición Activado (Tienes permisos para modificar datos)")
        else:
            st.info("🔒 Modo Consulta (Solo los oficiales autorizados pueden modificar datos)")
            
        st.write("---")

        try:
            # 2. Descargar los datos en tiempo real de tu Google Sheets
            df_usuarios = pd.read_csv(URL_USUARIOS)
            df_usuarios.columns = df_usuarios.columns.str.strip()
            
            # Buscamos por 'Alias' o 'Nombre' según cómo esté la cabecera
            col_identificador = 'Alias' if 'Alias' in df_usuarios.columns else 'Nombre'
            df_usuarios[col_identificador] = df_usuarios[col_identificador].astype(str).str.strip()
            
            # Selector interactivo de socios
            lista_miembros = sorted(df_usuarios[col_identificador].unique())
            miembro_sel = st.selectbox("Selecciona un miembro para gestionar su ficha:", ["-- Seleccionar miembro --"] + lista_miembros)
            
            st.write("---")
            
            if miembro_sel != "-- Seleccionar miembro --":
                # Extraer la fila del socio seleccionado
                datos_miembro = df_usuarios[df_usuarios[col_identificador] == miembro_sel].iloc[0]
                
                # Determinamos si los campos están bloqueados (si no es editor, disabled=True)
                bloqueado = not puede_editar
                
                # 3. INTERFAZ EN COLUMNAS CON TODOS LOS DATOS DEL GOOGLE SHEET
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Datos de Identidad")
                    nombre = st.text_input("Nombre Real", value=str(datos_miembro.get('Nombre', '')), disabled=bloqueado)
                    apellido = st.text_input("Apellido", value=str(datos_miembro.get('Apellido', '')), disabled=bloqueado)
                    alias = st.text_input("Alias en el Club", value=str(datos_miembro.get('Alias', miembro_sel)), disabled=bloqueado)
                    email = st.text_input("Email / Usuario", value=str(datos_miembro.get('Usuario', datos_miembro.get('Email', ''))), disabled=bloqueado)
                    telefono = st.text_input("Teléfono", value=str(datos_miembro.get('Telefono', '')), disabled=bloqueado)
                    
                    # Mostrar contraseña oculta solo si es editor por seguridad
                    if puede_editar:
                        contrasena = st.text_input("Contraseña Acceso App", value=str(datos_miembro.get('Contrasena', '')), type="password")
                
                with col2:
                    st.subheader("Estado y Fechas")
                    
                    # Selector de cargos oficiales basados en tus roles del club
                    lista_cargos = ["Presidente", "Vicepresidente", "Secretario", "Tesorero", "Capitán de Ruta", "Sargento de Armas", "Miembro", "Prospect", "Handground"]
                    cargo_actual = str(datos_miembro.get('Rol', datos_miembro.get('Cargo', 'Miembro'))).strip()
                    idx_cargo = lista_cargos.index(cargo_actual) if cargo_actual in lista_cargos else 6
                    
                    cargo = st.selectbox("Cargo / Rol", lista_cargos, index=idx_cargo, disabled=bloqueado)
                    
                    # Fechas y balances financieros
                    inicio = st.text_input("Fecha Inicio en el Club (DD/MM/AAAA)", value=str(datos_miembro.get('Inicio', '')), disabled=bloqueado)
                    final = st.text_input("Fecha Final / Baja (Si aplica)", value=str(datos_miembro.get('Final', '')), disabled=bloqueado)
                    
                    estado = st.text_input("Estado (Activo / Inactivo)", value=str(datos_miembro.get('Estado', 'Activo')), disabled=bloqueado)
                    saldo = st.text_input("Saldo de Cuentas (€)", value=str(datos_miembro.get('Saldo', '0.00')), disabled=bloqueado)
                
                st.write("---")
                st.subheader("Sección de Notas Internas")
                observaciones = st.text_area("Observaciones del Miembro", value=str(datos_miembro.get('Observaciones', '')), disabled=bloqueado)
                
                # 4. BOTÓN ACCIÓN INTELIGENTE (Solo visible para roles con permiso de escritura)
                if puede_editar:
                    if st.button("💾 GUARDAR Y ACTUALIZAR CAMBIOS"):
                        # Aquí llamaremos a tu procesador macro de Google Apps Script para impactar la fila exacta
                        st.info("Conectando con Google Sheets para aplicar cambios en la base de datos...")
                        
        except Exception as e:
            st.error(f"Error de lectura en la hoja 'Usuarios': {e}")
            st.warning("Verifica que los nombres de las columnas en tu Excel coincidan (Nombre, Apellido, Telefono, Inicio, Final, Estado, Observaciones).")
            
        # 5. Botón Volver limpio
        if st.button("⬅️ VOLVER"):
            st.session_state.current_menu = "OLD_RIDERS_MENU"
            st.rerun()


            
# === 3.1 PANTALLA: VISUALIZAR NORMATIVA ===
    elif st.session_state.pantalla == "NORMATIVA_VER":
        st.title("NORMATIVA INTERNA")
        
        # Creamos dos columnas en la parte superior para agrupar los botones de navegación
        col_botones1, col_botones2 = st.columns(2)
        
        with col_botones1:
            if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                if st.button("➕ AÑADIR NORMA"):
                    # CORREGIDO: Limpiamos los datos previos y desactivamos el modo lectura
                    st.session_state.edit_norma_data = None
                    st.session_state.modo_consulta_norma = False
                    st.session_state.pantalla = "NORMATIVA_CREAR"
                    st.rerun()
                    
        with col_botones2:
            if st.button("⬅️ VOLVER"):
                st.session_state.pantalla = "OLD_RIDERS_MENU"
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
                    
                    # === NUEVA LÓGICA INTELIGENTE: EDITAR O CONSULTAR SEGÚN ROL ===
                    if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                        if st.button(f"📝 EDITAR REGLA", key=f"edit_{index}"):
                            st.session_state.edit_norma_data = {
                                "indice_fila": int(index),  # Guardamos la fila numérica real
                                "tipo": row['Tipo'],
                                "subtipo": row['Subtipo'],
                                "descripcion": row['Descripcion'],
                                "tiempo": row['Tiempo']
                            }
                            st.session_state.modo_consulta_norma = False # Modo edición activo
                            st.session_state.pantalla = "NORMATIVA_CREAR"
                            st.rerun()
                    else:
                        # Si entra un miembro normal, le pintamos el botón para consultar los detalles
                        if st.button(f"👁️ CONSULTAR REGLA", key=f"view_{index}"):
                            st.session_state.edit_norma_data = {
                                "indice_fila": int(index),
                                "tipo": row['Tipo'],
                                "subtipo": row['Subtipo'],
                                "descripcion": row['Descripcion'],
                                "tiempo": row['Tiempo']
                            }
                            st.session_state.modo_consulta_norma = True # Modo lectura activado
                            st.session_state.pantalla = "NORMATIVA_CREAR"
                            st.rerun()
                            
                    st.write("<hr style='border:1px dashed #D4AF37'>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ No se encontraron normas con esos criterios.")
                
        except Exception as e:
            st.error(f"Error de conexión o lectura: {e}")

        if st.button("VOLVER", key="btn_volver_final"):
            st.session_state.pantalla = "OLD_RIDERS_MENU"
            st.rerun()


      # === 3.2 PANTALLA: CREAR / EDITAR / CONSULTAR NORMATIVA ===
    elif st.session_state.pantalla == "NORMATIVA_CREAR":
        es_edicion = st.session_state.edit_norma_data is not None
        es_consulta = st.session_state.get("modo_consulta_norma", False)
        
        if es_consulta:
            st.title("👁️ CONSULTA DE NORMA")
            datos_previos = st.session_state.edit_norma_data
        elif es_edicion:
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
            tipo_seleccionado = st.selectbox("TIPO (Categoría Principal)", categorias_principales, index=idx_tipo, disabled=es_consulta)
            
            subtipos_disponibles = list(df_cat[tipo_seleccionado].dropna().astype(str).unique())
            idx_sub = subtipos_disponibles.index(datos_previos["subtipo"]) if datos_previos["subtipo"] in subtipos_disponibles else 0
            subtipo_seleccionado = st.selectbox("SUBTIPO (Regla Específica)", subtipos_disponibles, index=idx_sub, disabled=es_consulta)
            
            descripcion_norma = st.text_area("DESCRIPCION DE LA NORMA", value=datos_previos["descripcion"], disabled=es_consulta)
            tiempo_norma = st.text_input("TIEMPO / VIGENCIA (Ej: Permanente)", value=datos_previos["tiempo"], disabled=es_consulta)
            
            # --- ZONA DE BOTONES DE ACCIÓN ---
            st.write("---")
            
            if not es_consulta:
                texto_boton = "ACTUALIZAR CAMBIOS" if es_edicion else "GUARDAR NORMA"
                if st.button(texto_boton):
                    if descripcion_norma and tiempo_norma:
                        
                        URL_PROCESADOR_GOOGLE = f"https://script.google.com/macros/s/AKfycby2x4Fz5QDCkRWnQR6NoEIM_4gMRbGA9OjBSWp2R1DC91ABQKTuV7pXFIcsQyrlPe6B/exec"
                        
                        if es_edicion:
                            payload = {
                                "accion": "editar",
                                "indice_fila": int(datos_previos["indice_fila"]),
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
                            import time
                            time.sleep(2.0)
                            st.session_state.edit_norma_data = None
                            st.session_state.modo_consulta_norma = False
                            st.session_state.pantalla = "NORMATIVA_VER"
                            st.rerun()
                        elif "OK_EDITAR" in respuesta.text:
                            st.success("✔️ ¡Norma modificada y actualizada con éxito!")
                            import time
                            time.sleep(2.0)
                            st.session_state.edit_norma_data = None
                            st.session_state.modo_consulta_norma = False
                            st.session_state.pantalla = "NORMATIVA_VER"
                            st.rerun()
                        else:
                            st.error("Google rechazó la operación.")
                    else:
                        st.error("Por favor, rellena todos los campos antes de continuar.")
            else:
                st.info("ℹ️ Estás en modo consulta (Lectura).")
                    
        except Exception as e:
            st.error(f"Error en el módulo de datos: {e}")
            
        texto_volver = "⬅️ VOLVER AL LISTADO" if es_consulta else "VOLVER"
        if st.button(texto_volver, key="btn_volver_crear"):
            st.session_state.edit_norma_data = None
            st.session_state.modo_consulta_norma = False
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
            st.session_state.pantalla = "OLD_RIDERS_MENU"
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
            st.session_state.pantalla = "OLD_RIDERS_MENU"
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
                    # Se limpian los datos previos y el modo consulta para asegurar una nueva reunión vacía
                    st.session_state.edit_reunion_data = None
                    st.session_state.modo_consulta = False
                    st.session_state.pantalla = "REUNIONES_CREAR"
                    st.rerun()
        with col_reun2:
            if st.button("⬅️ VOLVER"):
                st.session_state.pantalla = "PRINCIPAL"
                st.rerun()
                
        st.write("---")
        
        try:
            # === URL limpia oficial de Google Docs mantenida exactamente igual ===
            URL_REUNIONES = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Reuniones" 
            df_reuniones = pd.read_csv(URL_REUNIONES)
            df_reuniones.columns = df_reuniones.columns.str.strip()
            
            # Formatear fechas para poder extraer el año correctamente
            df_reuniones['Fecha_DT'] = pd.to_datetime(df_reuniones['Fecha'], format='%d/%m/%Y', errors='coerce')
            
            # --- SECCIÓN DE FILTROS ---
            st.subheader("🔍 BUSCADOR E HISTORIAL")
            
            # Filtro por Año
            df_reuniones['Año'] = df_reuniones['Fecha_DT'].dt.year.fillna(2026).astype(int)
            lista_años = ["TODOS"] + sorted(list(df_reuniones['Año'].unique()), reverse=True)
            año_sel = st.selectbox("Filtrar por Año", lista_años)
            
            # Filtro por palabra clave (Tema)
            busqueda_tema = st.text_input("Buscar por contenido o resumen...").strip().lower()
            
            st.write("---")
            
            # Aplicar los filtros
            df_filtrado = df_reuniones.copy()
            if año_sel != "TODOS":
                df_filtrado = df_filtrado[df_filtrado['Año'] == int(año_sel)]
            if busqueda_tema:
                df_filtrado = df_filtrado[
                    df_filtrado['Tipo'].astype(str).str.lower().str.contains(busqueda_tema) | 
                    df_filtrado['Resumen'].astype(str).str.lower().str.contains(busqueda_tema)
                ]
            
            # --- MOSTRAR LAS REUNIONES EN PANTALLA ---
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
                        
                    # === BOTÓN INTELIGENTE: EDITAR O CONSULTAR SEGÚN ROL ===
                    if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                        if st.button("📝 EDITAR REUNIÓN", key=f"edit_reun_{index}"):
                            # Se guardan los datos de la fila completa y se desactiva modo lectura
                            st.session_state.edit_reunion_data = row.to_dict()
                            st.session_state.modo_consulta = False
                            st.session_state.pantalla = "REUNIONES_CREAR"
                            st.rerun()
                    else:
                        if st.button("👁️ CONSULTAR REUNIÓN", key=f"view_reun_{index}"):
                            # Se guardan los datos de la fila completa y se activa el modo consulta de solo lectura
                            st.session_state.edit_reunion_data = row.to_dict()
                            st.session_state.modo_consulta = True
                            st.session_state.pantalla = "REUNIONES_CREAR"
                            st.rerun()
                        
                    st.write("<hr style='border:1px dashed #D4AF37'>", unsafe_allow_html=True)
            else:
                st.warning("No se encontraron reuniones guardadas.")
                
        except Exception as e:
            st.error(f"Error de lectura en la hoja: {e}")



       # === 2.2 PANTALLA: CREAR / EDITAR REUNIÓN ===
    elif st.session_state.pantalla == "REUNIONES_CREAR":
        es_edicion = st.session_state.get("edit_reunion_data") is not None
        es_consulta = st.session_state.get("modo_consulta", False)
        
        if es_consulta:
            st.title("👁️ CONSULTA DE REUNIÓN")
            datos_previos = st.session_state.edit_reunion_data
        elif es_edicion:
            st.title("📝 EDITAR REUNIÓN")
            datos_previos = st.session_state.edit_reunion_data
        else:
            st.title("➕ NUEVA REUNIÓN")
            datos_previos = {}
            
        import requests
        import json
        
        # --- 1. CONFIGURACIÓN DE VALORES INICIALES (EVITA KEYERROR) ---
        fecha_cruda = datos_previos.get('Fecha', '')
        if (es_edicion or es_consulta) and fecha_cruda:
            try:
                fecha_inicial_dt = pd.to_datetime(fecha_cruda, format='%d/%m/%Y').date()
            except:
                fecha_inicial_dt = pd.Timestamp.now().date()
        else:
            fecha_inicial_dt = pd.Timestamp.now().date()
            
        tipo_actual = datos_previos.get('Tipo', 'Ordinaria')
        resumen_actual = datos_previos.get('Resumen', '')
        pdf_actual = datos_previos.get('Enlace PDF', '')
        if pd.isna(pdf_actual) or str(pdf_actual).strip().lower() == 'nan':
            pdf_actual = ""
            
        correo_actual = datos_previos.get('Enviar por correo', 'NO')
        miembros_actuales = datos_previos.get('Miembros', '')
        
        # --- 2. RENDERIZADO DE LOS ENTRADAS DE LA INTERFAZ ---
        fecha_reunion = st.date_input("FECHA DE LA REUNIÓN", value=fecha_inicial_dt, disabled=es_consulta)
        
        tipos_disponibles = ["Ordinaria", "Extraordinaria", "Voto de colores", "Asamblea General"]
        idx_tipo = tipos_disponibles.index(tipo_actual) if tipo_actual in tipos_disponibles else 0
        tipo_reunion = st.selectbox("TIPO DE REUNIÓN", tipos_disponibles, index=idx_tipo, disabled=es_consulta)
        
        descripcion_reunion = st.text_area("RESUMEN / ORDEN DEL DÍA", value=resumen_actual, disabled=es_consulta)
        enlace_acta = st.text_input("ENLACE AL PDF DEL ACTA (Opcional)", value=pdf_actual, disabled=es_consulta)
        
        enviar_mail_check = st.checkbox("✉️ Enviar copia del acta por correo a todo el club", value=(correo_actual == "SÍ"), disabled=es_consulta)
        string_correo = "SÍ" if enviar_mail_check else "NO"
        
        st.subheader("👥 CONTROL DE ASISTENCIA")
        st.write("Selecciona los oficiales y miembros presentes:")
        
        # Procesar asistentes previos de forma segura
        asistentes_antiguos = [m.strip() for m in str(miembros_actuales).split(",") if m.strip()]
        
        asistentes_lista = []
        try:
            df_usuarios = pd.read_csv(URL_USUARIOS)
            df_usuarios.columns = df_usuarios.columns.str.strip()
            listado_miembros = sorted(df_usuarios['Alias'].dropna().astype(str).unique())
            
            for miembro in listado_miembros:
                # Si es edición o consulta respeta el Sheet; si es nueva reunión, todos marcados por defecto
                marcado_defecto = miembro in asistentes_antiguos if (es_edicion or es_consulta) else True
                if st.checkbox(f"🏍️ {miembro}", value=marcado_defecto, key=f"reun_real_{miembro}", disabled=es_consulta):
                    asistentes_lista.append(miembro)
        except Exception as e:
            st.warning("No se pudo enlazar la lista de miembros de la pestaña Usuarios.")
            
        string_asistentes_comas = ", ".join(asistentes_lista)
        
        # --- 3. BOTONES DE ACCIÓN (SIEMPRE VISIBLES AL FINAL) ---
        st.write("---")
        texto_boton_principal = "ACTUALIZAR CAMBIOS" if es_edicion else "GUARDAR REUNIÓN"
        col_accion1, col_accion2 = st.columns(2)
        
        with col_accion1:
            if not es_consulta:
                if st.button(texto_boton_principal):
                    if descripcion_reunion:
                        fecha_formateada = fecha_reunion.strftime('%d/%m/%Y')
                        
                        # ✔️ CORREGIDO: Tu URL de Apps Script real recuperada de los pasos anteriores
                        URL_DIRECTA = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
                        
                        if es_edicion:
                            payload = {
                                "accion": "editar_reunion_real",
                                "fecha_original": str(datos_previos.get('Fecha', '')),
                                "resumen_original": str(datos_previos.get('Resumen', '')),
                                "fecha": fecha_formateada,
                                "tipo": tipo_reunion,
                                "miembros": string_asistentes_comas,
                                "resumen": descripcion_reunion,
                                "enlace_pdf": enlace_acta,
                                "enviar_correo": string_correo
                            }
                        else:
                            payload = {
                                "accion": "crear_reunion_real",
                                "fecha": fecha_formateada,
                                "tipo": tipo_reunion,
                                "miembros": string_asistentes_comas,
                                "resumen": descripcion_reunion,
                                "enlace_pdf": enlace_acta,
                                "enviar_correo": string_correo
                            }
                        
                        try:
                            res = requests.post(
                                URL_DIRECTA, 
                                data=json.dumps(payload), 
                                headers={"Content-Type": "application/json"}
                            )
                            
                            if "OK_REUNION" in res.text:
                                st.success("✔️ ¡Reunión modificada y actualizada con éxito!")
                                import time
                                time.sleep(2.0)
                                st.session_state.edit_reunion_data = None
                                st.session_state.modo_consulta = False
                                st.session_state.pantalla = "REUNIONES_MENU"
                                st.rerun()
                            else:
                                st.error(f"Google rechazó la estructura: {res.text}")
                        except Exception as e:
                            st.error(f"Error de conexión con el servidor: {e}")
                    else:
                        st.warning("El campo RESUMEN / ORDEN DEL DÍA es obligatorio.")
            else:
                st.info("ℹ️ Estás en modo consulta (Lectura).")
                    
        with col_accion2:
            texto_volver = "⬅️ VOLVER AL LISTADO" if es_consulta else "❌ CANCELAR"
            if st.button(texto_volver):
                st.session_state.edit_reunion_data = None
                st.session_state.modo_consulta = False
                st.session_state.pantalla = "REUNIONES_MENU"
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


