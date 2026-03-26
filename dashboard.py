import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 页面设置
st.set_page_config(page_title="销售数据看板", layout="wide")
st.title("📊 销售数据 Dashboard - Excel 实时版")

# 读取 Excel 底稿
@st.cache_data(ttl=60)  # 每60秒自动刷新
def load_data():
    excel_path = "sales_data.xlsx"
    if not os.path.exists(excel_path):
        return None
    df = pd.read_excel(excel_path)
    return df

df = load_data()

if df is None:
    st.error("❌ 未找到 Excel 文件：c:/Python_Excel/sales_data.xlsx")
    st.info("请先在 Jupyter 里运行创建 Excel 的代码")
else:
    # 计算关键指标
    total_sales = df["销售额"].sum()
    total_orders = df["销售数量"].sum()
    avg_price = total_sales // total_orders if total_orders > 0 else 0

    # 指标卡片
    col1, col2, col3 = st.columns(3)
    col1.metric("总销售额", f"¥{total_sales:,}")
    col2.metric("总订单数", f"{total_orders}")
    col3.metric("平均单价", f"¥{avg_price}")

    st.divider()

    # 图表
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 各产品销售额")
        if "产品" in df.columns:
            product_sales = df.groupby("产品")["销售额"].sum().reset_index()
            fig1 = px.bar(product_sales, x="产品", y="销售额", color="产品")
            st.plotly_chart(fig1, use_container_width=True)

    
    with col_right:
        st.subheader("👤 销售员业绩")
        if "销售员" in df.columns:
            person_sales = df.groupby("销售员")["销售额"].sum().reset_index()
            fig2 = px.pie(person_sales, values="销售额", names="销售员")
            st.plotly_chart(fig2, use_container_width=True)

    # 数据表格
    st.subheader("📋 详细数据")
    st.dataframe(df, use_container_width=True)

    st.caption("💡 提示：修改 Excel 后，按 F5 刷新页面即可看到最新数据")
