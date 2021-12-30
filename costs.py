import pandas as pd

import config

config.salary_per_department


def gship_tuition(date_range, instate_date):
    costs = []
    for one_date in date_range:
        month_cost = config.gship_tuition["Gship"]

        if one_date.month not in [6, 7, 8]:  # Summer
            month_cost += config.gship_tuition["Instate"]
            if one_date < instate_date:
                month_cost += config.gship_tuition["Non-resident"]
        costs.append(month_cost)

    return costs


def salary(date_range, department, overhead, candidacy_year=None):
    if candidacy_year is None:
        candidacy_year = config.salary_per_department[department]["candidacy year"]
        candidacy_year = date_range[0] + pd.to_timedelta(f"{candidacy_year}Y")
    costs = []
    for one_date in date_range:
        if one_date < candidacy_year:
            month_cost = config.salary_per_department[department]["pre-candidacy"]
        else:
            month_cost = config.salary_per_department[department]["post-candidacy"]

        if overhead:
            month_cost *= 1.555

        costs.append(month_cost)
    return costs


def student(date_range, department, instate_date, overhead, candidacy_year=None):
    return [
        a + b
        for a, b in zip(
            gship_tuition(date_range, instate_date),
            salary(date_range, department, overhead, candidacy_year),
        )
    ]
