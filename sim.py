import pandas as pd

import config


def gship_tuition_student_costs(date_range, instate_date):
    costs = []
    for one_date in date_range:
        month_cost = config.gship_tuition["Gship"]

        if one_date.month not in [6, 7, 8]:  # Summer
            month_cost += config.gship_tuition["Instate"]
            if one_date < instate_date:
                month_cost += config.gship_tuition["Non-resident"]
        costs.append(month_cost)

    return costs


def salary_student_costs(department, date_range, candidacy_date=None):
    if candidacy_date is None:
        candidacy_date = date_range.start + pd.to_timedelta("4Y")
    costs = []
    for one_date in date_range:
        if one_date < candidacy_date:
            month_cost = config.phys["pre-candidacy"]
        else:
            month_cost = config.phys["post-candidacy"]
        costs.append(month_cost)
    return costs
