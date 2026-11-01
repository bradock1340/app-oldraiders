# ==============================================================================
# === 5. ZONA DE MERCHANDISING (MÓDULO INDEPENDIENTE PARA EVITAR ERRORES) ======
# ==============================================================================

# Cambiamos el primer 'elif' por un 'if' para aislarlo de los problemas de arriba
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
    
    # Botones inferiores de navegación en dos columnas (Volver / Salir)
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

# === 5.1 SUBPANTALLA: CONSULTAR PRODUCTOS (CON SISTEMA DE ELIMINACIÓN) ===
elif st.session_state.current_menu == "MERCH_CONSULTAR":
    st.title("📦 INVENTARIO DE PRODUCTOS")
    st.write("Consulta y gestiona el stock disponible del material oficial del club.")
    st.write("---")
    try:
        # 1. Leer los datos de la pestaña Merchandising en tiempo real
        df_merch = pd.read_csv(URL_MERCHANDISING)
        df_merch.columns = df_merch.columns.str.strip()
        
        if not df_merch.empty:
            # Buscador rápido por nombre de producto
            busqueda_prod = st.text_input("🔍 Buscar Producto por nombre...").strip().lower()
            df_filtrado_merch = df_merch.copy()
            if busqueda_prod:
                df_filtrado_merch = df_filtrado_merch[df_filtrado_merch['Producto'].astype(str).str.lower().str.contains(busqueda_prod)]
            
            st.write("---")
            
            # Listamos cada producto de forma individual con su botón de acción
            for index, row in df_filtrado_merch.iterrows():
                # Calculamos la línea exacta en el Sheets (+2 por cabecera y desfase)
                num_fila_producto = int(index) + 2
                
                with st.container():
                    col_info, col_accion = st.columns([3, 1])
                    
                    with col_info:
                        st.markdown(f"📦 **[{row['Id_Producto']}] {row['Producto']}** — **Precio:** {row['Precio']}€")
                        st.caption(f"🏬 Proveedor: {row['Proveedor']} ({row['Tel_Proveedor']}) | 📊 Stock Actual: {row['Stock']} u.")
                        if pd.notna(row['Descripcion']) and str(row['Descripcion']).strip() != "":
                            st.info(f"📝 *{row['Descripcion']}*")
                            
                    with col_accion:
                        # Botón rojo para eliminar el artículo con confirmación de seguridad
                        if st.button("❌ ELIMINAR", key=f"btn_eliminar_prod_{index}"):
                            import requests
                            import json
                            import time
                            
                            payload = {
                                "accion": "eliminar_producto_merch",
                                "num_fila": num_fila_producto
                            }
                            
                            URL_PROCESADOR_GOOGLE = "https://script.google.com/macros/s/AKfycbxq6-u0mVzhsxpSxSI4XVZMcozObFbJemJvYtzMehlTw0PUaK6vIV4Ek5vHn0xbHvFb/exec"
                            
                            with st.spinner("Borrando producto del inventario general..."):
                                try:
                                    respuesta = requests.post(URL_PROCESADOR_GOOGLE, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                                    if "OK" in respuesta.text or "éxito" in respuesta.text:
                                        st.success(f"🗑️ '{row['Producto']}' eliminado del inventario.")
                                        time.sleep(1.0)
                                        st.rerun()
                                    else:
                                        st.error(f"Fallo del servidor de Google: {respuesta.text}")
                                except Exception as err:
                                    st.error(f"Error de conexión: {err}")
                st.write("---") # Separador entre artículos
        else:
            st.info("No hay productos registrados en el inventario todavía.")
            
    except Exception as e:
        st.error(f"Error de lectura en la hoja Merchandising: {e}")
        
    if st.button("🔙 VOLVER", key="btn_volver_consultar"):
        st.session_state.current_menu = "PANTALLA_MERCHANDISING"
        st.rerun()

# === 5.2 SUBPANTALLA: NUEVO PRODUCTO ===
elif st.session_state.current_menu == "MERCH_NUEVO_PRODUCTO":
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
                    # S'envia a la URL global que hem centralitzat dalt del tot
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
        st.session_state.current_menu = "MERCHANDISING"
        st.rerun()


# === 5.3 SUBPANTALLA: NUEVO PEDIDO ===
elif st.session_state.current_menu == "MERCH_NUEVO_PEDIDO":
    st.title("🛒 REGISTRAR NUEVO PEDIDO")
    st.write("Selecciona el producto y define la talla para este pedido específico.")
    st.write("---")
    
    try:
        df_merch = pd.read_csv(URL_MERCHANDISING)
        df_merch.columns = df_merch.columns.str.strip()
        lista_productos = ["-- Seleccionar Artículo --"] + (df_merch['Producto'].dropna().unique().tolist() if not df_merch.empty else [])
        
        socios_disponibles = ["-- Seleccionar Socio --", "General"]
        try:
            df_usuarios_ped = pd.read_csv(URL_USUARIOS)
            df_usuarios_ped.columns = df_usuarios_ped.columns.str.strip()
            
            if 'Alias' in df_usuarios_ped.columns:
                lista_alias = df_usuarios_ped['Alias'].dropna().unique().tolist()
                socios_disponibles += [str(a) for a in lista_alias if str(a) != "General"]
        except Exception as e_users:
            st.error(f"Error al cargar la lista de miembros (Alias): {e_users}")
            
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
            
            if st.button("🛒 ENCARGAR Y GUARDAR PEDIDO"):
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
                                st.success(f"🎉 Pedido de {socio_pedido} guardado con éxito en la pestaña 'Pedidos'.")
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
        
    if st.button("🔙 VOLVER", key="btn_volver_pedido_final"):
        st.session_state.current_menu = "PANTALLA_MERCHANDISING"
        st.rerun()
 
# Marcadores de posición para el resto de pantallas (Normativa, Historia, etc.)
    elif st.session_state.current_menu in ["REUNIONES_MENU", "NORMATIVA_VER", "HISTORIA_VER"]:
        st.title(st.session_state.current_menu.replace("_", " "))
        st.info("Sección temporalmente en desarrollo...")
        if st.button("VOLVER"):
            st.session_state.current_menu = "OLD_RIDERS_MENU" if "MENU" not in st.session_state.current_menu else "CLUB_MENU"
            st.rerun()

