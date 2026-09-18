import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.conversation.conversation_manager import ConversationManager
from src.rag.rag_pipeline import EcoSynapseRAG
from src.rag.llm import GeminiLLM


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="EcoSynapse",
    page_icon="🌱",
    layout="wide"
)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "conversation" not in st.session_state:
    st.session_state.conversation = ConversationManager()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag" not in st.session_state:
    st.session_state.rag = EcoSynapseRAG()

if "llm" not in st.session_state:
    st.session_state.llm = GeminiLLM()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🌱 EcoSynapse")

st.markdown(
    """
    **Evidence-Grounded Biodiversity Intelligence**

    Analyze interconnected environmental conditions using
    scientific evidence from the EcoSynapse knowledge base.
    """
)

st.divider()

with st.sidebar:
    st.header("EcoSynapse")

    if st.button("🆕 New Scenario"):
        st.session_state.conversation.reset()
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# Display previous conversation
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# User input
# --------------------------------------------------

user_query = st.chat_input(
    "Describe an environmental condition..."
)


if user_query:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    # --------------------------------------------------
    # Process conversation state
    # --------------------------------------------------

    conversation_result = (
        st.session_state.conversation.process(user_query)
    )

    state = conversation_result["state"]
    risks = conversation_result["risks"]

    # --------------------------------------------------
    # Handle missing information
    # --------------------------------------------------

    if conversation_result["clarification_needed"]:

        response = conversation_result[
            "clarification_question"
        ]

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

    elif not risks:

        response = (
            "I need more information about the environmental "
            "condition before I can generate a grounded recommendation. "
            "For example, you can mention soil health, forest cover, "
            "pesticide use, rainfall, water availability, or biodiversity."
        )

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

    else:

        # --------------------------------------------------
        # Generate grounded answer
        # --------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing environmental signals and scientific evidence..."
            ):

                result = st.session_state.rag.answer(
                    query=user_query,
                    risks=risks,
                    llm_callable=st.session_state.llm.generate
                )

            st.markdown(result["answer"])

            # --------------------------------------------------
            # Show environmental signals
            # --------------------------------------------------

            with st.expander("Environmental signals"):

                for key, value in state.items():
                    st.write(
                        f"**{key.replace('_', ' ').title()}:** {value}"
                    )

            # --------------------------------------------------
            # Show detected risks
            # --------------------------------------------------

            with st.expander("Detected risks"):

                for risk in risks:
                    st.write(
                        f"• {risk.replace('_', ' ').title()}"
                    )

            # --------------------------------------------------
            # Show retrieved evidence
            # --------------------------------------------------

            with st.expander("Retrieved scientific evidence"):

                for i, (chunk, score) in enumerate(
                    result["evidence"], 1
                ):

                    st.markdown(
                        f"**{i}. {chunk.get('document')} — "
                        f"Page {chunk.get('page')}**"
                    )

                    st.caption(
                        f"Similarity: {float(score):.4f} | "
                        f"Claim type: {chunk.get('claim_type')}"
                    )

                    st.write(
                        chunk.get("text", "")[:1000]
                    )

                    st.divider()

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result["answer"]
            }
        )