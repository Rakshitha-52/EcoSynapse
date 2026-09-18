"""
Convert conversation state into environmental risk signals.
"""


def detect_risks(state):

    risks = []

    if state.get("organic_carbon") == "low":
        risks.append("low_organic_carbon")

    if state.get("forest_cover") == "low":
        risks.append("low_forest_cover")

    if state.get("pesticide_intensity") == "high":
        risks.append("high_pesticide_intensity")

    if state.get("rainfall") == "low":
        risks.append("water_stress")

    if state.get("freshwater_availability") == "low":
        risks.append("water_stress")

    if state.get("biodiversity_status") == "high_extinction_risk":
        risks.append("high_extinction_risk")

    return list(dict.fromkeys(risks))


def needs_clarification(state):

    if not state:
        return True, "What environmental condition would you like to analyze?"

    return False, None