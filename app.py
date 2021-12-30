import datetime

import numpy as np
import pandas as pd
import streamlit as st

import config
import sim

config_tuition_df = pd.DataFrame(config.gship_tuition, index=[0])
config_salary_df = pd.DataFrame(config.salary, index=[0])

st.write("""# Budget Simulations""")

st.sidebar.header("Global Parameters")

today = datetime.date.today()


def input_features():
    start_funds = st.sidebar.number_input("Available Funds [$]", 340000.0)
    start_date = st.sidebar.text_input("Start Date", f"{today}")
    start_date = pd.to_datetime(start_date)
    end_date = st.sidebar.text_input("End Date", "2026-01-01")
    end_date = pd.to_datetime(end_date)
    return start_funds, start_date, end_date


start_funds, start_date, end_date = input_features()

st.sidebar.header("Student 1")


def input_student1():
    student_start_date = st.sidebar.text_input("Student Start Date", f"{start_date}")
    student_start_date = pd.to_datetime(student_start_date)
    department = st.sidebar.multiselect(
        "Student Department", ["ECE", "CS", "PHYS"], ["ECE"]
    )
    instate_date = st.sidebar.text_input("Student Instate", f"{student_start_date}")
    instate_date = pd.to_datetime(instate_date)
    return student_start_date, department, instate_date


student_start_date, department, instate_date = input_student1()


global_daterange = pd.date_range(start=start_date, end=end_date, freq="M")
n_months = len(global_daterange)
budget_df = pd.DataFrame(
    {
        "init": [
            start_funds,
        ]
        * n_months
    },
    index=global_daterange,
)
budget_df["zero"] = [
    0,
] * n_months

# Student 1
student1_daterange = pd.date_range(start=student_start_date, end=end_date, freq="M")
student1_costs = [
    0,
] * (len(global_daterange) - len(student1_daterange))
student1_costs.extend(sim.gship_tuition_student_costs(student1_daterange, instate_date))

budget_df["budget"] = [
    start_funds,
] * n_months - np.cumsum(student1_costs)

# Adjusted Close Price
st.header("Budget [$]")
st.line_chart(budget_df)

# Configuration
st.header("Configuration")

st.table(config_tuition_df)
st.table(config_salary_df)
