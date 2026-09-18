🌱 EcoSynapse
Evidence-Grounded Biodiversity Intelligence System

EcoSynapse is an AI-powered environmental intelligence system designed for the Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge.

It analyzes interconnected environmental conditions such as soil health, rainfall, land use, biodiversity, and human impact, then generates actionable recommendations grounded in scientific literature and environmental datasets.

The system combines:

Structured environmental datasets
Scientific reports and research documents
Semantic embeddings and FAISS retrieval
Multi-risk causal reasoning
Conversational memory
Evidence-grounded LLM generation
A Streamlit conversational interface

The goal is to behave like an AI environmental scientist rather than a generic chatbot.

🚀 Key Features
1. Evidence-Grounded Recommendations

EcoSynapse does not rely only on an LLM's internal knowledge.

For every recommendation, the system retrieves relevant evidence from its scientific knowledge base and provides:

Recommendation
Scientific reasoning
Impacted environmental metrics
Time horizon
Source document and page
Evidence limitations

Example:

Low organic carbon + low rainfall
→ reduced soil water retention
→ Conservation Agriculture / organic matter management
→ improved soil carbon, water retention and erosion resilience

2. Multi-Metric Environmental Reasoning

Environmental problems rarely occur independently.

EcoSynapse explicitly reasons across connected variables:

Soil Health
     ↓
Water Retention
     ↓
Vegetation / Habitat Quality
     ↓
Biodiversity

and:

Pesticide Intensity
        +
Habitat Loss
        ↓
Pressure on Biodiversity
        ↓
Crop Diversification + Habitat Restoration

The reasoning engine supports combinations such as:

Low organic carbon + water stress
Low forest cover + high extinction risk
High pesticide intensity + low forest cover
High pesticide intensity + monoculture
High disaster exposure + low forest cover

This directly addresses the challenge requirement to reason across multiple environmental variables.

🧠 System Architecture
                         ┌──────────────────────┐
                         │      User Query      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │ Environmental Signal Parsing │
                    │      + Conversation Memory   │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       Risk Detection         │
                    │                              │
                    │ Soil │ Climate │ Land │ Bio  │
                    │ Human Impact                  │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │    Multi-Risk Reasoning      │
                    │                              │
                    │ Causal Chains + Interactions │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
          ┌──────────────────┐          ┌──────────────────┐
          │ Structured Data  │          │ Scientific PDFs  │
          │                  │          │                  │
          │ Land             │          │ FAO              │
          │ Biodiversity     │          │ IPCC             │
          │ Pesticides       │          │ IPBES            │
          │ Climate          │          │ UNCCD            │
          │ Environmental   │          │ NRSC / IMD       │
          └────────┬─────────┘          └────────┬─────────┘
                   │                             │
                   ▼                             ▼
          ┌──────────────────┐          ┌──────────────────┐
          │ Metric Lookup    │          │ Chunking         │
          │                  │          │ Metadata         │
          │ CSV / Registry   │          │ Embeddings       │
          └──────────────────┘          │ FAISS            │
                                        └────────┬─────────┘
                                                 │
                                                 ▼
                                      ┌────────────────────┐
                                      │ Evidence Retrieval │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │ Grounded RAG Prompt│
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │    Gemini LLM      │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                              ┌────────────────────────────────┐
                              │ Structured Environmental Answer│
                              │                                │
                              │ Recommendation                 │
                              │ Why                            │
                              │ Impacted Metrics               │
                              │ Time Horizon                   │
                              │ Scientific Evidence            │
                              │ Evidence Limitation            │
                              └────────────────────────────────┘
