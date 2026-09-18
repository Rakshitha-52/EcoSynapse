import re


class ConversationMemory:

    def __init__(self):

        self.state = {
            "location": None,
            "organic_carbon": None,
            "soil_ph": None,
            "forest_cover": None,
            "agricultural_land": None,
            "pesticide_intensity": None,
            "rainfall": None,
            "temperature": None,
            "freshwater_availability": None,
            "biodiversity_status": None
        }

        self.history = []

    def update(self, text):

        text_lower = text.lower()

        # Location/state
        states = [
            "karnataka",
            "kerala",
            "tamil nadu",
            "andhra pradesh",
            "telangana",
            "maharashtra",
            "goa",
            "odisha",
            "west bengal",
            "uttar pradesh",
            "madhya pradesh",
            "rajasthan",
            "gujarat",
            "punjab",
            "haryana"
        ]

        for state in states:
            if state in text_lower:
                self.state["location"] = state.title()

        # Soil organic carbon
        if "low organic carbon" in text_lower:
            self.state["organic_carbon"] = "low"

        elif "high organic carbon" in text_lower:
            self.state["organic_carbon"] = "high"

        # Soil pH
        ph_match = re.search(
            r"\bph\s*(?:is|=|:)?\s*(\d+(?:\.\d+)?)",
            text_lower
        )

        if ph_match:
            self.state["soil_ph"] = float(ph_match.group(1))

        # Forest cover
        if "low forest cover" in text_lower:
            self.state["forest_cover"] = "low"

        elif "high forest cover" in text_lower:
            self.state["forest_cover"] = "high"

        # Pesticides
        if "high pesticide" in text_lower:
            self.state["pesticide_intensity"] = "high"

        elif "low pesticide" in text_lower:
            self.state["pesticide_intensity"] = "low"

        # Rainfall
        if "low rainfall" in text_lower:
            self.state["rainfall"] = "low"

        elif "high rainfall" in text_lower:
            self.state["rainfall"] = "high"

        # Water
        if "water stress" in text_lower:
            self.state["freshwater_availability"] = "low"

        # Biodiversity
        if "high extinction risk" in text_lower:
            self.state["biodiversity_status"] = "high_extinction_risk"

        self.history.append(text)

    def get_state(self):

        return {
            key: value
            for key, value in self.state.items()
            if value is not None
        }

    def get_history(self):

        return self.history

    def missing_for_analysis(self):

        state = self.get_state()

        if not state:
            return ["environmental condition"]

        return []