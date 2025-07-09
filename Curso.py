#python -m streamlit run Curso.py   
import streamlit as st

# Configuración de la página
st.set_page_config(layout="wide")

# Crear las pestañas
Tab1, Tab2 = st.tabs(["Tab1", "Tab2"])

# Usar st.session_state para rastrear la pestaña activa
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Tab1"

# Actualizar la pestaña activa cuando el usuario cambia de pestaña
def update_active_tab():
    st.session_state.active_tab = st.query_params.get("tab", "Tab1")

# Llamar a la función para actualizar la pestaña activa
update_active_tab()

# Mostrar el sidebar solo en la pestaña 1
if st.session_state.active_tab == "Tab1":
    with st.sidebar:
        st.write("### Sidebar de Tab 1")
        wind_speed = st.text_input("Wind speed (m/s)", value="5", key="tab1_wind_speed")
        kite_area = st.text_input("Kite area (m^2)", value="7", key="tab1_kite_area")
        scale_factor = st.text_input("Gearbox Ratio", value="4.26", key="tab1_scale_factor")

# Ocultar el sidebar en la pestaña 2 usando CSS
if st.session_state.active_tab == "Tab2":
    hide_sidebar_css = """
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """
    st.markdown(hide_sidebar_css, unsafe_allow_html=True)

# Pestaña 1
with Tab1:
    st.header("This is Tab 1")
    st.write("Welcome to Tab 1!")
    st.write(f"Wind speed: {wind_speed}")
    st.write(f"Kite area: {kite_area}")
    st.write(f"Scale factor: {scale_factor}")

# Pestaña 2
with Tab2:
    st.header("This is Tab 2")
    st.write("Welcome to Tab 2!")
    number = st.slider("Pick a number in Tab 2", 0, 100, key="tab2_slider")
    st.write(f"You selected: {number}")