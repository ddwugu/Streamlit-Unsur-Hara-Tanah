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
    with open('Pred_Kesuburan.sav', 'rb') as file:
        kesuburan = pickle.load(file)
except Exception as e:
    st.error(f"⚠️ Error loading the model: {e}")
    kesuburan = None  # Assign None if there is an error loading the model

# ===================== UI APLIKASI =====================

# Web Title dengan Emoji & Warna
st.markdown("<h1 style='text-align: center; color: white;'>🌱 PREDICTION OF SOIL NUTRIENTS, METALS, AND pH FOR ULTISOL SOIL ⚡</h1>", unsafe_allow_html=True)

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
            column_names = ["Mg(%)", "Al(%)", "Si(%)", "Fe(%)", "S(%)", "Cl(%)", "K(%)", "Ca(%)", "Ti(%)", "Zn(%)", 
                            "Zr(%)", "Ni(%)", "Ga(%)", "Ta(%)", "V(%)", "Cr(%)", "Mn(%)", "C(%)", "P(%)", "N(%)", "pH(%)"]
            df_prediksi = pd.DataFrame(prediksi_unsur_hara, columns=column_names)

            # Gabungkan dengan nilai Impedance yang dimasukkan user
            result_df = pd.concat([pd.DataFrame({'Impedance(Ω)': [float(Impedance)]}), df_prediksi], axis=1)

            # Tampilkan hasil dengan expander
            with st.expander("📊 **View Prediction Data**", expanded=True):
                st.write(result_df)

            # ===================== VISUALISASI =====================

            # Bar Chart dengan Label Rotasi
            st.markdown("### 📊 **Bar Chart of Soil Nutrients**")
            fig, ax = plt.subplots(figsize=(10, 6))  # Lebih lebar agar tidak bertumpuk
            df_prediksi.T.plot(kind="bar", legend=False, ax=ax, color='skyblue')

            ax.set_xticklabels(column_names, rotation=45, ha='right', fontsize=10)  # Rotasi label
            ax.set_xlabel("Nutrient Type", fontsize=12)
            ax.set_ylabel("Predicted Value (%)", fontsize=12)
            ax.set_title("Soil Nutrient Prediction - Bar Chart", fontsize=14, fontweight="bold")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig)

            # Line Chart dengan Label Rotasi
            st.markdown("### 📈 **Line Chart of Soil Nutrients**")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(column_names, prediksi_unsur_hara[0], marker='o', linestyle='-', color='cyan', linewidth=2)

            ax.set_xticks(range(len(column_names)))  # Set posisi label
            ax.set_xticklabels(column_names, rotation=45, ha='right', fontsize=10)  # Rotasi label

            ax.set_xlabel("Nutrient Type", fontsize=12)
            ax.set_ylabel("Predicted Value (%)", fontsize=12)
            ax.set_title("Soil Nutrient Prediction - Line Chart", fontsize=14, fontweight="bold")
            ax.grid(True, linestyle='--', alpha=0.7)

            st.pyplot(fig)

            # Kesimpulan hasil prediksi
            st.success("✅ Prediction successful! Check the charts above for details.")

    except Exception as e:
        st.error(f"❌ Error predicting soil nutrients: {e}")
