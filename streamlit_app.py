    if st.button("ENTRAR"):
        # Sistema de reintentos automáticos para evitar el error de conexión
        df_usuarios = None
        for intento in range(3): # Lo intenta hasta 3 veces seguidas de forma interna
            try:
                df_usuarios = pd.read_csv(URL_USUARIOS)
                break # Si conecta con éxito, rompe el bucle y continúa
            except:
                import time
                time.sleep(0.2) # Espera un parpadeo antes de volver a intentar
        
        if df_usuarios is not None:
            try:
                # Limpiamos nombres de columnas
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
                        st.session_state.user_role = usuario_valido.iloc[0]['Rol']
                        st.session_state.user_alias = usuario_valido.iloc[0]['Alias']
                        st.rerun()
                    else:
                        st.error("Contraseña incorrecta")
                else:
                    st.error("El usuario no está registrado en el Moto Club")
            except Exception as e:
                st.error("Error al procesar los datos de usuario. Revisa las columnas del Sheets.")
        else:
            st.error("Google Sheets está tardando en responder. Por favor, vuelve a pulsar ENTRAR.")

