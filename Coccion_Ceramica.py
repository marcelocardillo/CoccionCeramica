import streamlit as st
import pandas as pd
import altair as alt
from collections import namedtuple

# Título de la aplicación
st.title('Gráfico de Temperatura de Cocción')

# Sidebar con controles de entrada
st.sidebar.header('Configuración de Datos')
hora_inicio = st.sidebar.text_input('Hora de inicio de Cocción (ejemplo: 14.40):')
hora_fin = st.sidebar.text_input('Hora de fin de Cocción (ejemplo: 16.15):')

# Convertir la hora ingresada en formato decimal
def convertir_hora_decimal(hora_texto):
    try:
        horas, minutos = map(float, hora_texto.split('.'))
        return horas + minutos / 60
    except:
        return None

hora_inicio_decimal = convertir_hora_decimal(hora_inicio)
hora_fin_decimal = convertir_hora_decimal(hora_fin)

temperatura = st.sidebar.number_input('Temperatura de Cocción (en °C):', 0, 1500, 100)

# Botón para agregar datos
if st.sidebar.button('Agregar Datos'):
    if hora_inicio_decimal is not None and hora_fin_decimal is not None:
        data = {'Hora Inicio': [hora_inicio_decimal], 'Hora Fin': [hora_fin_decimal], 'Temperatura': [temperatura]}
        df = pd.DataFrame(data)

        # Si es la primera vez que se agrega un dato, creamos el DataFrame
        if 'data' not in st.session_state:
            st.session_state.data = df
        else:
            # Si ya existe el DataFrame, lo actualizamos agregando los nuevos datos
            st.session_state.data = pd.concat([st.session_state.data, df], ignore_index=True)

# Gráfico de línea con los datos ingresados
if 'data' in st.session_state:
    st.header('Gráfico de Temperatura de Cocción')
    chart = alt.Chart(st.session_state.data).mark_line(color='#0068c9').encode(
        x='Hora Inicio:Q',
        y='Temperatura:Q'
    ).properties(height=500, width=500)
    st.altair_chart(chart)

    # Calcular la media de temperatura a partir de la segunda medición
    if len(st.session_state.data) > 1:
        mean_temperature = st.session_state.data['Temperatura'].mean()
        st.write(f'Media de Temperatura a partir de la segunda medición: {mean_temperature:.3f} °C')

    # Calcular el tiempo total de cocción en horas
    total_cooking_time = st.session_state.data['Hora Fin'].max() - st.session_state.data['Hora Inicio'].min()
    st.write(f'Tiempo Total de Cocción en Horas: {total_cooking_time:.3f} horas')
