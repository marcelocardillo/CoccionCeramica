Para permitir que los usuarios ingresen la hora en formato AM o PM en lugar de la cantidad de horas, puedes utilizar un control de entrada de texto para la hora y luego convertir esa entrada en un valor numérico. Aquí tienes el código modificado:

```python
import streamlit as st
import pandas as pd
import altair as alt

# Título de la aplicación
st.title('Gráfico de Temperatura de Cocción')

# Sidebar con controles de entrada
st.sidebar.header('Configuración de Datos')

# Campo de entrada de hora en formato AM/PM
hora_texto = st.sidebar.text_input('Hora de Cocción (ejemplo: 2:30 PM):')

# Función para convertir la hora en formato AM/PM a decimal
def convertir_hora_am_pm_a_decimal(hora_texto):
    try:
        hora_obj = pd.to_datetime(hora_texto, format='%I:%M %p')
        hora_decimal = hora_obj.hour + hora_obj.minute / 60
        return hora_decimal
    except:
        return None

hora_decimal = convertir_hora_am_pm_a_decimal(hora_texto)

temperatura = st.sidebar.number_input('Temperatura de Cocción (en °C):', 0, 1500, 100)

# Botón para agregar datos
if st.sidebar.button('Agregar Datos'):
    if hora_decimal is not None:
        data = {'Hora': [hora_decimal], 'Temperatura': [temperatura]}
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
        x='Hora:Q',  # Cambio en el eje X
        y='Temperatura:Q'
    ).properties(height=500, width=500)
    st.altair_chart(chart)

    # Calcular la media de temperatura a partir de la segunda medición
    if len(st.session_state.data) > 1:
        mean_temperature = st.session_state.data['Temperatura'].mean()
        st.write(f'Media de Temperatura a partir de la segunda medición: {mean_temperature:.3f} °C')

    # Calcular el tiempo total de cocción en horas
    total_cooking_time = st.session_state.data['Hora'].max() - st.session_state.data['Hora'].min()
    st.write(f'Tiempo Total de Cocción en Horas: {total_cooking_time:.3f} horas')
```

Con este código, los usuarios pueden ingresar la hora en formato AM/PM (por ejemplo, "2:30 PM"), y la aplicación la convertirá internamente a un valor decimal para su procesamiento.
