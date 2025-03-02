import pickle
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===================== CONFIGURASI APLIKASI =====================

# Custom CSS untuk background dan styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: white;
        }
        .stApp {
            background: linear-gradient(to right, #4facfe, #00f2fe);
        }
        .stMarkdown {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ===================== LOAD MODEL =====================

try:
    with open('Pred_RF1_Impedansi.sav', 'rb') as file:
        kesuburan = pickle.load(file)
except Exception as e:
    st.error(f"⚠️ Error loading the model: {e}")
    kesuburan = None  # Assign None if there is an error loading the model

# ===================== UI APLIKASI =====================

# Web Title dengan Emoji & Warna
st.markdown("<h1 style='text-align: center; color: white;'>🌱 PREDICTION OF SOIL NUTRIENTS, METALS, AND pH ⚡</h1>", unsafe_allow_html=True)

# Deskripsi Singkat
st.markdown("""
    **👋 Welcome to the Soil Nutrient Prediction App!**  
    This tool predicts the **nutrient content, metal concentration, and pH** of soil based on its **impedance value (Ω)**.  
    Simply enter the impedance value below and hit the **"Predict Soil Nutrients"** button! 🚀
""")

# ===================== INPUT USER =====================

# Input Form
Impedance = st.text_input('🔍 Enter Soil Impedance Value (Ω)', '')

# ===================== PREDIKSI =====================

if kesuburan is not None and st.button('⚡ Predict Soil Nutrients'):
    try:
        # Pastikan nilai Impedance valid
        if Impedance.strip() == "":
            st.warning("⚠️ Please enter a valid Impedance value!")
        else:
            prediksi_unsur_hara = kesuburan.predict([[float(Impedance)]])

            # Convert hasil prediksi ke DataFrame
            column_names = ["Mg(%)", "Al(%)", "Si(%)", "Fe(%)", "S(%)", "Cl(%)", "K(%)", "Ca(%)", "Zn(%)", "Mn(%)", "C(%)", "N(%)", "pH"]
            df_prediksi = pd.DataFrame(prediksi_unsur_hara, columns=column_names)

            # Gabungkan dengan nilai Impedance yang dimasukkan user
            result_df = pd.concat([pd.DataFrame({'Impedance(Ω)': [float(Impedance)]}), df_prediksi], axis=1)

            # Tampilkan hasil dengan expander
            with st.expander("📊 **View Prediction Data**", expanded=True):
                st.write(result_df)

            # ===================== VISUALISASI =====================

            # Bar Chart
            st.markdown("### 📊 **Bar Chart of Soil Nutrients**")
            st.bar_chart(result_df.set_index('Impedance(Ω)'))

            # Line Chart
            st.markdown("### 📈 **Line Chart of Soil Nutrients**")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(column_names, prediksi_unsur_hara[0], marker='o', linestyle='-', color='cyan', linewidth=2)
            ax.set_xlabel("Nutrient Type")
            ax.set_ylabel("Predicted Value (%)")
            ax.set_title("Soil Nutrient Prediction")
            ax.grid(True)
            st.pyplot(fig)

            # Kesimpulan hasil prediksi
            st.success("✅ Prediction successful! Check the charts above for details.")

    except Exception as e:
        st.error(f"❌ Error predicting soil nutrients: {e}")
