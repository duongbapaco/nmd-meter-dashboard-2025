import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard công tơ NMĐ", layout="wide")

st.title("📊 Dashboard công tơ NMĐ")

# Upload Excel
excel_file = st.file_uploader("📂 Tải lên file Excel danh sách công tơ", type=["xlsx", "xlsm"])
if excel_file:
    df_meters = pd.read_excel(excel_file)
    st.subheader("📌 Danh sách công tơ")
    st.dataframe(df_meters)

# Upload ảnh công tơ
uploaded_images = st.file_uploader("📷 Tải ảnh công tơ", type=["jpg", "png"], accept_multiple_files=True)

results = []
if uploaded_images:
    for img_file in uploaded_images:
        img = Image.open(img_file)
        text = pytesseract.image_to_string(img, config="--psm 7 digits")
        
        try:
            value = float("".join([c for c in text if c.isdigit() or c=="."]))
        except:
            value = None

        results.append({"Ảnh": img_file.name, "Giá trị đo": value})

    df_readings = pd.DataFrame(results)
    st.subheader("📊 Kết quả OCR")
    st.dataframe(df_readings)

    if excel_file:
        # Merge theo số thứ tự (đơn giản: ghép lần lượt)
        df = df_meters.copy()
        df["Giá trị đo"] = df_readings["Giá trị đo"]
        df["ΔNước"] = df["Giá trị đo"].diff()
        if "Lượng khí" in df.columns:
            df["Định mức (tấn/h)"] = df["ΔNước"] / df["Lượng khí"]

            # Cảnh báo màu: đỏ nếu >1.15, xanh nếu <=1.15
            def color_threshold(val):
                if pd.isna(val):
                    return ""
                color = "red" if val > 1.15 else "green"
                return f"color: {color}; font-weight: bold;"

            st.subheader("📈 Bảng định mức (có cảnh báo)")
            st.dataframe(df.style.applymap(color_threshold, subset=["Định mức (tấn/h)"]))

        if "Định mức (tấn/h)" in df.columns:
            fig, ax = plt.subplots()
            df.plot(y="Định mức (tấn/h)", marker="o", ax=ax, color="blue")
            ax.axhline(1.15, color="red", linestyle="--", label="Ngưỡng 1.15")
            ax.legend()
            st.pyplot(fig)
