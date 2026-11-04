import streamlit as st
import pandas as pd
import base64
import time
import requests
import json

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
URL_PEDIDOS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Pedidos"
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
                        URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
                        
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
        
# === VISTAS DE CONTENIDO  ===
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

# ==============================================================================
# === 5. ZONA DE MERCHANDISING (MÓDULO INDEPENDIENTE PARA EVITAR ERRORES) ======
# ==============================================================================
# 🔐 CONTROL DE ACCESOS Y ROLES DIRECTIVOS
rol_actual = st.session_state.get("user_role", None)
ROLES_AUTORIZADOS = ["Presidente", "Vicepresidente", "Secretario", "Tesorero"]
es_directiva = rol_actual in ROLES_AUTORIZADOS

URL_PEDIDOS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Pedidos"
URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"

if st.session_state.current_menu in ["PANTALLA_MERCHANDISING", "MERCHANDISING"]:
    st.title("👕 MERCHANDISING")
    if st.button("CONSULTAR PRODUCTOS"):
        st.session_state.current_menu = "MERCH_CONSULTAR"
        st.rerun()
    if st.button("CONSULTAR PEDIDOS / RESERVAS"):
        st.session_state.current_menu = "MERCH_PEDIDOS"
        st.rerun()
    if st.button("NUEVO PRODUCTO"):
        st.session_state.current_menu = "MERCH_NUEVO_PRODUCTO"
        st.rerun()
    if st.button("NUEVO PEDIDO"):
        st.session_state.current_menu = "MERCH_NUEVO_PEDIDO"
        st.rerun()
    st.write("---")
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ VOLVER", key="btn_volver_merch_principal"):
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()
    with col_nav2:
        if st.button("❌ SALIR", key="btn_salir_merch_principal"):
            st.session_state.authenticated = False
            st.session_state.current_menu = "PRINCIPAL"
            st.rerun()

