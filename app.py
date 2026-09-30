import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="My Excel Dashboard", layout="wide")
st.title("📊 Interactive Excel Data Dashboard")

# 1. File Uploader Widget
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # 2. Read Excel Data into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Show raw data preview toggler
    if st.checkbox("Show raw Excel data preview"):
        st.dataframe(df)
    
    # 3. Dynamic Sidebar Filters
    st.sidebar.header("Filter Options")
    # Dynamically find columns to use as filters (assumes categorical data exists)
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if categorical_cols:
        selected_col = st.sidebar.selectbox("Select Column to Filter By", categorical_cols)
        unique_values = df[selected_col].unique()
        selected_val = st.sidebar.multiselect(f"Select values from {selected_col}", unique_values, default=unique_values)
        
        # Filter the dataframe
        df_filtered = df[df[selected_col].isin(selected_val)]
    else:
        df_filtered = df

    # 4. Create Visual Charts
    numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) >= 1 and categorical_cols:
        st.subheader("📈 Visual Data Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar Chart
            fig_bar = px.bar(df_filtered, x=categorical_cols[0], y=numeric_cols[0], title=f"{numeric_cols[0]} by {categorical_cols[0]}")
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col2:
            # Line or Scatter Chart
            fig_line = px.line(df_filtered, y=numeric_cols[0], title=f"{numeric_cols[0]} Trend")
            st.plotly_chart(fig_line, use_container_width=True)
            
    else:
        st.warning("Please ensure your Excel sheet contains at least one text column and one numeric column for charting.")
else:
    st.info("💡 Please upload an Excel file above to generate the visual charts.")
