import numpy as np

gship_tuition = {
    "Gship": 539.33,
    "Instate": 1509.01,
    "Non-resident": 1678,
    "Tuition inflation": 0.1,
}

salary = {
    "Step 8": 6514.81,
    "Step 9": 6656.08,
    "Step 10": 7186.58,
    "Salary_inflation": 0.03,
}

salary_per_department = {
    "ece": {
        "pre-master": np.nan,
        "pre-candidacy": 0.45 * salary["Step 9"],
        "post-candidacy": 0.45 * salary["Step 10"],
    },
    "cs": {
        "pre-master": 0.49 * salary["Step 8"],
        "pre-candidacy": 0.49 * salary["Step 9"],
        "post-candidacy": 0.49 * salary["Step 10"],
    },
    "phys": {
        "pre-master": np.nan,
        "pre-candidacy": 0.4999 * salary["Step 8"],
        "post-candidacy": 0.4999 * salary["Step 9"],
    },
}

candidacy_per_department = {
    "ece": 4,
    "cs": 3,
    "phys": 3,
}