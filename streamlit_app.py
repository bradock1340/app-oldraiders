import streamlit as st
import pandas as pd
import base64

# Configuración de la página estilo móvil
st.set_page_config(page_title="Old Riders MC", page_icon="🏍️", layout="centered")

# --- 1. FUNCIÓN PARA CARGAR LA IMAGEN DE FONDO
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

# --- 2. CONFIGURACIÓN DINÁMICA DEL FONDO (IMAGEN PERSISTENTE CON OPACIDAD)
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
URL_MERCHANDISING = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Merchandising"

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

# === 2.1. MENÚ PRINCIPAL ===
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
            st.session_state.current_menu = "MERCHANDISING" # <-- Guarda "MERCHANDISING"
            st.rerun()
        if st.button("Cerrar Sesión"):
            st.session_state.authenticated = False
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

# === 2.2. PANTALLA: MENÚ CLUB ===
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
   
    # === 2.1 PANTALLA: REUNIONES (Listado con tus Columnas Reales) ===
    elif st.session_state.current_menu == "REUNIONES_MENU":
        st.title("REUNIONES Y ACTAS")
        col_reun1, col_reun2 = st.columns(2)
        with col_reun1:
            if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                if st.button("➕ AÑADIR REUNIÓN"):
                    st.session_state.edit_reunion_data = None
                    st.session_state.modo_consulta = False
                    st.session_state.current_menu = "REUNIONES_CREAR"
                    st.rerun()
        with col_reun2:
            if st.button("⬅️ VOLVER"):
                st.session_state.current_menu = "CLUB_MENU"
                st.rerun()
        st.write("---")
        try:
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
                    st.markdown(f"### 🗓️ {row['Fecha']} — {row['Tipo']}")
                    st.write(f"**Resumen / Orden del día:** {row['Resumen']}")
                    if 'Miembros' in df_filtrado.columns and pd.notna(row['Miembros']) and str(row['Miembros']).strip() != "":
                        st.markdown(f"👥 **Asistentes:** *{row['Miembros']}*")
                    if 'Enlace PDF' in df_filtrado.columns and pd.notna(row['Enlace PDF']) and str(row['Enlace PDF']).strip() != "":
                        st.markdown(f"[📥 Descargar Acta PDF]({row['Enlace PDF']})")
                    if 'Enviar por correo' in df_filtrado.columns and row['Enviar por correo'] == "SÍ":
                        st.caption("📧 *Esta acta fue marcada para difusión por correo electrónico.*")
                    
                    if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                        if st.button("📝 EDITAR REUNIÓN", key=f"edit_reun_{index}"):
                            st.session_state.edit_reunion_data = row.to_dict()
                            st.session_state.modo_consulta = False
                            st.session_state.current_menu = "REUNIONES_CREAR"
                            st.rerun()
                    else:
                        if st.button("👁️ CONSULTAR REUNIÓN", key=f"view_reun_{index}"):
                            st.session_state.edit_reunion_data = row.to_dict()
                            st.session_state.modo_consulta = True
                            st.session_state.current_menu = "REUNIONES_CREAR"
                            st.rerun()
                    st.write("<hr style='border:1px dashed #D4AF37'>", unsafe_allow_html=True)
            else:
                st.warning("No se encontraron reuniones guardadas.")
        except Exception as e:
            st.error(f"Error de lectura en la hoja: {e}")

    # === 2.2 PANTALLA: CREAR / EDITAR REUNIÓN ===
    elif st.session_state.current_menu == "REUNIONES_CREAR":
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
        
        fecha_cruda = datos_previos.get('Fecha', "")
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
        miembros_actuales = datos_previos.get('Miembros', "")
        
        fecha_reunion = st.date_input("FECHA DE LA REUNIÓN", value=fecha_inicial_dt, disabled=es_consulta)
        tipos_disponibles = ["Ordinaria", "Extraordinaria", "Voto de colores", "Asamblea General"]
        idx_tipo = tipos_disponibles.index(tipo_actual) if tipo_actual in tipos_disponibles else 0
        tipo_reunion = st.selectbox("TIPO DE REUNIÓN", tipos_disponibles, index=idx_tipo, disabled=es_consulta)
        descripcion_reunion = st.text_area("RESUMEN / ORDEN DEL DÍA", value=resumen_actual, disabled=es_consulta)
        enlace_acta = st.text_input("ENLACE AL PDF DEL ACTA (Opcional)", value=pdf_actual, disabled=es_consulta)
        enviar_mail_check = st.checkbox("📬 Enviar copia del acta por correo a todo el club", value=(correo_actual == "SÍ"), disabled=es_consulta)
        string_correo = "SÍ" if enviar_mail_check else "NO"
        
        st.subheader("👥 CONTROL DE ASISTENCIA")
        st.write("Selecciona los oficiales y miembros presentes:")
        asistentes_antiguos = [m.strip() for m in str(miembros_actuales).split(",") if m.strip()]
        asistentes_lista = []
        try:
            df_usuarios = pd.read_csv(URL_USUARIOS)
            df_usuarios.columns = df_usuarios.columns.str.strip()
            listado_miembros = sorted(df_usuarios['Alias'].dropna().astype(str).unique())
            for miembro in listado_miembros:
                marcado_defecto = miembro in asistentes_antiguos if (es_edicion or es_consulta) else True
                if st.checkbox(f"🇲🇨 {miembro}", value=marcado_defecto, key=f"reun_real_{miembro}", disabled=es_consulta):
                    asistentes_lista.append(miembro)
        except Exception as e:
            st.warning("No se pudo enlazar la lista de miembros de la pestaña Usuarios.")
            
        string_asistentes_comas = ", ".join(asistentes_lista)
        st.write("---")
        
