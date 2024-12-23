import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Title and description
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")
st.title("📊 HR Analytics Dashboard")
st.write("A dynamic dashboard showcasing key HR metrics and insights.")

# Sidebar
st.sidebar.header("Filter Data")

# Generate Demo Dataset
def create_demo_data():
    np.random.seed(42)
    departments = ["HR", "Sales", "IT", "Finance", "Marketing"]
    employees = [f"Employee {i}" for i in range(1, 101)]
    data = {
        "Employee Name": np.random.choice(employees, 100),
        "Department": np.random.choice(departments, 100),
        "Age": np.random.randint(22, 60, 100),
        "Salary": np.random.randint(30000, 120000, 100),
        "Satisfaction Score": np.random.uniform(1, 5, 100).round(1),
        "Years with Company": np.random.randint(1, 20, 100),
        "Performance Score": np.random.uniform(50, 100, 100).round(1),
        "Date of Joining": [datetime(2023, np.random.randint(1, 13), np.random.randint(1, 28)) for _ in range(100)]
    }
    return pd.DataFrame(data)

# Load data
df = create_demo_data()

# Filter by department
department_filter = st.sidebar.multiselect("Select Department(s):", options=df["Department"].unique(), default=df["Department"].unique())
filtered_df = df[df["Department"].isin(department_filter)]

# KPIs Section
st.header("Key Performance Indicators (KPIs)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_satisfaction = filtered_df["Satisfaction Score"].mean().round(2)
    st.metric(label="Average Satisfaction", value=f"{avg_satisfaction} / 5")

with col2:
    avg_salary = filtered_df["Salary"].mean().round(2)
    st.metric(label="Average Salary", value=f"${avg_salary:,.2f}")

with col3:
    avg_tenure = filtered_df["Years with Company"].mean().round(1)
    st.metric(label="Average Tenure", value=f"{avg_tenure} years")

with col4:
    avg_performance = filtered_df["Performance Score"].mean().round(1)
    st.metric(label="Average Performance", value=f"{avg_performance} / 100")

# Visualization Section
st.header("Visual Analytics")

# Satisfaction by Department
satisfaction_chart = px.bar(
    filtered_df.groupby("Department")["Satisfaction Score"].mean().reset_index(),
    x="Department",
    y="Satisfaction Score",
    color="Department",
    title="Average Satisfaction Score by Department",
    labels={"Satisfaction Score": "Avg Satisfaction Score"}
)
st.plotly_chart(satisfaction_chart, use_container_width=True)

# Salary Distribution
salary_chart = px.box(
    filtered_df,
    x="Department",
    y="Salary",
    color="Department",
    title="Salary Distribution by Department",
    points="all"
)
st.plotly_chart(salary_chart, use_container_width=True)

# Performance vs Tenure Scatter Plot
scatter_chart = px.scatter(
    filtered_df,
    x="Years with Company",
    y="Performance Score",
    size="Satisfaction Score",
    color="Department",
    title="Performance Score vs. Years with Company",
    labels={"Years with Company": "Years with Company", "Performance Score": "Performance Score"}
)
st.plotly_chart(scatter_chart, use_container_width=True)

# Projections (Interactive)
st.header("Projections")
projection_years = st.slider("Select Projection Years:", min_value=1, max_value=10, value=5)
projected_salaries = filtered_df.groupby("Department")["Salary"].mean() * (1 + 0.03 * projection_years)

projection_chart = go.Figure()
projection_chart.add_trace(go.Bar(
    x=projected_salaries.index,
    y=projected_salaries.values,
    name="Projected Salaries",
    marker_color="lightskyblue"
))
projection_chart.update_layout(
    title="Projected Average Salaries by Department",
    xaxis_title="Department",
    yaxis_title="Projected Average Salary",
    template="plotly_white"
)
st.plotly_chart(projection_chart, use_container_width=True)

# Download Filtered Data
st.sidebar.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_hr_data.csv",
    mime="text/csv"
)

st.write("---")
st.write("Built with ❤️ using Streamlit.")