📁 Project Structure
EcoSynapse/
│
├── app/
│   └── app.py
│
├── data/
│   ├── master/
│   │   ├── agricultural_land.csv
│   │   ├── biodiversity_indicators.csv
│   │   ├── biodiversity_observations.csv
│   │   ├── climatewatch_ghg.csv
│   │   ├── darukaa_land_reference.csv
│   │   ├── environmental_indicators.csv
│   │   ├── forest_area.csv
│   │   └── pesticide_use.csv
│   │
│   ├── supporting/
│   │   ├── agriculture_context.csv
│   │   ├── india_state_species_richness.csv
│   │   ├── global_soil_health_metadata.json
│   │   ├── soil_health_metadata.csv
│   │   └── FAOSTAT supporting datasets
│   │
│   ├── knowledge_base/
│   │   ├── biodiversity/
│   │   ├── climate_and_risks/
│   │   ├── land_and_ecosystems/
│   │   ├── pollution/
│   │   ├── scientific_reports/
│   │   └── soil/
│   │
│   └── raw/
│
├── index/
│   ├── extracted_text/
│   ├── chunks.jsonl
│   ├── chunk_metadata.jsonl
│   ├── embeddings.npy
│   ├── faiss.index
│   └── faiss_row_to_chunk_id.json
│
├── src/
│   ├── schema/
│   │   ├── vocab.py
│   │   ├── metric_registry.json
│   │   ├── metric_loader.py
│   │   └── chunk_schema.py
│   │
│   ├── ingestion/
│   │   ├── 1_extract_text.py
│   │   ├── 2_chunk_documents.py
│   │   ├── 3_tag_chunks.py
│   │   ├── 4_build_embeddings.py
│   │   ├── 5_build_faiss_index.py
│   │   └── retriever.py
│   │
│   ├── reasoning/
│   │   ├── causal_chains.py
│   │   ├── risk_combination.py
│   │   └── reasoning_engine.py
│   │
│   ├── rag/
│   │   ├── prompt.py
│   │   ├── rag_pipeline.py
│   │   └── llm.py
│   │
│   └── conversation/
│       ├── memory.py
│       ├── state_analyzer.py
│       └── conversation_manager.py
│
├── tests/
│   ├── test_memory.py
│   ├── test_conversation.py
│   ├── test_reasoning_retrieval.py
│   ├── test_rag_pipeline.py
│   └── test_gemini_rag.py
│
├── requirements.txt
└── README.md
📚 Knowledge Base

EcoSynapse uses two complementary knowledge layers.

Structured Environmental Data

The structured layer contains environmental indicators used for direct metric lookup and environmental context.

Biodiversity
Biodiversity observations
Species counts
Endemic species indicators
Threatened / extinction-risk indicators
State-level species richness
Land Use
Forest area
Agricultural land
Land-use / land-cover context
Human Impact
Pesticide use
Pesticide intensity per cropland area
SO₂
NOx
Hazardous waste
Transport-related GHG emissions
Climate and Environmental Risk
Rainfall-related context
Freshwater availability
Climatological disaster indicators
Hydrological disaster indicators

The structured datasets are maintained separately from the document retrieval layer so numerical/environmental lookups do not need to be embedded.

📖 Scientific Knowledge Base

The unstructured knowledge layer contains scientific and institutional reports from sources including:

Food and Agriculture Organization (FAO)
Intergovernmental Panel on Climate Change (IPCC)
Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services (IPBES)
United Nations Convention to Combat Desertification (UNCCD)
National Remote Sensing Centre (NRSC)
India Meteorological Department (IMD)

The current knowledge base contains 19 PDF documents covering:

Soil health
Soil organic carbon
Conservation agriculture
Land degradation
Land use / land cover
Biodiversity
Climate risks
Pollution
Ecosystem services
🔎 Retrieval Pipeline

Scientific documents are processed through the following pipeline:

PDF Documents
     ↓
Page-level Text Extraction
     ↓
Paragraph-aware Chunking
     ↓
Metadata Tagging
     ↓
Sentence Transformer Embeddings
     ↓
FAISS Vector Index
     ↓
Semantic Retrieval
     ↓
Evidence Filtering
     ↓
Grounded LLM Prompt
Embeddings

The system uses:

all-MiniLM-L6-v2

with normalized embeddings.

The resulting embeddings have:

1286 chunks × 384 dimensions
Vector Search

FAISS IndexFlatIP is used for similarity search.

Because embeddings are normalized, inner-product similarity corresponds to cosine similarity.

🧩 Metadata-Aware Knowledge Layer

Each retrieved chunk contains metadata such as:

{
  "chunk_id": "...",
  "text": "...",
  "source": "FAO",
  "document": "...",
  "year": 2026,
  "page": 118,
  "topic": "soil_health",
  "metric": ["organic_carbon"],
  "practice": ["reduced_tillage"],
  "region_scope": "global",
  "claim_type": "practice_evidence"
}

This allows EcoSynapse to distinguish between:

Background information
Quantified evidence
Practice-specific evidence

Practice-specific and quantified evidence are prioritized when generating recommendations.

🧠 Reasoning Engine

The reasoning layer operates before the LLM.

It maps detected environmental risks to causal chains.

For example:

Low Organic Carbon
        ↓
Reduced Soil Structure
        ↓
Lower Water Retention
        ↓
Higher Sensitivity to Dry Conditions
        ↓
Water Stress
        ↓
Vegetation / Habitat Pressure

Another example:

Low Forest Cover
        ↓
Habitat Loss + Fragmentation
        ↓
Reduced Ecological Connectivity
        ↓
Pressure on Species
        ↓
Higher Extinction Risk

For combinations of risks, the reasoning engine creates an interaction rather than treating every risk independently.

💬 Conversational Intelligence

EcoSynapse maintains environmental context across turns.

Example:

User:
My farm has low organic carbon and low rainfall.

EcoSynapse:
[detects low organic carbon + water stress]

User:
What should I do?

EcoSynapse:
[uses the previously established environmental context]

The system also supports scenario reset through the New Scenario control to prevent unrelated environmental cases from sharing state.

For incomplete queries such as:

What should I do?

without an established environmental condition, the system can request additional information rather than inventing environmental signals.

🤖 RAG + LLM Generation

The LLM does not receive only the user's question.

The prompt contains:

User query
Detected environmental risks
Causal reasoning
Recommended practices
Impacted metrics
Retrieved scientific evidence
Source metadata
Page numbers
Evidence limitations

The model is instructed to:

Use supplied evidence for scientific claims
Avoid fabricating studies or statistics
Preserve source/page information
Distinguish evidence from ecological reasoning
State when evidence is insufficient
Avoid treating generic biodiversity information as direct evidence for a specific practice
📊 Output Format

EcoSynapse generates structured responses containing:

Recommendation

Specific actions that can be taken.

Why

The ecological mechanism connecting the observed conditions to the recommendation.

Impacted Metrics

Environmental variables expected to be affected.

Time Horizon
Short-term
Medium-term
Long-term
Scientific Evidence

Retrieved scientific sources with document and page references.

Evidence Limitation

Explicitly identifies where available evidence is indirect, insufficient, or non-quantitative.

🛠️ Technology Stack
Component	Technology
Language	Python
UI	Streamlit
LLM	Google Gemini
RAG	Custom retrieval pipeline
Embeddings	Sentence Transformers
Embedding Model	all-MiniLM-L6-v2
Vector Database	FAISS
Data Processing	Pandas, NumPy
PDF Extraction	pdfplumber
Schema / Metadata	JSON, JSONL
Environment	Python virtual environment
Version Control	Git / GitHub
⚙️ Local Setup
1. Clone the repository
git clone https://github.com/Rakshitha-52/EcoSynapse.git
cd EcoSynapse
2. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate
3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
4. Configure Gemini API key

PowerShell:

$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

Do not commit API keys to GitHub.

🏗️ Build the Knowledge Index

If rebuilding the knowledge index from the source PDFs:

Extract PDF text
python src/ingestion/1_extract_text.py
Create document chunks
python src/ingestion/2_chunk_documents.py
Add metadata
python src/ingestion/3_tag_chunks.py
Generate embeddings
python src/ingestion/4_build_embeddings.py
Build FAISS index
python src/ingestion/5_build_faiss_index.py
▶️ Run the Application
python -m streamlit run app/app.py

