"""
Multi-risk reasoning rules.

These rules identify interactions between environmental risks.
The purpose is to produce recommendations that consider
multiple environmental variables together.
"""


RISK_COMBINATIONS = {

    frozenset({
        "low_forest_cover",
        "high_extinction_risk"
    }): {
        "interaction": (
            "Low forest cover combined with high extinction risk "
            "suggests that habitat availability and ecological connectivity "
            "should be considered together."
        ),
        "reasoning": [
            "Reduced forest cover can decrease habitat availability",
            "Species already at extinction risk may have fewer suitable habitats",
            "Habitat restoration and connectivity can address both pressures"
        ],
        "recommended_practices": [
            "native_reforestation",
            "agroforestry",
            "buffer_strips"
        ],
        "affected_metrics": [
            "forest_pct",
            "extinction_risk_count",
            "regional_species_richness"
        ]
    },


    frozenset({
        "high_pesticide_intensity",
        "low_forest_cover"
    }): {
        "interaction": (
            "Pesticide pressure combined with low vegetation cover "
            "can create simultaneous chemical and habitat pressures "
            "on biodiversity."
        ),
        "reasoning": [
            "Pesticide intensity represents chemical pressure",
            "Low forest or vegetation cover represents habitat pressure",
            "Reducing chemical dependence while restoring vegetation "
            "addresses both dimensions"
        ],
        "recommended_practices": [
            "crop_diversification",
            "buffer_strips",
            "agroforestry"
        ],
        "affected_metrics": [
            "pesticide_intensity",
            "forest_pct",
            "regional_species_richness"
        ]
    },


    frozenset({
        "low_organic_carbon",
        "water_stress"
    }): {
        "interaction": (
            "Low soil organic carbon combined with water stress "
            "indicates interacting soil and water-retention pressures."
        ),
        "reasoning": [
            "Low organic carbon can reduce soil structural quality",
            "Water stress limits available moisture",
            "Improving soil organic matter can support water retention "
            "while reducing erosion pressure"
        ],
        "recommended_practices": [
            "cover_crops",
            "organic_amendments",
            "reduced_tillage"
        ],
        "affected_metrics": [
            "organic_carbon",
            "freshwater_pc",
            "soil_erosion"
        ]
    },


    frozenset({
        "high_disaster_exposure",
        "low_forest_cover"
    }): {
        "interaction": (
            "High disaster exposure combined with low forest cover "
            "suggests reduced landscape resilience."
        ),
        "reasoning": [
            "Repeated climate or hydrological disturbances can damage ecosystems",
            "Low vegetation cover can increase landscape vulnerability",
            "Restoring vegetation can improve habitat and landscape resilience"
        ],
        "recommended_practices": [
            "native_reforestation",
            "agroforestry",
            "cover_crops"
        ],
        "affected_metrics": [
            "disaster_count",
            "forest_pct",
            "soil_erosion"
        ]
    },


    frozenset({
        "high_pesticide_intensity",
        "monoculture_land_use"
    }): {
        "interaction": (
            "High pesticide intensity combined with simplified agricultural "
            "land use can create simultaneous chemical and habitat pressures."
        ),
        "reasoning": [
            "Monoculture can reduce habitat diversity",
            "High pesticide use adds chemical pressure",
            "Crop diversification can improve habitat heterogeneity "
            "while supporting reduced pesticide dependence"
        ],
        "recommended_practices": [
            "crop_diversification",
            "intercropping",
            "buffer_strips"
        ],
        "affected_metrics": [
            "pesticide_intensity",
            "agricultural_pct",
            "regional_species_richness"
        ]
    }
}


def get_combination(risks):
    """
    Return the strongest matching multi-risk rule.

    Parameters
    ----------
    risks : iterable[str]
        Detected environmental risks.

    Returns
    -------
    dict | None
        Matching combination rule.
    """

    risk_set = set(risks)

    # Prefer the most specific rule with the largest number
    # of matching risks.
    matches = []

    for combination, rule in RISK_COMBINATIONS.items():
        overlap = risk_set.intersection(combination)

        if len(overlap) == len(combination):
            matches.append((len(combination), rule))

    if not matches:
        return None

    matches.sort(key=lambda x: x[0], reverse=True)

    return matches[0][1]