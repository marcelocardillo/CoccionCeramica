import streamlit as st
import pandas as pd
import altair as alt
from collections import namedtuple
import math

# Título de la aplicación
st.title('Gráfico de Temperatura de Cocción')

# Sidebar con controles de entrada
st.sidebar.header('Configuración de Datos')
hora = st.sidebar.number_input('Hora de Cocción (en horas):', 0.0, 24.0, 0.0, step=0.5)
temperatura = st.sidebar.number_input('Temperatura de Cocción (en °C):', 0, 300, 100)

# Botón para agregar datos
if st.sidebar.button('Agregar Datos'):
    data = {'Hora': [hora], 'Temperatura': [temperatura]}
    df = pd.DataFrame(data)

    # Si es la primera vez que se agrega un dato, creamos el DataFrame
    if 'data' not in st.session_state:
        st.session_state.data = df
    else:
        # Si ya existe el DataFrame, lo actualizamos agregando los nuevos datos
        st.session_state.data = pd.concat([st.session_state.data, df], ignore_index=True)

# Gráfico de dispersión con los datos ingresados
if 'data' in st.session_state:
    st.header('Gráfico de Temperatura de Cocción')
    chart = alt.Chart(st.session_state.data).mark_circle(color='#0068c9', opacity=0.5).encode(
        x='Hora:Q',
        y='Temperatura:Q'
    ).properties(height=500, width=500)
    st.altair_chart(chart)
