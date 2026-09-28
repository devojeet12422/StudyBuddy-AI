import random
import re
import streamlit as st

from pypdf import PdfReader
from docx import Document

from groq_client import ask_groq
from rag_engine import RAGEngine


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# MOTIVATIONAL QUOTES
# ============================================================

QUOTES = [
    "Success is the sum of small efforts, repeated day in and day out.",
    "Don't study to know more. Study to understand better.",
    "Your future self will thank you for studying today.",
    "One chapter today is one step closer to your goal.",
    "You don't have to be perfect. You just have to keep going.",
    "The secret of getting ahead is getting started.",
    "Focus on progress, not perfection.",
    "Study now. Make your future easier.",
    "Every expert was once a beginner.",
    "Your goals are bigger than your excuses.",
    "A little progress every day adds up to big results.",
    "Dream big. Study hard. Stay consistent.",
    "Small steps every day lead to big achievements.",
    "Don't stop until you are proud of yourself.",
    "The harder you work, the luckier you get."
]


# ============================================================
# SESSION STATE
# ============================================================

if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if "welcome_quote" not in st.session_state:
    st.session_state.welcome_quote = random.choice(QUOTES)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


## ============================================================
# ANIMATED WELCOME SCREEN
# ============================================================

if not st.session_state.welcome_shown:

    welcome_html = f"""
    <style>

        /* Hide Streamlit padding */
        .welcome-wrapper {{
            min-height: 70vh;

            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            text-align: center;

            position: relative;

            overflow: hidden;
        }}


        /* Small welcome text */

        .welcome-small {{
            font-size: 20px;
            letter-spacing: 7px;
            font-weight: 500;

            opacity: 0;

            animation: fadeDown 1s ease forwards;
        }}


        /* Main title */

        .welcome-title {{
            margin-top: 12px;

            font-size: 82px;
            font-weight: 900;
            letter-spacing: 3px;

            background: linear-gradient(
                90deg,
                #7c3aed,
                #06b6d4,
                #8b5cf6,
                #06b6d4
            );

            background-size: 300% 300%;

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            opacity: 0;

            animation:
                titleAppear 1.2s ease forwards,
                gradientMove 5s ease infinite,
                titleFloat 3s ease-in-out infinite;
        }}


        /* Subtitle */

        .welcome-subtitle {{
            margin-top: 12px;

            font-size: 20px;

            opacity: 0;

            animation:
                fadeUp 1s ease 0.8s forwards;
        }}


        /* Quote */

        .welcome-quote {{
            max-width: 700px;

            margin-top: 45px;

            font-size: 23px;

            line-height: 1.6;

            font-style: italic;

            opacity: 0;

            animation:
                fadeUp 1.2s ease 1.2s forwards;
        }}


        /* Decorative glowing circles */

        .glow {{
            position: absolute;

            border-radius: 50%;

            pointer-events: none;

            filter: blur(2px);
        }}


        .glow-one {{
            width: 320px;
            height: 320px;

            border: 1px solid rgba(124, 58, 237, 0.25);

            animation: orbitOne 6s ease-in-out infinite;
        }}


        .glow-two {{
            width: 500px;
            height: 500px;

            border: 1px solid rgba(6, 182, 212, 0.12);

            animation: orbitTwo 8s ease-in-out infinite;
        }}


        /* Floating particles */

        .particle {{
            position: absolute;

            width: 5px;
            height: 5px;

            border-radius: 50%;

            background: rgba(139, 92, 246, 0.6);
        }}


        .particle-1 {{
            left: 15%;
            top: 25%;

            animation: float1 5s infinite ease-in-out;
        }}


        .particle-2 {{
            right: 18%;
            top: 30%;

            animation: float2 6s infinite ease-in-out;
        }}


        .particle-3 {{
            left: 25%;
            bottom: 20%;

            animation: float1 7s infinite ease-in-out;
        }}


        .particle-4 {{
            right: 25%;
            bottom: 20%;

            animation: float2 5s infinite ease-in-out;
        }}


        /* ====================================================
           ANIMATIONS
        ==================================================== */


        @keyframes fadeDown {{

            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}

            to {{
                opacity: 0.8;
                transform: translateY(0);
            }}

        }}


        @keyframes titleAppear {{

            from {{
                opacity: 0;
                transform: scale(0.85);
            }}

            to {{
                opacity: 1;
                transform: scale(1);
            }}

        }}


        @keyframes fadeUp {{

            from {{
                opacity: 0;
                transform: translateY(25px);
            }}

            to {{
                opacity: 0.75;
                transform: translateY(0);
            }}

        }}


        @keyframes titleFloat {{

            0%, 100% {{
                transform: translateY(0);
            }}

            50% {{
                transform: translateY(-8px);
            }}

        }}


        @keyframes gradientMove {{

            0% {{
                background-position: 0% 50%;
            }}

            50% {{
                background-position: 100% 50%;
            }}

            100% {{
                background-position: 0% 50%;
            }}

        }}


        @keyframes orbitOne {{

            0%, 100% {{
                transform: scale(0.8);
                opacity: 0.2;
            }}

            50% {{
                transform: scale(1.15);
                opacity: 0.5;
            }}

        }}


        @keyframes orbitTwo {{

            0%, 100% {{
                transform: scale(0.9);
                opacity: 0.1;
            }}

            50% {{
                transform: scale(1.08);
                opacity: 0.25;
            }}

        }}


        @keyframes float1 {{

            0%, 100% {{
                transform: translateY(0);
            }}

            50% {{
                transform: translateY(-30px);
            }}

        }}


        @keyframes float2 {{

            0%, 100% {{
                transform: translateY(0);
            }}

            50% {{
                transform: translateY(25px);
            }}

        }}

    </style>


    <div class="welcome-wrapper">

        <div class="glow glow-one"></div>

        <div class="glow glow-two"></div>


        <div class="particle particle-1"></div>

        <div class="particle particle-2"></div>

        <div class="particle particle-3"></div>

        <div class="particle particle-4"></div>


        <div class="welcome-small">
            ✨ WELCOME TO
        </div>


        <div class="welcome-title">
            STUDYBUDDY
        </div>


        <div class="welcome-subtitle">
            Your AI-powered study companion 🤖
        </div>


        <div class="welcome-quote">
            “{st.session_state.welcome_quote}”
        </div>

    </div>
    """

    # IMPORTANT:
    # Use st.html instead of st.markdown
    st.html(welcome_html)


    # ========================================================
    # START BUTTON
    # ========================================================

    col1, col2, col3 = st.columns(
        [1, 1, 1]
    )

    with col2:

        if st.button(
            "🚀  Start Studying",
            use_container_width=True
        ):

            st.session_state.welcome_shown = True

            st.rerun()


    st.markdown(
        """
        <div style="
            text-align:center;
            opacity:0.65;
            font-size:14px;
            margin-top:12px;
        ">
            Learn smarter • Stay consistent • Achieve more
        </div>
        """,
        unsafe_allow_html=True
    )


    # Stop the rest of the app
    st.stop()
    # ========================================================
    # RANDOM QUOTE
    # ========================================================

    st.markdown(
        f"""
        <div class="welcome-quote">
            “{st.session_state.welcome_quote}”
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # START BUTTON
    # ========================================================

    col1, col2, col3 = st.columns(
        [1, 1, 1]
    )

    with col2:

        if st.button(
            "🚀  Start Studying",
            use_container_width=True
        ):

            st.session_state.welcome_shown = True

            st.rerun()


    st.markdown(
        """
        <div class="start-text">
            Learn smarter • Stay consistent • Achieve more
        </div>
        """,
        unsafe_allow_html=True
    )


    # VERY IMPORTANT:
    # Stop the rest of the application from displaying
    st.stop()


# ============================================================
# MAIN APPLICATION
# ============================================================

st.title("🤖 StudyBuddy AI")

st.caption(
    "Your AI-powered document study assistant"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📚 StudyBuddy")

    st.divider()

    # Upload section
    st.subheader("📄 Your Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF, DOCX or TXT",
        type=["pdf", "docx", "txt"],
        help="Upload your study material and ask questions about it."
    )

    st.divider()

    # Document information
    if st.session_state.file_name:

        st.success(
            f"📄 {st.session_state.file_name}"
        )

        rag = st.session_state.rag_engine

        if rag:

            st.metric(
                "Searchable Chunks",
                len(rag.chunks)
            )

            st.caption(
                "Questions are answered using "
                "the most relevant sections "
                "of your document."
            )

    else:

        st.info(
            "Upload a document to start "
            "document-based Q&A."
        )

    st.divider()

    # Reset button
    if st.button(
        "🔄 New Study Session",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.rag_engine = None

        st.session_state.file_name = None

        st.rerun()


# ============================================================
# FILE TEXT EXTRACTION
# ============================================================

def extract_pages(file):

    pages = []


    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if file.name.lower().endswith(".pdf"):

        reader = PdfReader(file)

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            try:

                text = page.extract_text()

            except Exception:

                text = None

            if text and text.strip():

                pages.append(
                    (
                        page_number,
                        text
                    )
                )


    # --------------------------------------------------------
    # TXT
    # --------------------------------------------------------

    elif file.name.lower().endswith(".txt"):

        text = file.read().decode(
            "utf-8",
            errors="ignore"
        )

        if text.strip():

            pages.append(
                (
                    1,
                    text
                )
            )


    # --------------------------------------------------------
    # DOCX
    # --------------------------------------------------------

    elif file.name.lower().endswith(".docx"):

        document = Document(file)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

        if text.strip():

            pages.append(
                (
                    1,
                    text
                )
            )


    return pages


# ============================================================
# PROCESS UPLOADED FILE
# ============================================================

if uploaded_file:

    new_file = (
        st.session_state.file_name
        != uploaded_file.name
    )


    if new_file:

        with st.spinner(
            "📖 Reading and indexing your document..."
        ):

            try:

                pages = extract_pages(
                    uploaded_file
                )


                if not pages:

                    st.error(
                        "❌ I couldn't extract text "
                        "from this document."
                    )

                    st.stop()


                # Create RAG engine
                rag = RAGEngine(
                    chunk_size=1200,
                    chunk_overlap=200
                )


                # Build searchable index
                rag.build_index(
                    pages
                )


                # Save to session
                st.session_state.rag_engine = rag

                st.session_state.file_name = (
                    uploaded_file.name
                )


                # New document = new chat
                st.session_state.messages = []


                st.success(
                    f"✅ {uploaded_file.name} is ready!"
                )


            except Exception as e:

                st.error(
                    f"❌ Could not process file: {e}"
                )

                st.stop()


    # Show document statistics
    rag = st.session_state.rag_engine

    if rag:

        st.info(
            f"📚 **{len(rag.chunks):,} searchable "
            f"chunks** created from your document."
        )


# ============================================================
# WELCOME MESSAGE IN CHAT
# ============================================================

if (
    not st.session_state.messages
    and st.session_state.rag_engine
):

    st.markdown(
        """
        ### 👋 Your document is ready!

        Ask me anything about your uploaded
        study material.

        **Try asking:**

        - Explain this topic in simple language.
        - Give me important points for the exam.
        - Explain this with an example.
        - What are the differences between these concepts?
        - Create 5 questions from this topic.
        """
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a question..."
)


if question:


    # ========================================================
    # USER MESSAGE
    # ========================================================

    with st.chat_message("user"):

        st.markdown(
            question
        )


    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ========================================================
    # DOCUMENT MODE
    # ========================================================

    rag = st.session_state.rag_engine


    if rag:

        # ----------------------------------------------------
        # RETRIEVAL
        # ----------------------------------------------------

        with st.spinner(
            "🔎 Searching your document..."
        ):

            results = rag.retrieve(
                question,
                top_k=5
            )


        # ----------------------------------------------------
        # No relevant chunks
        # ----------------------------------------------------

        if not results:

            answer = (
                "I couldn't find relevant information "
                "for this question in the uploaded document."
            )


            with st.chat_message(
                "assistant"
            ):

                st.warning(
                    answer
                )


        else:

            # ------------------------------------------------
            # Build context from retrieved chunks
            # ------------------------------------------------

            context_parts = []


            for result in results:

                context_parts.append(
                    f"""
[Page {result['page']}]

{result['text']}
"""
                )


            context = "\n".join(
                context_parts
            )


            # ------------------------------------------------
            # GROQ PROMPT
            # ------------------------------------------------

            prompt = f"""
You are StudyBuddy AI, an AI study
assistant that answers questions using
uploaded study material.

Use ONLY the document sections provided
below to answer the user's question.

IMPORTANT RULES:

1. Do not invent information.

2. If the answer is not supported by
the provided document sections, say:

"I couldn't find this information
in the uploaded document."

3. Explain concepts in simple,
student-friendly language.

4. If appropriate, use examples.

5. For exam-related questions,
structure the answer clearly.

6. Mention the relevant page number
when possible.

DOCUMENT SECTIONS
=================

{context}

=================

USER QUESTION
=============

{question}
"""


            # ------------------------------------------------
            # ASK GROQ
            # ------------------------------------------------

            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "🤖 StudyBuddy is thinking..."
                ):

                    try:

                        answer = ask_groq(
                            prompt
                        )


                        st.markdown(
                            answer
                        )


                        # ------------------------------------
                        # SOURCES
                        # ------------------------------------

                        with st.expander(
                            "📖 View document sources"
                        ):

                            for index, result in enumerate(
                                results,
                                start=1
                            ):

                                st.markdown(
                                    f"""
**Source {index} — Page {result['page']}**

{result['text'][:600]}...
"""
                                )


                    except Exception as e:

                        answer = (
                            f"❌ Groq error: {str(e)}"
                        )

                        st.error(
                            answer
                        )


        # Save answer
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    # ========================================================
    # NORMAL CHAT MODE
    # ========================================================

    else:

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🤖 StudyBuddy is thinking..."
            ):

                try:

                    answer = ask_groq(
                        question
                    )

                    st.markdown(
                        answer
                    )


                except Exception as e:

                    answer = (
                        f"❌ Groq error: {str(e)}"
                    )

                    st.error(
                        answer
                    )


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )