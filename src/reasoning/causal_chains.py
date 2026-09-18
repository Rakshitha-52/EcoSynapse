"""
Causal reasoning templates for EcoSynapse.

Each chain connects an environmental condition to:
- intermediate ecological mechanism
- affected environmental metrics
- evidence-oriented practices
"""

CAUSAL_CHAINS = {

    "low_organic_carbon": {
        "trigger": "Low soil organic carbon",
        "mechanism": [
            "Reduced soil organic matter can weaken soil structure",
            "Lower soil water retention can increase sensitivity to dry conditions",
            "Reduced soil quality can affect vegetation and below-ground biological activity"
        ],
        "affected_metrics": [
            "organic_carbon",
            "soil_erosion",
            "freshwater_pc",
            "regional_species_richness"
        ],
        "practices": [
            "cover_crops",
            "organic_amendments",
            "reduced_tillage"
        ]
    },

    "low_forest_cover": {
        "trigger": "Low forest cover",
        "mechanism": [
            "Reduced vegetation cover can decrease available habitat",
            "Habitat loss can increase fragmentation and reduce ecological connectivity",
            "Reduced habitat availability can place pressure on species richness"
        ],
        "affected_metrics": [
            "forest_pct",
            "regional_species_richness",
            "extinction_risk_count"
        ],
        "practices": [
            "native_reforestation",
            "agroforestry"
        ]
    },

    "high_pesticide_intensity": {
        "trigger": "High pesticide intensity",
        "mechanism": [
            "High pesticide pressure can affect non-target organisms",
            "Pollinator and insect communities can be exposed to chemical pressure",
            "Reduced abundance of ecological functional groups can affect ecosystem functioning"
        ],
        "affected_metrics": [
            "pesticide_intensity",
            "regional_species_richness",
            "extinction_risk_count"
        ],
        "practices": [
            "crop_diversification",
            "buffer_strips"
        ]
    },

    "water_stress": {
        "trigger": "Water stress",
        "mechanism": [
            "Limited water availability can constrain plant growth",
            "Reduced vegetation productivity can affect habitat quality",
            "Water stress can increase pressure on species dependent on available water"
        ],
        "affected_metrics": [
            "freshwater_pc",
            "rainfall",
            "regional_species_richness"
        ],
        "practices": [
            "cover_crops",
            "agroforestry",
            "organic_amendments"
        ]
    },

    "high_extinction_risk": {
        "trigger": "High number of species at extinction risk",
        "mechanism": [
            "High extinction risk indicates pressure on vulnerable species",
            "Habitat degradation can reduce suitable ecological niches",
            "Restoring habitat can improve ecological conditions for vulnerable species"
        ],
        "affected_metrics": [
            "extinction_risk_count",
            "forest_pct",
            "regional_species_richness"
        ],
        "practices": [
            "native_reforestation",
            "agroforestry",
            "buffer_strips"
        ]
    },

    "high_disaster_exposure": {
        "trigger": "High climate or hydrological disaster exposure",
        "mechanism": [
            "Frequent climate-related disturbances can damage vegetation and habitats",
            "Repeated disturbance can reduce ecosystem resilience",
            "Landscape-level vegetation can help improve ecological resilience"
        ],
        "affected_metrics": [
            "disaster_count",
            "forest_pct",
            "soil_erosion"
        ],
        "practices": [
            "agroforestry",
            "native_reforestation",
            "cover_crops"
        ]
    },

    "monoculture_land_use": {
        "trigger": "High agricultural land pressure or monoculture",
        "mechanism": [
            "Simplified agricultural landscapes can reduce habitat diversity",
            "Reduced habitat diversity can limit ecological niches",
            "Diversified vegetation can provide additional habitat and ecological functions"
        ],
        "affected_metrics": [
            "agricultural_pct",
            "regional_species_richness",
            "forest_pct"
        ],
        "practices": [
            "crop_diversification",
            "intercropping",
            "agroforestry"
        ]
    }
}