# === 5.1 SUBPANTALLA: CONSULTAR PRODUCTOS (CON ACCESO PROTEGIDO) ===
elif st.session_state.current_menu == "MERCH_CONSULTAR":
    st.title("📦 INVENTARIO DE PRODUCTOS")
    st.write("Consulta y gestiona el stock disponible del material oficial del club.")
    st.write("---")
    
    rol_actual = st.session_state.get("user_role", None)
    roles_autorizados = ["Presidente", "Vicepresidente", "Secretario", "Tesorero", "Administrador"]
    
    try:
        df_merch = pd.read_csv(URL_MERCHANDISING)
        df_merch.columns = df_merch.columns.str.strip()
        
        if not df_merch.empty:
            busqueda_prod = st.text_input("🔍 Buscar Producto por nombre...").strip().lower()
            df_filtrado_merch = df_merch.copy()
            if busqueda_prod:
                df_filtrado_merch = df_filtrado_merch[df_filtrado_merch['Producto'].astype(str).str.lower().str.contains(busqueda_prod)]
            
            st.write("---")
            
            for index, row in df_filtrado_merch.iterrows():
                num_fila_producto = int(index) + 2
                
                with st.container():
                    if rol_actual in roles_autorizados:
                        col_info, col_accion_edit, col_accion_elim = st.columns([3, 0.8, 0.8])
                    else:
                        col_info = st.container()
                        col_accion_edit, col_accion_elim = None, None
                    
                    with col_info:
                        st.markdown(f"📦 **[{row['Id_Producto']}] {row['Producto']}** — **Precio:** {row['Precio']}€")
                        st.caption(f"🏬 Proveedor: {row['Proveedor']} ({row['Tel_Proveedor']}) | 📊 Stock Actual: {row['Stock']} u.")
                        if pd.notna(row['Descripcion']) and str(row['Descripcion']).strip() != "":
                            st.info(f"📝 *{row['Descripcion']}*")                   
 # Inicializar estado para controlar qué producto se está editando
                    if f"editando_{index}" not in st.session_state:
                        st.session_state[f"editando_{index}"] = False

                    if col_accion_edit is not None and col_accion_elim is not None:
                        with col_accion_edit:
                            if st.button("✏️ EDITAR", key=f"btn_editar_prod_{index}"):
                                st.session_state[f"editando_{index}"] = not st.session_state[f"editando_{index}"]
                        
                        with col_accion_elim:
                            if st.button("❌ ELIMINAR", key=f"btn_eliminar_prod_{index}"):
                                import requests
                                import json
                                import time
                                payload = {
                                    "accion": "eliminar_producto_merch",
                                    "num_fila": num_fila_producto
                                }
                                with st.spinner("Borrando producto del inventario general..."):
                                    try:
                                        respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                                        if "OK" in respuesta.text or "éxito" in respuesta.text:
                                            st.success(f"🗑️ '{row['Producto']}' eliminado.")
                                            time.sleep(1.0)
                                            st.rerun()
                                        else:
                                            st.error(f"Fallo del servidor: {respuesta.text}")
                                    except Exception as err:
                                        st.error(f"Error de conexión: {err}")

                        # Formulario dinámico de edición si se pulsa "EDITAR"
                        if st.session_state[f"editando_{index}"]:
                            with st.expander(f"✏️ Modificar datos de: {row['Producto']}", expanded=True):
                                form_key = f"form_edit_{index}"
                                with st.form(key=form_key):
                                    nuevo_nombre = st.text_input("Nombre del Producto", value=str(row['Producto']))
                                    nuevo_precio = st.number_input("Precio (€)", value=float(row['Precio']), step=0.5)
                                    nuevo_stock = st.number_input("Stock Actual", value=int(row['Stock']), step=1)
                                    nuevo_proveedor = st.text_input("Proveedor", value=str(row['Proveedor']))
                                    nuevo_tel = st.text_input("Teléfono Proveedor", value=str(row['Tel_Proveedor']))
                                    nueva_desc = st.text_area("Descripción", value=str(row['Descripcion']) if pd.notna(row['Descripcion']) else "")
                                    
                                    btn_guardar = st.form_submit_button("💾 Guardar Cambios")
                                    if btn_guardar:
                                        import requests
                                        import json
                                        import time
                                        
                                        payload_edit = {
                                            "accion": "editar_producto_merch",
                                            "num_fila": num_fila_producto,
                                            "producto": nuevo_nombre,
                                            "precio": nuevo_precio,
                                            "stock": nuevo_stock,
                                            "proveedor": nuevo_proveedor,
                                            "tel_proveedor": nuevo_tel,
                                            "descripcion": nueva_desc
                                        }
                                        
                                        with st.spinner("Actualizando producto en la base de datos..."):
                                            try:
                                                respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload_edit), headers={"Content-Type": "application/json"})
                                                if "OK" in respuesta.text or "éxito" in respuesta.text:
                                                    st.success("✨ Producto actualizado correctamente.")
                                                    st.session_state[f"editando_{index}"] = False
                                                    time.sleep(1.0)
                                                    st.rerun()
                                                else:
                                                    st.error(f"Fallo del servidor: {respuesta.text}")
                                            except Exception as err:
                                                st.error(f"Error de conexión: {err}")
                    st.write("---")
        else:
            st.info("No hay productos registrados en el inventario todavía.")
            
    except Exception as e:
        st.error(f"Error de lectura en la hoja Merchandising: {e}")
        
    if st.button("🔙 VOLVER", key="btn_volver_consultar"):
        st.session_state.current_menu = "PANTALLA_MERCHANDISING"
        st.rerun()
