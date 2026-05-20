from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import streamlit as st
import os

# Disable prompt caching — fixes Groq compatibility
os.environ["CREWAI_DISABLE_PROMPT_CACHING"] = "true"

load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Content Crew",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Sora', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
        color: #ffffff;
    }
    
    .hero {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }
    
    .hero h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero p {
        color: #888;
        font-size: 1rem;
        font-weight: 300;
    }

    .agent-card {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        
    }

    .article-box {
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
    }

    div[data-testid="stTextInput"] input {
        background: #1a1a2e !important;
        border: 1px solid #2a2a4a !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2) !important;
    }

    div[data-testid="stButton"] button {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    .stMarkdown h2 {
        color: #00d4ff !important;
        border-bottom: 1px solid #2a2a4a;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# LLM
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>🤖 AI Content Creation Crew</h1>
    <p>Three specialized AI agents working together to create polished articles</p>
</div>
""", unsafe_allow_html=True)

# Show agent cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="agent-card">
        <h4>🔍 Researcher</h4>
        <p style="color:#888; font-size:0.85rem">Finds comprehensive information and key facts</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h4>✍️ Writer</h4>
        <p style="color:#888; font-size:0.85rem">Transforms research into engaging articles</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <h4>✏️ Editor</h4>
        <p style="color:#888; font-size:0.85rem">Polishes and perfects the final content</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Input
topic = st.text_input("", placeholder="Enter any topic e.g. AI agents, quantum computing...")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_btn = st.button("Generate Article")

if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic first!")
    else:
        # Agents
        researcher = Agent(
            role="Senior Research Analyst",
            goal="Find comprehensive and accurate information about the given topic",
            backstory="""You are an expert researcher with 10 years of experience.
            You find accurate, relevant and up to date information.
            You always provide well structured research notes.""",
            llm=llm,
            verbose=False
        )

        writer = Agent(
            role="Content Writer",
            goal="Write engaging and informative articles based on research",
            backstory="""You are a skilled content writer who transforms research
            into clear, engaging articles. You write in a professional yet
            conversational tone that is easy to understand.""",
            llm=llm,
            verbose=False
        )

        editor = Agent(
            role="Senior Editor",
            goal="Review and improve articles for clarity, accuracy and quality",
            backstory="""You are a meticulous editor with an eye for detail.
            You improve structure, fix inconsistencies and ensure the article
            is polished and professional.""",
            llm=llm,
            verbose=False
        )

        # Tasks
        research_task = Task(
            description=f"""Research the following topic thoroughly: {topic}
            Find key information, latest developments, important facts and examples.
            Provide well structured research notes.""",
            expected_output="""Detailed research notes with:
            - Key facts and information
            - Latest developments
            - Important examples
            - Relevant statistics if available""",
            agent=researcher
        )

        write_task = Task(
            description="""Using the research provided, write a comprehensive article.
            Make it engaging, informative and easy to understand.
            Structure it with clear sections and headings.""",
            expected_output="""A well written article with:
            - Engaging introduction
            - Clear sections with headings
            - Informative content
            - Strong conclusion""",
            agent=writer
        )

        edit_task = Task(
            description="""Review and improve the written article.
            Fix any issues with clarity, structure or accuracy.
            Make it polished and professional.""",
            expected_output="""A polished final article that is:
            - Clear and well structured
            - Professional and engaging
            - Free of errors
            - Ready to publish""",
            agent=editor
        )

        # Crew
        crew = Crew(
            agents=[researcher, writer, editor],
            tasks=[research_task, write_task, edit_task],
            verbose=False
        )

        # Run with status
        with st.status("🤖 Crew working on your article...", expanded=True) as status:
            st.write("🔍 Researcher gathering information...")
            st.write("✍️ Writer creating article...")
            st.write("✏️ Editor polishing content...")
            
            result = crew.kickoff()
            
            status.update(label="✅ Article ready!", state="complete")

        # Display result
        st.markdown('<div class="article-box">', unsafe_allow_html=True)
        st.markdown(f"### 📄 Article: {topic}")
        st.divider()
        st.markdown(str(result))
        st.markdown('</div>', unsafe_allow_html=True)