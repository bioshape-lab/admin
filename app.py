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
    startup_funds = st.sidebar.number_input("Startup Funds [$]", 379835.00)
    nsf_grants_funds = st.sidebar.number_input("NSF Grant Funds [$]", 334786.00)
    funds = startup_funds + nsf_grants_funds
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
    start1 = st.sidebar.text_input("Student Start Date", f"{today}")
    start1 = pd.to_datetime(start1)

    instate_start1 = st.sidebar.text_input("Student Instate", f"{today}")
    instate_start1 = pd.to_datetime(instate_start1)

    candidacy1 = st.sidebar.number_input(
        "Candidacy Year", config.salary_per_department[department1]["candidacy year"]
    )
    overhead1 = st.sidebar.selectbox(
        "Overhead", ["yes (contract grant)", "no (startup funds)"], index=0, key="grant"
    )
    return start1, department1, instate_start1, candidacy1, overhead1


start1, department1, instate_start1, candidacy1, overhead1 = input_student1()
daterange1 = pd.date_range(start=start1, end=end, freq="M")
costs1_zeros = [0] * (len(daterange) - len(daterange1))
costs1_nonzeros = costs.student(
    daterange1, department1, instate_start1, overhead1, candidacy_year=candidacy1
)
costs1 = costs1_zeros + costs1_nonzeros
cumcost1 = np.cumsum(costs1)

budget_dict = {
    "init": [funds] * len(daterange),
    "zero": [funds] * len(daterange),
    "student1": cumcost1,
    "result": [funds] * len(daterange) - cumcost1,
}

budget_df = pd.DataFrame(budget_dict, index=daterange)

# Adjusted Close Price
st.header("Budget [$]")
st.line_chart(budget_df)

# Configuration
st.header("Configuration")

st.table(pd.DataFrame(config.gship_tuition, index=["$/month"]))
st.table(pd.DataFrame(config.salary, index=["$/month"]))
st.table(pd.DataFrame(config.salary_per_department))
st.table(pd.DataFrame(config.candidacy_per_department, index=["Year index"]))