# === 5.2 SUBPANTALLA: NUEVO PRODUCTO ===
elif st.session_state.current_menu == "MERCH_NUEVO_PRODUCTO":
    # Control estricto de seguridad basado en tus variables de rol oficiales
    rol_actual = st.session_state.user_role
    roles_autorizados = ["Presidente", "Vicepresidente", "Secretario", "Tesorero", "Administrador"]
    
    if rol_actual not in roles_autorizados:
        st.error("⛔ ACCESO DENEGADO: No tienes permisos para registrar nuevos artículos.")
        if st.button("⬅️ VOLVER AL MENÚ", key="btn_error_nuevo_prod"):
            st.session_state.current_menu = "PANTALLA_MERCHANDISING"
            st.rerun()
    else:
        st.title("➕ REGISTRAR NUEVO PRODUCTO")
        st.write("Introduce los datos del nuevo artículo para el inventario general.")
        st.write("---")
        
        id_prod = st.text_input("ID Producto (Ej: PROD001)")
        nombre_prod = st.text_input("Nombre del Producto")
        precio_prod = st.number_input("Precio (€)", min_value=0.0, step=0.5)
        proveedor = st.text_input("Proveedor")
        tel_proveedor = st.text_input("Teléfono Proveedor")
        descripcion = st.text_area("Descripción")
        stock_inicial = st.number_input("Stock Inicial", min_value=0, step=1)
        
        if st.button("💾 GUARDAR PRODUCTO"):
            if id_prod and nombre_prod:
                URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
                payload = {
                    "accion": "crear_producto_merch",
                    "Id_Producto": id_prod,
                    "Producto": nombre_prod,
                    "Precio": float(precio_prod),
                    "Proveedor": proveedor,
                    "Tel_Proveedor": tel_proveedor,
                    "Descripcion": descripcion,
                    "Stock": int(stock_inicial)
                }
                
                import requests
                import json
                import time
                
                with st.spinner("Registrando nuevo artículo en el inventario..."):
                    try:
                        respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                        if "OK" in respuesta.text or "MERCH" in respuesta.text:
                            st.success(f"🎉 ¡Producto '{nombre_prod}' guardado con éxito en Google Sheets!")
                            time.sleep(1.5)
                            st.session_state.current_menu = "PANTALLA_MERCHANDISING"
                            st.rerun()
                        else:
                            st.error(f"Fallo del servidor de Google: {respuesta.text}")
                    except Exception as err:
                        st.error(f"Error de conexión al guardar el producto: {err}")
            else:
                st.error("Por favor, rellena los campos obligatorios (ID y Nombre).")
                
        if st.button("⬅️ VOLVER AL MENÚ", key="btn_volver_nuevo_prod"):
            st.session_state.current_menu = "PANTALLA_MERCHANDISING"
            st.rerun()

