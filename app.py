import streamlit as st
import pandas as pd
from io import BytesIO

# 設定網頁配置
st.set_page_config(page_title="客戶資料管理中心", layout="wide")

st.title("📂 客戶資料匯入與管理系統")

# --- 初始化資料 ---
if 'customer_data' not in st.session_state:
    # 建立一個初始的空表格
    st.session_state.customer_data = pd.DataFrame(columns=["客戶名稱", "聯絡電話", "電子郵件", "備註"])

# --- 側邊欄：功能選單 ---
st.sidebar.header("功能面板")

# 1. 匯入功能
uploaded_file = st.sidebar.file_uploader("匯入現有的 Excel 檔案", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 讀取上傳的 Excel
        imported_df = pd.read_excel(uploaded_file)
        # 確保欄位名稱一致（可根據需求調整）
        st.session_state.customer_data = imported_df
        st.sidebar.success("檔案匯入成功！")
    except Exception as e:
        st.sidebar.error(f"匯入失敗: {e}")

# 2. 手動新增功能
st.sidebar.markdown("---")
st.sidebar.subheader("手動新增資料")
with st.sidebar.form(key='add_form', clear_on_submit=True):
    name = st.text_input("客戶名稱")
    phone = st.text_input("聯絡電話")
    email = st.text_input("電子郵件")
    note = st.text_area("備註")
    submit = st.form_submit_button("新增至下方列表")

if submit and name:
    new_row = pd.DataFrame([[name, phone, email, note]], columns=st.session_state.customer_data.columns)
    st.session_state.customer_data = pd.concat([st.session_state.customer_data, new_row], ignore_index=True)

# --- 主畫面：HTML 表格顯示 ---
st.subheader("📊 客戶資料預覽 (HTML 頁面)")

if not st.session_state.customer_data.empty:
    # 使用 st.data_editor 讓網頁上的表格可以直接點擊修改
    edited_df = st.data_editor(st.session_state.customer_data, use_container_width=True, num_rows="dynamic")
    
    # 同步修改後的資料
    st.session_state.customer_data = edited_df

    # --- 匯出功能 ---
    st.markdown("---")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.customer_data.to_excel(writer, index=False)
    
    st.download_button(
        label="💾 下載更新後的 Excel 檔案",
        data=output.getvalue(),
        file_name="updated_customers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("目前尚無資料，請由左側匯入 Excel 或手動新增。")
