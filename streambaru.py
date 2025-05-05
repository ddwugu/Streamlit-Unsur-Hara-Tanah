import pickle
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

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
    with open('Pred_RF_Baru.sav', 'rb') as file:
        kesuburan = pickle.load(file)
except Exception as e:
    st.error(f"⚠️ Error loading the model: {e}")
    kesuburan = None

# ===================== UI APLIKASI =====================

# Web Title dengan Emoji & Warna
st.markdown("<h1 style='text-align: center; color: white;'>🌱 PREDICTION OF SOIL NUTRIENTS, METALS, AND pH ⚡</h1>", unsafe_allow_html=True)

# **Tambahkan Tanggal & Waktu**
current_time = datetime.datetime.now().strftime("%A, %d %B %Y - %H:%M:%S")
st.markdown(f"<h4 style='text-align: center; color: white;'>🕒 {current_time}</h4>", unsafe_allow_html=True)

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
            column_names = ["Mg(%)", "Al(%)", "Si(%)", "Fe(%)", "S(%)", "Cl(%)", "K(%)", "Ca(%)", "Ti(%)", "Zn(%)","Zr(%)","Ni(%)", "Ga(%)", "Mn(%)","Cr(%)", "Rh(%)", "Ta(%)", "V(%)", "C(%)", "N(%)", "pH"]
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

            # ===================== RADAR CHART =====================

            st.markdown("### 🕸 **Radar Chart of Soil Nutrients**")

            # Ambil nilai prediksi untuk radar chart
            values = prediksi_unsur_hara[0]
            categories = column_names

            # Pastikan radar chart menutup lingkaran
            values = np.append(values, values[0])
            categories.append(categories[0])

            # Buat sudut untuk tiap sumbu di radar chart
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()

            # Inisialisasi Radar Chart
            fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

            # Plot garis & area radar chart
            ax.fill(angles, values, color="cyan", alpha=0.3)
            ax.plot(angles, values, color="blue", linewidth=2)

            # Set label kategori
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories[:-1], fontsize=10)

            # Styling
            ax.set_yticklabels([])
            ax.set_title("Soil Nutrient Composition", fontsize=14, fontweight="bold")

            # Tampilkan radar chart
            st.pyplot(fig)

            # Kesimpulan hasil prediksi
            st.success("✅ Prediction successful! Check the charts above for details.")

    except Exception as e:
        st.error(f"❌ Error predicting soil nutrients: {e}")