# === 5.3 SUBPANTALLA: NUEVO PEDIDO ===
elif st.session_state.current_menu == "MERCH_NUEVO_PEDIDO":
    # Control estricto de seguridad basado en tus variables de rol oficiales
    rol_actual = st.session_state.user_role
    roles_autorizados = ["Presidente", "Vicepresidente", "Secretario", "Tesorero", "Administrador"]
    
    if rol_actual not in roles_autorizados:
        st.error("⛔ ACCESO DENEGADO: No tienes permisos para registrar nuevos pedidos.")
        if st.button("⬅️ VOLVER", key="btn_error_nuevo_pedido"):
            st.session_state.current_menu = "PANTALLA_MERCHANDISING"
            st.rerun()
    else:
        st.title("🛒 REGISTRAR NUEVO PEDIDO")
        st.write("Selecciona el producto y define la talla para este pedido específico.")
        st.write("---")
        try:
            # Carga de productos disponibles desde el inventario de Merchandising
            df_merch = pd.read_csv(URL_MERCHANDISING)
            df_merch.columns = df_merch.columns.str.strip()
            lista_productos = ["-- Seleccionar Artículo --"] + (df_merch['Producto'].dropna().unique().tolist() if not df_merch.empty else [])
            
            socios_disponibles = ["-- Seleccionar Socio --", "General"]
            try:
                # Carga de socios registrados en la pestaña Usuarios
                df_usuarios_ped = pd.read_csv(URL_USUARIOS)
                df_usuarios_ped.columns = df_usuarios_ped.columns.str.strip()
                if 'Alias' in df_usuarios_ped.columns:
                    lista_alias = df_usuarios_ped['Alias'].dropna().unique().tolist()
                    socios_disponibles += [str(a) for a in lista_alias if str(a) != "General"]
            except Exception as e_users:
                st.error(f"Error al cargar la lista de miembros (Alias): {e_users}")
                
            # Selectores de la interfaz
            socio_pedido = st.selectbox("👤 Selecciona el Socio / Miembro:", socios_disponibles)
            producto_pedido = st.selectbox("📦 Selecciona el Producto:", lista_productos)
            
            if producto_pedido != "-- Seleccionar Artículo --":
                tallas_disponibles = ["Única", "S", "M", "L", "XL", "XXL", "3XL", "4XL", "5XL"]
                talla_seleccionada = st.selectbox("📏 Talla para este pedido:", tallas_disponibles)
                
                col_cant, col_entrega = st.columns(2)
                with col_cant:
                    cantidad = st.number_input("Cantidad de unidades", min_value=1, value=1, step=1)
                with col_entrega:
                    estado_entrega = st.radio("Estado de la Entrega", ["Entregado", "Reservado / Pendiente"], index=1, horizontal=True)
                
                st.write("---")
                
                if st.button("📥 ENCARGAR Y GUARDAR PEDIDO"):
                    if socio_pedido != "-- Seleccionar Socio --" and producto_pedido != "-- Seleccionar Artículo --":
                        from datetime import datetime
                        import requests
                        import json
                        import time
                        
                        ahora = datetime.now()
                        id_pedido_automatico = f"PED-{ahora.strftime('%Y%m%d%H%M%S')}"
                        
                        payload = {
                            "accion": "guardar_pedido_merch",
                            "Id_Pedido": id_pedido_automatico,
                            "Fecha": ahora.strftime("%d/%m/%Y"),
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
                                    st.success(f"🛍️ Pedido de '{socio_pedido}' guardado con éxito en la pestaña 'Pedidos'.")
                                    time.sleep(1.5)
                                    st.session_state.current_menu = "PANTALLA_MERCHANDISING"
                                    st.rerun()
                                else:
                                    st.error(f"Fallo en la respuesta de Google: {respuesta.text}")
                            except Exception as err:
                                st.error(f"Error de red al guardar el pedido: {err}")
                    else:
                        st.warning("Por favor, selecciona obligatoriamente un miembro o 'General' y un producto antes de confirmar.")
            else:
                st.info("Por favor, selecciona un artículo para configurar los detalles del encargo.")
                
        except Exception as e:
            st.error(f"Error al procesar las bases de datos para el pedido: {e}")
            
        if st.button("⬅️ VOLVER", key="btn_volver_pedido_final"):
            st.session_state.current_menu = "PANTALLA_MERCHANDISING"
            st.rerun()

# === 5.4 SUBPANTALLA: CONSULTAR PEDIDOS (TODOS CONSULTAN, SOLO DIRECTIVA MODIFICA) ===
elif st.session_state.current_menu == "MERCH_PEDIDOS":
    st.title("📋 CONSULTA DE PEDIDOS Y RESERVAS")
    st.write("Consulta el estado de las reservas de merchandising.")
    st.write("---")
    URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
    
    try:
        # Generamos la URL usando tu SHEET_ID y apuntando a la pestaña 'Pedidos'
              #URL_PEDIDOS = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Pedidos"
        URL_PEDIDOS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Pedidos"
        df_pedidos = pd.read_csv(URL_PEDIDOS)
        df_pedidos.columns = df_pedidos.columns.str.strip()
        
        if not df_pedidos.empty:
            # Creamos una columna temporal con el número de fila real en Google Sheets para no perderlo al filtrar
            df_pedidos['Fila_Sheets'] = df_pedidos.index + 2
            
            # Buscador rápido por texto
            busqueda_ped = st.text_input("🔍 Buscar por Socio o Producto...").strip().lower()
            
            # FILTRO VISUAL RECUPERADO: Selector horizontal para cambiar de vista cómodamente
            filtro_estado = st.radio("Filtrar por estado de entrega:", ["📋 Todos", "⏳ Reservados / Pendientes", "✅ Entregados"], horizontal=True)
            
            df_filtrado_ped = df_pedidos.copy()
            
            # Aplicamos buscador de texto si existe
            if busqueda_ped:
                df_filtrado_ped = df_filtrado_ped[
                    df_filtrado_ped['Socio'].astype(str).str.lower().str.contains(busqueda_ped) |
                    df_filtrado_ped['Producto'].astype(str).str.lower().str.contains(busqueda_ped)
                ]
                
            # Aplicamos el filtro visual seleccionado sin romper los índices reales
            if "Pendientes" in filtro_estado:
                df_filtrado_ped = df_filtrado_ped[df_filtrado_ped['Estado_Entrega'].astype(str).str.contains("Reservado|Pendiente", case=False)]
            elif "Entregados" in filtro_estado:
                df_filtrado_ped = df_filtrado_ped[df_filtrado_ped['Estado_Entrega'].astype(str).str.contains("Entregado", case=False)]
            
            st.write("---")
            
            # Renderizamos la lista filtrada
            for index, row in df_filtrado_ped.iterrows():
                num_fila_pedido = int(row['Fila_Sheets'])
                id_ped_actual = row.get('Id_Pedido', index)
                
                with st.container():
                    col_info, col_accion = st.columns([2.5, 1.5])
                    
                    with col_info:
                        st.markdown(f"🛍️ **Pedido ID:** {id_ped_actual} — 👤 **{row.get('Socio', 'N/A')}**")
                        st.write(f"📦 **Producto:** {row.get('Producto', 'N/A')} | 🔢 **Cantidad:** {row.get('Cantidad', 1)} ud. | 📏 **Talla:** {row.get('Talla', 'N/A')}")
                        
                        estado = str(row.get('Estado_Entrega', 'Reservado / Pendiente')).strip()
                        if "Entregado" in estado:
                            st.success(f"🟢 Estado: {estado}")
                        else:
                            st.warning(f"🟡 Estado: {estado}")
                            
                    with col_accion:
                        # 🔒 Tu regla de control de acceso por roles directivos
                        if rol in ["Presidente", "Vicepresidente", "Tesorero", "Secretario", "Administrador"]:
                            col_b1, col_b2 = st.columns(2)
                            
                            with col_b1:
                                # PATRÓN REUNIONES: Guardamos el pedido en memoria y cambiamos el menú
                                if st.button("📝 EDITAR", key=f"btn_editar_ped_{index}"):
                                    pedido_diccionario = row.to_dict()
                                    pedido_diccionario['Fila_Sheets'] = num_fila_pedido
                                    st.session_state.edit_pedido_data = pedido_diccionario
                                    st.session_state.current_menu = "MERCH_EDITAR_PEDIDO"
                                    st.rerun()
                                    
                            with col_b2:
                                if st.button("❌ ELIMINAR", key=f"btn_eliminar_ped_{index}"):
                                    st.session_state.pedido_a_confirmar = index
                                    st.rerun()
                                    
                            # INTERFÍCIE DE SEGURETAT: Si pulsa eliminar, abre la fianza de confirmación justo debajo
                            if st.session_state.get("pedido_a_confirmar") == index:
                                st.write("")
                                st.error(f"¿Borrar pedido **{id_ped_actual}**?")
                                col_c1, col_c2 = st.columns(2)
                                with col_c1:
                                    if st.button("⚠️ SÍ", key=f"btn_si_conf_{index}"):
                                        payload_del = {
                                            "accion": "eliminar_pedido_merch",
                                            "num_fila": num_fila_pedido
                                        }
                                        with st.spinner("Borrando del Sheets..."):
                                            try:
                                                respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload_del), headers={"Content-Type": "application/json"})
                                                if "OK" in respuesta.text or "éxito" in respuesta.text:
                                                    st.success("Pedido eliminado.")
                                                    st.session_state.pedido_a_confirmar = None
                                                    time.sleep(1.0)
                                                    st.rerun()
                                                else:
                                                    st.error(f"Error: {respuesta.text}")
                                            except Exception as err:
                                                st.error(f"Error de red: {err}")
                                with col_c2:
                                    if st.button("❌ NO", key=f"btn_no_conf_{index}"):
                                        st.session_state.pedido_a_confirmar = None
                                        st.rerun()
                        else:
                            st.caption("🔒 *Solo Lectura*")
                st.write("---")
        else:
            st.info("No hay pedidos registrados en el sistema todavía.")
            
    except Exception as e:
        st.error(f"Error al leer la pestaña Pedidos: {e}")
        
    if st.button("🔙 VOLVER AL MENÚ", key="btn_volver_pedidos"):
        st.session_state.pedido_a_confirmar = None
        st.session_state.current_menu = "PANTALLA_MERCHANDISING"
        st.rerun()


