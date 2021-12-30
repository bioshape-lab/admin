import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

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


name_dict = config.name_dict

for student_key, student_dict in name_dict.items():
    st.sidebar.header(
        student_key,
    )
    student_dict["department"] = st.sidebar.selectbox(
        "Student Department",
        ["ece", "cs", "phys"],
        index=0,
        key=student_key,
    )
    student_dict["start"] = pd.to_datetime(
        st.sidebar.text_input(
            "Student Start Date",
            "2022-09",
            key=student_key,
        )
    )
    student_dict["end"] = pd.to_datetime(
        st.sidebar.text_input(
            "Student End Date",
            "2026-09",
            key=student_key,
        )
    )
    student_dict["instate"] = pd.to_datetime(
        st.sidebar.text_input(
            "Student Instate",
            "2022-09",
            key=student_key,
        )
    )
    student_dict["candidacy"] = st.sidebar.number_input(
        "Candidacy Year",
        value=config.salary_per_department[student_dict["department"]][
            "candidacy year"
        ],
        key=student_key,
    )

    overhead = st.sidebar.selectbox(
        "Overhead",
        ["yes (contract grant)", "no (startup funds)"],
        index=0,
        key=student_key,
    )
    student_dict["overhead"] = overhead == "yes (contract grant)"


start1, end1 = name_dict["Student 1"]["start"], name_dict["Student 1"]["end"]
start, end = min(start, start1), max(end, end1)
costs1 = costs.student(name_dict["Student 1"])
costs1 = costs.over_date_range(start, end, start1, end1, costs1)

start2, end2 = name_dict["Student 2"]["start"], name_dict["Student 2"]["end"]
start, end = min(start, start2), max(end, end2)
costs2 = costs.student(name_dict["Student 2"])
costs2 = costs.over_date_range(start, end, start2, end2, costs2)

start3, end3 = name_dict["Student 3"]["start"], name_dict["Student 3"]["end"]
start, end = min(start, start3), max(end, end3)
costs3 = costs.student(name_dict["Student 3"])
costs3 = costs.over_date_range(start, end, start3, end3, costs3)

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
student1_str = "Student 1 (" + name_dict["Student 1"]["department"] + ")"
student2_str = "Student 2 (" + name_dict["Student 2"]["department"] + ")"
student3_str = "Student 3 (" + name_dict["Student 3"]["department"] + ")"

budget_dict = {
    "date": daterange.date,
    student1_str: np.cumsum(costs1),
    student2_str: np.cumsum(costs2),
    student3_str: np.cumsum(costs3),
    "Sra": np.cumsum(costs_sra),
    "Zero": [0.0] * len(daterange),
    "Rest": [funds] * len(daterange)
    - np.cumsum(costs1)
    - np.cumsum(costs2)
    - np.cumsum(costs3)
    - np.cumsum(costs_sra),
}
color_dict = {
    student1_str: "lightblue",
    student2_str: "darkblue",
    student3_str: "blue",
    "Sra": "orange",
    "Zero": "red",
    "Rest": "green",
}


budget_df = pd.DataFrame(budget_dict, index=daterange.date)


st.header("Budget [$]")
fig = px.line(
    budget_df,
    x="date",
    y=budget_df.columns[1:],
    color_discrete_map=color_dict,
)

st.plotly_chart(fig, use_container_width=True)

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
