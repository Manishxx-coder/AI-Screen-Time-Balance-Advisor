import numpy as np
import skfuzzy as fuzz

def evaluate_balance(screen_time, study_time, sleep_time):
    screen = np.arange(0, 13, 0.1)
    study = np.arange(0, 13, 0.1)
    sleep = np.arange(3, 11, 0.1)
    output = np.arange(0, 101, 1)

    screen_low = fuzz.trapmf(screen, [0, 0, 2, 4])
    screen_medium = fuzz.trimf(screen, [2, 5, 8])
    screen_high = fuzz.trapmf(screen, [6, 9, 12, 12])

    study_low = fuzz.trapmf(study, [0, 0, 1, 3])
    study_medium = fuzz.trimf(study, [2, 4, 7])
    study_high = fuzz.trapmf(study, [6, 8, 12, 12])

    sleep_low = fuzz.trapmf(sleep, [3, 3, 5, 6.5])
    sleep_normal = fuzz.trimf(sleep, [5.5, 7, 8.5])
    sleep_high = fuzz.trapmf(sleep, [7.5, 9, 10, 10])

    poor = fuzz.trapmf(output, [0, 0, 20, 40])
    moderate = fuzz.trimf(output, [25, 50, 70])
    good = fuzz.trapmf(output, [55, 75, 100, 100])

    sl = fuzz.interp_membership(screen, screen_low, screen_time)
    sm = fuzz.interp_membership(screen, screen_medium, screen_time)
    sh = fuzz.interp_membership(screen, screen_high, screen_time)

    stl = fuzz.interp_membership(study, study_low, study_time)
    stm = fuzz.interp_membership(study, study_medium, study_time)
    sth = fuzz.interp_membership(study, study_high, study_time)

    spl = fuzz.interp_membership(sleep, sleep_low, sleep_time)
    spn = fuzz.interp_membership(sleep, sleep_normal, sleep_time)

    poor_rules = [min(sh, stl), min(sh, spl), min(stl, spl)]
    moderate_rules = [min(sh, stm), min(sm, stl), min(sm, spl)]
    good_rules = [min(sl, sth, spn), min(sm, sth), min(sl, spn)]

    aggregated = np.zeros_like(output, dtype=float)

    for strength in poor_rules:
        aggregated = np.fmax(aggregated, np.fmin(strength, poor))
    for strength in moderate_rules:
        aggregated = np.fmax(aggregated, np.fmin(strength, moderate))
    for strength in good_rules:
        aggregated = np.fmax(aggregated, np.fmin(strength, good))

    if np.max(aggregated) == 0:
        aggregated = moderate

    score = fuzz.defuzz(output, aggregated, "centroid")

    if score < 40:
        level = "Poor"
    elif score < 70:
        level = "Moderate"
    else:
        level = "Good"

    return {"score": round(float(score), 2), "level": level}