# === 5.5 SUBPANTALLA: MODIFICAR / EDITAR PEDIDO (ENCADENADO CORRECTAMENTE EN LA SECUENCIA DE ELIF) ===
elif st.session_state.current_menu == "MERCH_EDITAR_PEDIDO":
    st.title("📝 MODIFICAR DETALLES DEL PEDIDO")
    st.write("Modifica el estado de la entrega, la cantidad o los datos del encargo.")
    st.write("---")
    
    datos_previos_pedido = st.session_state.get("edit_pedido_data", {})
    fila_editar = datos_previos_pedido.get("Fila_Sheets")
    
    if not datos_previos_pedido:
        st.error("No se han cargado datos para modificar.")
        if st.button("⬅️ VOLVER"):
            st.session_state.current_menu = "MERCH_PEDIDOS"
            st.rerun()
    else:
        id_pedido_act = st.text_input("ID Pedido", value=str(datos_previos_pedido.get("Id_Pedido", "")), disabled=True)
        socio_act = st.text_input("👤 Miembro / Socio", value=str(datos_previos_pedido.get("Socio", "")), disabled=True)
        producto_act = st.text_input("📦 Artículo", value=str(datos_previos_pedido.get("Producto", "")), disabled=True)
        talla_act = st.text_input("📏 Talla", value=str(datos_previos_pedido.get("Talla", "Única")), disabled=True)
        
        # --- SOLUCIÓN AL VALUE_ERROR (BLINDAJE DE CANTIDAD) ---
        try:
            valor_cantidad_previo = datos_previos_pedido.get("Cantidad", 1)
            if pd.isna(valor_cantidad_previo) or str(valor_cantidad_previo).strip() == "":
                cantidad_defecto = 1
            else:
                cantidad_defecto = int(float(valor_cantidad_previo))
        except Exception:
            cantidad_defecto = 1
            
        cantidad_nueva = st.number_input("🔢 Modificar Cantidad", min_value=1, value=cantidad_defecto, step=1)
        
        estado_actual_str = str(datos_previos_pedido.get("Estado_Entrega", "Reservado / Pendiente"))
        idx_defecto_radio = 0 if "Entregado" in estado_actual_str else 1
        estado_nuevo = st.radio("🔄 Modificar Estado de Entrega:", ["Entregado", "Reservado / Pendiente"], index=idx_defecto_radio, horizontal=True)
        
        st.write("---")
        
        if st.button("💾 GUARDAR Y ACTUALIZAR CAMBIOS"):
            import requests
            import json
            import time
            
            # CORRECCIÓN: Agregamos la variable Cantidad al payload que se envía al servidor
            payload_update = {
                "accion": "editar_pedido_merch",
                "num_fila": fila_editar,
                "Cantidad": int(cantidad_nueva),
                "Estado_Entrega": estado_nuevo
            }
            URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
            with st.spinner("Sincronizando modificaciones con Google Sheets..."):
                try:
                    respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload_update), headers={"Content-Type": "application/json"})
                    if "OK" in respuesta.text or "éxito" in respuesta.text:
                        st.success("🎉 ¡Pedido modificado con éxito!")
                        time.sleep(1.5)
                        st.session_state.edit_pedido_data = None
                        st.session_state.current_menu = "MERCH_PEDIDOS"
                        st.rerun()
                    else:
                        st.error(f"Fallo del servidor de Google: {respuesta.text}")
                except Exception as err:
                    st.error(f"Error de conexión al actualizar el pedido: {err}")
                    
        if st.button("⬅️ CANCELAR Y VOLVER", key="btn_cancelar_edicion_ped"):
            st.session_state.edit_pedido_data = None
            st.session_state.current_menu = "MERCH_PEDIDOS"
            st.rerun()

# Marcadores de posición para el resto de pantallas (Normativa, Historia, etc.)

if st.session_state.current_menu in ["REUNIONES_MENU", "NORMATIVA_VER", "HISTORIA_VER"]:
    st.title(st.session_state.current_menu.replace("_", " "))
    st.info("Sección temporalmente en desarrollo...")
    if st.button("VOLVER"):
        st.session_state.current_menu = "OLD_RIDERS_MENU" if "MENU" not in st.session_state.current_menu else "CLUB_MENU"
        st.rerun()

