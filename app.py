import datetime

import numpy as np
import pandas as pd
import streamlit as st

import config
import costs

st.write("""# Budget Simulations""")

st.sidebar.header("Global Parameters")
today = datetime.date.today()


def input_features():
    funds = st.sidebar.number_input("Available Funds [$]", 340000.0)
    start = st.sidebar.text_input("Start Date", f"{today}")
    start = pd.to_datetime(start)
    end = st.sidebar.text_input("End Date", "2026-01-01")
    end = pd.to_datetime(end)
    return funds, start, end


funds, start, end = input_features()
daterange = pd.date_range(start=start, end=end, freq="M")

st.sidebar.header("Student 1")


def input_student1():
    department1 = st.sidebar.selectbox(
        "Student Department", ["ece", "cs", "phys"], index=0, key="department1"
    )
    start1 = st.sidebar.text_input("Student Start Date", f"{start}")
    start1 = pd.to_datetime(start1)

    instate_start1 = st.sidebar.text_input("Student Instate", f"{start1}")
    instate_start1 = pd.to_datetime(instate_start1)
    return start1, department1, instate_start1


start1, department1, instate_start1 = input_student1()
daterange1 = pd.date_range(start=start1, end=end, freq="M")
costs1 = [
    0,
] * (len(daterange) - len(daterange1))
costs1.extend(costs.student(daterange1, department1, instate_start1))

n_months = len(daterange)
budget_df = pd.DataFrame(
    {
        "init": [
            funds,
        ]
        * n_months
    },
    index=daterange,
)
budget_df["zero"] = [
    0,
] * n_months


budget_df["budget"] = [
    funds,
] * n_months - np.cumsum(costs1)

# Adjusted Close Price
st.header("Budget [$]")
st.line_chart(budget_df)

# Configuration
st.header("Configuration")

st.table(pd.DataFrame(config.gship_tuition, index=["$/month"]))
st.table(pd.DataFrame(config.salary, index=["$/month"]))
st.table(pd.DataFrame(config.salary_per_department))
st.table(pd.DataFrame(config.candidacy_per_department, index=["Year index"]))