The application will open in the browser.

🧪 Testing

Run the reasoning retrieval test:

python -m tests.test_reasoning_retrieval

Test conversational memory:

python -m tests.test_memory

Test conversation handling:

python -m tests.test_conversation

Test RAG prompt generation:

python -m tests.test_rag_pipeline

Test Gemini-powered RAG:

python -m tests.test_gemini_rag
🧪 Example Scenarios
Scenario 1 — Soil + Climate

Input

My farm has low organic carbon and low rainfall. What should I do?

EcoSynapse connects:

Low Organic Carbon
        +
Low Rainfall
        ↓
Water-retention pressure
        ↓
Reduced tillage + organic matter management
        + 
Organic soil cover
Scenario 2 — Forest + Biodiversity

Input

The region has low forest cover and high species extinction risk.

EcoSynapse connects:

Low Forest Cover
        ↓
Habitat Loss / Fragmentation
        ↓
Reduced Ecological Connectivity
        ↓
Species Extinction Risk

Possible interventions include native reforestation and agroforestry where supported by retrieved evidence.

Scenario 3 — Pesticides + Habitat

Input

My farm has high pesticide use and low forest cover.
What practices would improve biodiversity?

EcoSynapse combines:

High Pesticide Intensity
        +
Low Forest Cover
        ↓
Chemical Pressure + Habitat Pressure
        ↓
Biodiversity Risk
        ↓
Crop Diversification + Habitat Restoration

The final recommendation is grounded using retrieved FAO/IPBES evidence.

🔐 Evidence and Hallucination Control

EcoSynapse follows a retrieval-first approach.

The system:

User Query
    ↓
Risk Detection
    ↓
Reasoning
    ↓
Evidence Retrieval
    ↓
Evidence Filtering
    ↓
LLM Generation

rather than:

User Query
    ↓
LLM
    ↓
Recommendation

If sufficient evidence cannot be retrieved, the system can return:

I don't have sufficient scientific evidence in the
knowledge base to support a recommendation.

This keeps recommendations auditable and makes the retrieved scientific sources visible to the user.

🔄 CI/CD

The project is maintained using Git and GitHub.

Current development workflow:

Code Changes
     ↓
Git
     ↓
GitHub Repository
     ↓
Application Deployment

The repository contains the application source code, ingestion pipeline, reasoning engine, RAG pipeline, tests, datasets and documentation required to reproduce the system.

📈 Challenge Alignment

EcoSynapse was designed around the requirements of the Darukaa.Earth challenge.

Challenge Requirement	EcoSynapse Implementation
Structured knowledge base	Environmental CSV datasets + metric registry
Scientific knowledge retrieval	FAO, IPCC, IPBES, UNCCD, NRSC, IMD documents
RAG / vector database	Sentence Transformers + FAISS
Soil health	SOC and soil-management evidence
Land use / land cover	Forest and agricultural land datasets + LULC reports
Biodiversity	Biodiversity observations, species indicators and species richness
Climate	Rainfall, freshwater and climate-risk context
Human impact	Pesticide, pollution and GHG indicators
Clarifying questions	Conversation state analyzer
Multi-turn memory	Conversation memory
Multi-metric reasoning	Causal chains + risk combinations
Evidence-backed recommendations	Retrieved scientific evidence with page references
Actionable outputs	Recommendations + metrics + time horizons
Grounding	Evidence-first RAG prompting and evidence filtering
🎯 Design Goal

EcoSynapse is designed around one central principle:

Environmental recommendations should connect observed conditions, ecological mechanisms, measurable environmental metrics, and scientific evidence.

Rather than simply answering environmental questions, the system attempts to reason across interacting environmental factors and make the reasoning traceable through retrieved scientific sources.

👩‍💻 Author

Rakshitha B N

B.E. Artificial Intelligence & Machine Learning
BMS Institute of Technology and Management

GitHub:
https://github.com/Rakshitha-52/EcoSynapse