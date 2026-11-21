def calculate_risk_score(likelihood, impact):

    if likelihood < 1 or likelihood > 5:
        raise ValueError("Likelihood must be between 1 and 5")

    if impact < 1 or impact > 5:
        raise ValueError("Impact must be between 1 and 5")

    score = likelihood * impact

    return score


def classify_risk(score):

    if score < 1 or score > 25:
        raise ValueError("Risk score must be between 1 and 25")

    if score <= 4:
        return "Low"

    elif score <= 9:
        return "Medium"

    elif score <= 16:
        return "High"

    else:
        return "Critical"