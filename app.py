import datetime
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_bokeh
import plotly.express as px
import streamlit as st
from bokeh.plotting import figure

import config
import costs

st.sidebar.header("Global Parameters")
today = datetime.date.today()


def input_features():
    startup_funds = st.sidebar.number_input("Startup Funds [$]", 379835.00)
    nsf_grants_funds = st.sidebar.number_input("NSF Grant Funds [$]", 334786.00)
    funds = startup_funds + nsf_grants_funds
    start = st.sidebar.text_input("Start Date", "2021-12")
    start = pd.to_datetime(start)
    end = st.sidebar.text_input("End Date", "2027-01")
    end = pd.to_datetime(end)
    return funds, start, end


funds, start, end = input_features()

st.sidebar.header("Student 1")


def input_student1():
    department1 = st.sidebar.selectbox(
        "Student Department", ["ece", "cs", "phys"], index=0, key="department1"
    )
    start1 = st.sidebar.text_input("Student Start Date", "2022-09")
    start1 = pd.to_datetime(start1)
    end1 = st.sidebar.text_input("Student End Date", "2026-08")
    end1 = pd.to_datetime(end1)

    instate_start1 = st.sidebar.text_input("Student Instate", "2022-09")
    instate_start1 = pd.to_datetime(instate_start1)

    candidacy1 = st.sidebar.number_input(
        "Candidacy Year",
        value=config.salary_per_department[department1]["candidacy year"],
    )
    overhead_str1 = st.sidebar.selectbox(
        "Overhead", ["yes (contract grant)", "no (startup funds)"], index=0, key="grant"
    )
    overhead1 = overhead_str1 == "yes (contract grant)"
    print(overhead1)
    return start1, end1, department1, instate_start1, candidacy1, overhead1


start1, end1, department1, instate_start1, candidacy1, overhead1 = input_student1()
start, end = min(start, start1), max(end, end1)

daterange1 = pd.date_range(start=start1, end=end1, freq="M")
costs1 = costs.student(
    daterange1, department1, instate_start1, overhead1, candidacy_year=candidacy1
)
costs1 = costs.over_date_range(start, end, start1, end1, costs1)

st.sidebar.header("SRA")


def input_sra():
    start_sra = st.sidebar.text_input("SRA Start Date", "2021-12")
    end_sra = st.sidebar.text_input("SRA End Date", "2022-05")
    return pd.to_datetime(start_sra), pd.to_datetime(end_sra)


start_sra, end_sra = input_sra()
start, end = min(start, start_sra), max(end, end_sra)
costs_sra = costs.sra(pd.date_range(start=start_sra, end=end_sra, freq="M"))
costs_sra = costs.over_date_range(start, end, start_sra, end_sra, costs_sra)

daterange = pd.date_range(start=start, end=end, freq="M")

budget_dict = {
    "date": daterange.date,
    "Student1": costs1,
    "Sra": costs_sra,
    "Rest": [funds] * len(daterange) - np.cumsum(costs1) - np.cumsum(costs_sra),
}
color_dict = {
    "Student1": "pink",
    "Sra": "orange",
    "Rest": "green",
}


budget_df = pd.DataFrame(budget_dict, index=daterange.date)


st.header("Budget [$]")
# st.line_chart(budget_df)

# fig = px.line(budget_df, x="date", y="Rest", color="green")
fig = px.line(
    budget_df, x="date", y=budget_df.columns[1:], color_discrete_map=color_dict
)

st.plotly_chart(fig, use_container_width=True)

# fig, ax = plt.subplots()
# #budget_df.plot_bokeh()
# p = figure(
#      title='simple line example',
#      x_axis_label='x',
#      y_axis_label='y')

# p.line(budget_df.index, budget_df.Rest, legend_label='Trend', line_width=2)

# st.bokeh_chart(p, use_container_width=True)
# ax.tick_params(axis='x', labelrotation=45)
# for one_year in np.unique(daterange.year):
#     ax.axvline(x=f"{one_year}-01", ls="--", color="grey")

# st.pyplot(fig)

# Configuration
st.header("Configuration")


df_gship_tuition = pd.DataFrame(config.gship_tuition, index=["$/month"]).style.format(
    "{:.2f}"
)
df_salary = pd.DataFrame(config.salary, index=["$/month"]).style.format("{:.2f}")
df_salary_per_department = pd.DataFrame(config.salary_per_department).style.format(
    "{:.2f}"
)
st.table(df_gship_tuition)
st.table(df_salary)
st.table(df_salary_per_department)
