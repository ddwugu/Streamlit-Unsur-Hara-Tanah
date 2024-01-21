import pickle
import streamlit as st
import pandas as pd



# Load the model
try:
    with open('Pred_Kesuburan.sav', 'rb') as file:
        kesuburan = pickle.load(file)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    kesuburan = None  # Assign None if there is an error loading the model

# Web Title
st.title('PREDIKSI UNSUR HARA, UNSUR LOGAM, DAN PH TANAH')

# User Inputs
Impedance = st.text_input('Input Nilai Impedansi Tanah (Ω)')

# Code prediction
prediksi_nilai = ''

# Prediction Button
if kesuburan is not None and st.button('Prediksi Unsur Hara'):
    try:
        prediksi_unsur_hara = kesuburan.predict([[float(Impedance)]])

        # Convert the predicted values to a DataFrame
        column_names = ["Mg(%)", "Al(%)", "Si(%)", "Fe(%)", "S(%)", "Cl(%)", "K(%)", "Ca(%)", "Ti(%)", "Zn(%)", "Zr(%)", "Ni(%)", "Ga(%)", "Ta(%)", "V(%)", "Cr(%)", "Mn(%)", "c(%)", "p(%)", "N(%)", "pH(%)"]
        df_prediksi = pd.DataFrame(prediksi_unsur_hara, columns=column_names)

        # Concatenate the input value with the predicted DataFrame
        result_df = pd.concat([pd.DataFrame({'Impedance(Ω)': [Impedance]}), df_prediksi], axis=1)

        # Display the concatenated DataFrame
        st.write(result_df)

        # Plotting the bar chart
        st.bar_chart(result_df.set_index('Impedance(Ω)'))

    except Exception as e:
        st.error(f"Error predicting location: {e}")
