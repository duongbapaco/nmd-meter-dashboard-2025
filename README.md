# 📊 Dashboard công tơ NMĐ

Ứng dụng Streamlit để:
- Đọc danh sách công tơ từ Excel
- Tách dữ liệu từ ảnh công tơ (OCR với Tesseract)
- Tính định mức theo công thức:  
  **(Nước ngày sau - Nước ngày trước) / Lượng khí = Định mức (tấn/h)**
- Hiển thị báo cáo + biểu đồ

## 🚀 Deploy trên Streamlit Cloud
1. Upload toàn bộ thư mục này lên GitHub
2. Vào [Streamlit Cloud](https://share.streamlit.io)
3. Chọn repo → chọn file `app.py`
4. Bấm Deploy ✅

## 🖥️ Chạy local
```bash
pip install -r requirements.txt
streamlit run app.py
```