# --- ZONA DE ACCIÓN: COLUMNAS DE LOS BOTONES AL FINAL ---
        texto_boton_principal = "ACTUALIZAR CAMBIOS" if es_edicion else "GUARDAR REUNIÓN"
        col_accion1, col_accion2 = st.columns(2)
        
        with col_accion1:
            if not es_consulta:
                if st.button(texto_boton_principal):
                    if descripcion_reunion:
                        fecha_formateada = fecha_reunion.strftime('%d/%m/%Y')
                        URL_DIRECTA = "https://google.com"
                        
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
                            res = requests.post(URL_DIRECTA, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                            if "OK_REUNION" in res.text:
                                st.success("🎉 ¡Reunión guardada con éxito!")
                                import time
                                time.sleep(2.0)
                                st.session_state.edit_reunion_data = None
                                st.session_state.modo_consulta = False
                                st.session_state.current_menu = "REUNIONES_MENU"
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
            texto_volver = "🔙 VOLVER AL LISTADO" if es_consulta else "❌ CANCELAR"
            if st.button(texto_volver):
                st.session_state.edit_reunion_data = None
                st.session_state.modo_consulta = False
                st.session_state.current_menu = "REUNIONES_MENU"
                st.rerun()

                                
### Bloc de NORMATIVA (`NORMATIVA_VER` i `NORMATIVA_CREAR`)
    # === 3.1 PANTALLA: VISUALIZAR NORMATIVA ===
    elif st.session_state.current_menu == "NORMATIVA_VER":
        st.title("NORMATIVA INTERNA")
        col_botones1, col_botones2 = st.columns(2)
        with col_botones1:
            if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                if st.button("➕ AÑADIR NORMA"):
                    st.session_state.edit_norma_data = None
                    st.session_state.modo_consulta_norma = False
                    st.session_state.current_menu = "NORMATIVA_CREAR"
                    st.rerun()
        with col_botones2:
            if st.button("⬅️ VOLVER"):
                st.session_state.current_menu = "OLD_RIDERS_MENU"
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
                df_filtrado = df_filtrado[
                    df_filtrado['Tipo'].astype(str).str.lower().str.contains(busqueda) |
                    df_filtrado['Subtipo'].astype(str).str.lower().str.contains(busqueda) |
                    df_filtrado['Descripcion'].astype(str).str.lower().str.contains(busqueda)
                ]
            
            if not df_filtrado.empty:
                for index, row in df_filtrado.iterrows():
                    st.markdown(f"### 📌 {row['Subtipo']}")
                    st.caption(f"Categoría: {row['Tipo']}")
                    st.write(row['Descripcion'])
                    if 'Tiempo' in df_filtrado.columns and pd.notna(row['Tiempo']):
                        st.markdown(f"⏱️ **Vigencia:** *{row['Tiempo']}*")
                    
                    if rol in ["Presidente", "Vicepresidente", "Secretario", "Administrador"]:
                        if st.button("📝 EDITAR REGLA", key=f"edit_{index}"):
                            st.session_state.edit_norma_data = {
                                "indice_fila": int(index),
                                "tipo": row['Tipo'],
                                "subtipo": row['Subtipo'],
                                "descripcion": row['Descripcion'],
                                "tiempo": row['Tiempo']
                            }
                            st.session_state.modo_consulta_norma = False
                            st.session_state.current_menu = "NORMATIVA_CREAR"
                            st.rerun()
                    else:
                        if st.button("👁️ CONSULTAR REGLA", key=f"view_{index}"):
                            st.session_state.edit_norma_data = {
                                "indice_fila": int(index),
                                "tipo": row['Tipo'],
                                "subtipo": row['Subtipo'],
                                "descripcion": row['Descripcion'],
                                "tiempo": row['Tiempo']
                            }
                            st.session_state.modo_consulta_norma = True
                            st.session_state.current_menu = "NORMATIVA_CREAR"
                            st.rerun()
                    st.write("<hr style='border:1px dashed #D4AF37'>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ No se encontraron normas con esos criterios.")
        except Exception as e:
            st.error(f"Error de conexión o lectura: {e}")

# === 3.2 PANTALLA: CREAR / EDITAR / CONSULTAR NORMATIVA ===
    elif st.session_state.current_menu == "NORMATIVA_CREAR":
        es_edicion = st.session_state.get("edit_norma_data") is not None
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
            
            st.write("---")
            if not es_consulta:
                texto_boton = "ACTUALIZAR CAMBIOS" if es_edicion else "GUARDAR NORMA"
                if st.button(texto_boton):
                    if descripcion_norma and tiempo_norma:
                        URL_PROCESADOR_GOOGLE = "https://google.com"
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
                        if "OK_CREAR" in respuesta.text or "OK_EDITAR" in respuesta.text:
                            st.success("👍 ¡Norma procesada con éxito!")
                            import time
                            time.sleep(2.0)
                            st.session_state.edit_norma_data = None
                            st.session_state.modo_consulta_norma = False
                            st.session_state.current_menu = "NORMATIVA_VER"
                            st.rerun()
                        else:
                            st.error("Google rechazó la operación.")
            else:
                st.info("ℹ️ Estás en modo consulta (Lectura).")
        except Exception as e:
            st.error(f"Error en el módulo de datos: {e}")
            
        texto_volver = "🔙 VOLVER AL LISTADO" if es_consulta else "🔙 VOLVER"
        if st.button(texto_volver, key="btn_volver_crear"):
            st.session_state.edit_norma_data = None
            st.session_state.modo_consulta_norma = False
            st.session_state.current_menu = "NORMATIVA_VER"
            st.rerun()

# === 3.3 PANTALLA: HISTÒRIA DEL CLUB ===
    elif st.session_state.current_menu == "HISTORIA_VER":
        st.title("HISTORIA DEL CLUB")
        st.markdown("""
        ### 📜 **Fundación**
        Fundado un **16 de septiembre del 2017** por un grupo de 8 antiguos motoristas de diferentes moto clubs y algún otro.  
        Después de un tiempo, algunos nos dejaron y otros se fueron a recorrer las autopistas del cielo.
        
        ### 🦅 **Evolución**
        Tras unos años de andadura nos convertimos en **MC en 2026** bajo los valores de:
        * Amistad
        * Rutas
        * Libertad
        * Hermandad
        * Pasión por las motos.
        
        ### 🖤 **In memoriam**
        **Sebas 1967-2022**
        """)
        if st.button("⬅️ VOLVER"):
            st.session_state.current_menu = "OLD_RIDERS_MENU"
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
    elif st.session_state.current_menu == "USUARIOS_FICHA" or st.session_state.get("pantalla") == "USUARIOS_FICHA":
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
            
# La columna identificadora oficial per al desplegable és 'Alias'
            col_identificador = 'Alias'
            df_usuarios[col_identificador] = df_usuarios[col_identificador].astype(str).str.strip()
            
# Selector interactiu de socis per el seu Alias
            lista_miembros = sorted(df_usuarios[col_identificador].unique())
            miembro_sel = st.selectbox("Selecciona un miembro para gestionar su ficha:", ["-- Seleccionar miembro --"] + lista_miembros)
            
            st.write("---")
            
            if miembro_sel != "-- Seleccionar miembro --":
# Filtrem la fila del membre elegit
                fila_filtrada = df_usuarios[df_usuarios[col_identificador] == miembro_sel]
                
# Calculem la línia real del Sheets (+2 per capçalera i desplaçament de Python)
                num_fila_sheets = int(fila_filtrada.index[0]) + 2
                
# Extraiem les dades de la primera coincidència de forma 100% segura
                datos_miembro = fila_filtrada.iloc[0]
                
                bloqueado = not puede_editar
                
# INTERFÍCIE EN COLUMNES ADAPTADA A LES TEVES CABESES REALS
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Datos de Identidad")
                    st.text_input("ID de Registro", value=str(datos_miembro.get('ID', '')), disabled=True)
                    alias_val = st.text_input("Alias / Nombre en Club", value=str(datos_miembro.get('Alias', miembro_sel)), disabled=bloqueado)
                    nombre_val = st.text_input("Nombre Real", value=str(datos_miembro.get('Nombre', '')), disabled=bloqueado)
                    apellido_val = st.text_input("Apellido", value=str(datos_miembro.get('Apellido', '')), disabled=bloqueado)
                    email_val = st.text_input("Email", value=str(datos_miembro.get('Email', '')), disabled=bloqueado)
                    telefono_val = st.text_input("Teléfono", value=str(datos_miembro.get('Telefono', '')), disabled=bloqueado)
                    nacimiento_val = st.text_input("Fecha de Nacimiento (DD/MM/AAAA)", value=str(datos_miembro.get('Fecha_Nacimiento', '')), disabled=bloqueado)
                
                with col2:
                    st.subheader("Estado y Gestión")
                    
# Selector de càrrecs del club (s'adapta exactament al teu 'miembro' en minúscula)
                    lista_cargos = ["Presidente", "Vicepresidente", "Secretario", "Tesorero", "Capitán de Ruta", "Sargento de Armas", "miembro", "Prospect", "Handground"]
                    cargo_actual = str(datos_miembro.get('Rol', 'miembro')).strip()
                    idx_cargo = lista_cargos.index(cargo_actual) if cargo_actual in lista_cargos else 6
                    
                    cargo_val = st.selectbox("Cargo / Rol", lista_cargos, index=idx_cargo, disabled=bloqueado)
                    
                    inicio_val = st.text_input("Fecha Inicio (DD/MM/AAAA)", value=str(datos_miembro.get('Inicio', '')), disabled=bloqueado)
                    final_val = st.text_input("Fecha Final / Baja", value=str(datos_miembro.get('Final', '')), disabled=bloqueado)
                    estado_val = st.text_input("Estado (Ej: Vigente)", value=str(datos_miembro.get('Estado', 'Vigente')), disabled=bloqueado)
                    
                    # Contrasenya de seguretat
                    contrasena_actual = str(datos_miembro.get('Contrasena', ''))
                    if puede_editar:
                        contrasena_val = st.text_input("Contraseña Acceso App", value=contrasena_actual, type="password")
                    else:
                        contrasena_val = contrasena_actual
                
                st.write("---")
                st.subheader("Sección de Notas Internas")
                observaciones_val = st.text_area("Observaciones del Miembro", value=str(datos_miembro.get('Observaciones', '')), disabled=bloqueado)
                
                # === ACCIÓ DE GUARDAR DADES ===
                if puede_editar:
                    if st.button("💾 GUARDAR Y ACTUALIZAR CAMBIOS"):
                        import requests
                        import json
                        import time
                        
                        # Construïm el paquet clavat a les columnes de la teva imatge
                        payload = {
                            "accion": "editar_usuario",
                            "num_fila": num_fila_sheets,
                            "ID": str(datos_miembro.get('ID', '')),
                            "Alias": alias_val,
                            "Nombre": nombre_val,
                            "Apellido": apellido_val,
                            "Email": email_val,
                            "Telefono": telefono_val,
                            "Rol": cargo_val,
                            "Inicio": inicio_val,
                            "Final": final_val,
                            "Estado": estado_val,
                            "Observaciones": observaciones_val,
                            "Contrasena": contrasena_val,
                            "Fecha_Nacimiento": nacimiento_val
                        }
                        
                        URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
                        
                        with st.spinner("Sincronizando cambios con Google Sheets..."):
                            try:
                                respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                                if "OK" in respuesta.text or "éxito" in respuesta.text:
                                    st.success(f"🎉 ¡Ficha de {alias_val} guardada con éxito!")
                                    time.sleep(1.5)
                                    st.rerun()
                                else:
                                    st.error(f"Respuesta del servidor de Google: {respuesta.text}")
                            except Exception as err:
                                st.error(f"Error al conectar con el servidor: {err}")
                        
        except Exception as e:
            st.error(f"Error de lectura en la hoja 'Usuarios': {e}")
            
        if st.button("⬅️ VOLVER"):
            st.session_state.current_menu = "OLD_RIDERS_MENU"
            st.session_state.pantalla = "OLD_RIDERS_MENU"
            st.rerun()
        
# === VISTAS DE CONTENIDO MACRO  ===
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

# === 5. PANTALLA: MENÚ MERCHANDISING (CORREGIDO EL CONFLICTO DE NOMBRES) ===
    elif st.session_state.current_menu == "PANTALLA_MERCHANDISING" or st.session_state.current_menu == "MERCHANDISING":
        st.title("👕 MERCHANDISING")
        
        if st.button("CONSULTAR PRODUCTOS"):
            st.session_state.current_menu = "MERCH_CONSULTAR"
            st.rerun()
            
        if st.button("NUEVO PRODUCTO"):
            st.session_state.current_menu = "MERCH_NUEVO_PRODUCTO"
            st.rerun()
            
        if st.button("NUEVO PEDIDO"):
            st.session_state.current_menu = "MERCH_NUEVO_PEDIDO"
            st.rerun()
            
        st.write("---")
        
        # Botones inferiores de navegación en dos columnas (Volver / Salir)
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("⬅️ VOLVER"):
                st.session_state.current_menu = "PRINCIPAL"
                st.rerun()
        with col_nav2:
            if st.button("❌ SALIR"):
                st.session_state.authenticated = False
                st.session_state.current_menu = "PRINCIPAL"
                st.rerun()

# === 5.1 SUBPANTALLA: CONSULTAR PRODUCTOS ===
    elif st.session_state.current_menu == "MERCH_CONSULTAR":
        st.title("📦 INVENTARIO DE PRODUCTOS")
        st.write("Consulta el stock disponible de chalecos, parches, camisetas y material oficial.")
        st.write("---")
        
        try:
            # 1. Leer los datos de la pestaña Merchandising
            df_merch = pd.read_csv(URL_MERCHANDISING)
            df_merch.columns = df_merch.columns.str.strip()
            
            if not df_merch.empty:
                # Buscador rápido por nombre de producto
                busqueda_prod = st.text_input("🔍 Buscar Producto por nombre...").strip().lower()
                
                df_filtrado_merch = df_merch.copy()
                if busqueda_prod:
                    df_filtrado_merch = df_filtrado_merch[df_filtrado_merch['Producto'].astype(str).str.lower().str.contains(busqueda_prod)]
                
                # Mostrar el inventario en una tabla bonita de Streamlit
                st.dataframe(df_filtrado_merch, use_container_width=True, hide_index=True)
            else:
                st.info("No hay productos registrados en el inventario todavía.")
                
        except Exception as e:
            st.error(f"Error de lectura en la hoja Merchandising: {e}")
            
        if st.button("🔙 VOLVER"):
            st.session_state.current_menu = "PANTALLA_MERCHANDISING"
            st.rerun()

    # === 5.2 SUBPANTALLA: NUEVO PRODUCTO (FORMULARIO E INTEGRACIÓN) ===
    elif st.session_state.current_menu == "MERCH_NUEVO_PRODUCTO":
        st.title("➕ AÑADIR NUEVO PRODUCTO")
        
        # Validamos que solo los roles autorizados puedan añadir material al inventario
        if rol not in ["Presidente", "Vicepresidente", "Tesorero", "Administrador"]:
            st.warning("⚠️ No tienes permisos para añadir productos al inventario.")
            if st.button("🔙 VOLVER"):
                st.session_state.current_menu = "PANTALLA_MERCHANDISING"
                st.rerun()
        else:
            st.write("Introduce los datos del nuevo artículo para el catálogo del club.")
            st.write("---")
            
            import requests
            import json
            import time
            
# Formulario organizado con tus columnas reales
            col1, col2 = st.columns(2)
            with col1:
                id_prod = st.text_input("ID del Producto (Ej: Id_chaleco1)")
                nombre_prod = st.text_input("Nombre del Producto (Ej: Camiseta Oficial)")
                talla_prod = st.text_input("Talla (Ej: XL / Única / No aplica)")
                precio_prod = st.text_input("Precio (€)")
            with col2:
                proveedor_prod = st.text_input("Nombre del Proveedor")
                tel_proveedor_prod = st.text_input("Teléfono del Proveedor")
                stock_prod = st.number_input("Stock Inicial Disponibles", min_value=0, value=10, step=1)
                
            desc_prod = st.text_area("Descripción detallada del producto")
            
            st.write("---")
            
            if st.button("💾 GUARDAR PRODUCTO EN SHEET"):
                if id_prod and nombre_prod and precio_prod:
                    # Creamos el paquete exacto para mandarlo al Apps Script
                    payload = {
                        "accion": "crear_producto_merch",
                        "Id_Producto": id_prod,
                        "Producto": nombre_prod,
                        "Talla": talla_prod,
                        "Precio": precio_prod,
                        "Proveedor": proveedor_prod,
                        "Tel_Proveedor": tel_proveedor_prod,
                        "Descripcion": desc_prod,
                        "Stock": int(stock_prod)
                    }
                    
                    URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
                    
                    with st.spinner("Guardando nuevo artículo en Google Sheets..."):
                        try:
                            respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                            if "OK_MERCH" in respuesta.text:
                                st.success("🎉 ¡Nuevo producto añadido con éxito al inventario!")
                                time.sleep(1.5)
                                st.session_state.current_menu = "PANTALLA_MERCHANDISING"
                                st.rerun()
                            else:
                                st.error(f"Respuesta inesperada del servidor de Google: {respuesta.text}")
                        except Exception as err:
                            st.error(f"Error de conexión al guardar el producto: {err}")
                else:
                    st.warning("Por favor, rellena obligatoriamente los campos ID, Nombre y Precio antes de continuar.")
                    
            if st.button("❌ CANCELAR"):
                st.session_state.current_menu = "PANTALLA_MERCHANDISING"
                st.rerun()
                
       # === 5.3 SUBPANTALLA: REGISTRAR NUEVO PEDIDO (CON TALLAS Y GUARDADO REAL) ===
    elif st.session_state.current_menu == "MERCH_NUEVO_PEDIDO":
        st.title("🛒 REGISTRAR NUEVO PEDIDO")
        st.write("Apunta las compras o reservas de material oficial que realizan los miembros.")
        st.write("---")
        
        try:
            # 1. Descargamos los datos para cruzarlos en tiempo real
            df_socios = pd.read_csv(URL_USUARIOS)
            df_socios.columns = df_socios.columns.str.strip()
            
            df_articulos = pd.read_csv(URL_MERCHANDISING)
            df_articulos.columns = df_articulos.columns.str.strip()
            
            if not df_socios.empty and not df_articulos.empty:
                import requests
                import json
                import time
                from datetime import datetime
                
                # Generador automático de ID único de pedido basado en el momento exacto
                id_pedido_automatico = f"PED_{datetime.now().strftime('%Y%M%d_%H%M%S')}"
                
                # SELECTOR DE MIEMBRO
                col_socio = 'Alias' if 'Alias' in df_socios.columns else 'Nombre'
                lista_socios = sorted(df_socios[col_socio].dropna().astype(str).unique())
                socio_pedido = st.selectbox("👤 ¿Qué miembro realiza el pedido?", ["-- Seleccionar Socio --"] + lista_socios)
                
                # SELECTOR DE PRODUCTO
                lista_productos = sorted(df_articulos['Producto'].dropna().astype(str).unique())
                producto_pedido = st.selectbox("📦 ¿Qué artículo se lleva?", ["-- Seleccionar Artículo --"] + lista_productos)
                
                # FILTRADO DINÁMICO DE TALLAS SEGÚN EL PRODUCTO SELECCIONADO
                tallas_disponibles = ["Única"]
                if producto_pedido != "-- Seleccionar Artículo --":
                    # Filtramos en tu hoja de Merchandising para extraer las tallas registradas para ese producto concreto
                    filas_prod = df_articulos[df_articulos['Producto'] == producto_pedido]
                    tallas_disponibles = sorted(filas_prod['Talla'].dropna().astype(str).unique())
                
                # SELECTOR DE TALLA (¡Añadido perfectamente!)
                talla_seleccionada = st.selectbox("📏 Talla disponible del producto:", tallas_disponibles)
                
                col_cant, col_entrega = st.columns(2)
                with col_cant:
                    cantidad = st.number_input("Cantidad de unidades", min_value=1, value=1, step=1)
                with col_entrega:
                    estado_entrega = st.radio("Estado de la Entrega", ["Entregado", "Reservado / Pendiente"], horizontal=True)
                    
                st.write("---")
                
                # BOTÓN DE ACCIÓN COMPLETO CON POST HACIA GOOGLE APPS SCRIPT
                if st.button("🛒 ENCARGAR Y GUARDAR PEDIDO"):
                    if socio_pedido != "-- Seleccionar Socio --" and producto_pedido != "-- Seleccionar Artículo --":
                        
                        payload = {
                            "accion": "guardar_pedido_merch",
                            "Id_Pedido": id_pedido_automatico,
                            "Fecha": datetime.now().strftime("%d/%m/%Y"),
                            "Socio": socio_pedido,
                            "Producto": producto_pedido,
                            "Talla": talla_seleccionada,
                            "Cantidad": int(cantidad),
                            "Estado_Entrega": estado_entrega
                        }
                        
                        URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
                        
                        with st.spinner("Registrando pedido en el histórico de Google Sheets..."):
                            try:
                                respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                                if "OK" in respuesta.text or "éxito" in respuesta.text:
                                    st.success(f"🎉 Pedido de {socio_pedido} guardado con éxito en la pestaña 'Pedidos'.")
                                    time.sleep(1.5)
                                    st.session_state.current_menu = "PANTALLA_MERCHANDISING"
                                    st.rerun()
                                else:
                                    st.error(f"Fallo en la respuesta de Google: {respuesta.text}")
                            except Exception as err:
                                st.error(f"Error de red al guardar el pedido: {err}")
                    else:
                        st.warning("Por favor, selecciona obligatoriamente un miembro y un producto antes de confirmar.")
            else:
                st.error("Necesitas tener miembros e inventario cargados previamente para procesar encargos.")
                
        except Exception as e:
            st.error(f"Error al cruzar las bases de datos para el pedido: {e}")
            
        if st.button("🔙 VOLVER"):
            st.session_state.current_menu = "PANTALLA_MERCHANDISING"
            st.rerun()

# Marcadores de posición para el resto de pantallas (Normativa, Historia, etc.)
    elif st.session_state.current_menu in ["REUNIONES_MENU", "NORMATIVA_VER", "HISTORIA_VER"]:
        st.title(st.session_state.current_menu.replace("_", " "))
        st.info("Sección temporalmente en desarrollo...")
        if st.button("VOLVER"):
            st.session_state.current_menu = "OLD_RIDERS_MENU" if "MENU" not in st.session_state.current_menu else "CLUB_MENU"
            st.rerun()
