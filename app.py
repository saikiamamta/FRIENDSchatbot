import os
import streamlit as st
from dotenv import load_dotenv
from chatbot import get_openai_client, get_response

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

st.set_page_config(
    page_title="Friends Chatbot",
    page_icon="☕",
    layout="centered",
)

# Custom CSS for Friends theming
st.markdown("""
<style>
    .stApp {
        background-color: #FFF8F0;
    }
    .friends-header {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .friends-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #7B68AE;
        letter-spacing: 0.15em;
        margin-bottom: 0;
    }
    .friends-subtitle {
        font-size: 1rem;
        color: #A0522D;
        margin-top: 0.25rem;
    }
    [data-testid="stSidebar"] {
        background-color: #F3EDE4;
    }
    .characters-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        padding: 1rem 0;
    }
    .char-card {
        border-radius: 16px;
        padding: 1.2rem 0.8rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        cursor: default;
    }
    .char-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.18);
    }
    .char-avatar {
        font-size: 3.5rem;
        line-height: 1;
        margin-bottom: 0.4rem;
    }
    .char-name {
        font-weight: 800;
        font-size: 1.05rem;
        margin-bottom: 0.15rem;
    }
    .char-actor {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-bottom: 0.4rem;
    }
    .char-quote {
        font-size: 0.8rem;
        font-style: italic;
        opacity: 0.85;
    }
    .char-ross   { background: linear-gradient(135deg, #E8F5E9, #C8E6C9); color: #2E7D32; }
    .char-rachel { background: linear-gradient(135deg, #FCE4EC, #F8BBD0); color: #AD1457; }
    .char-monica { background: linear-gradient(135deg, #E3F2FD, #BBDEFB); color: #1565C0; }
    .char-chandler { background: linear-gradient(135deg, #FFF3E0, #FFE0B2); color: #E65100; }
    .char-joey   { background: linear-gradient(135deg, #F3E5F5, #E1BEE7); color: #6A1B9A; }
    .char-phoebe { background: linear-gradient(135deg, #FFFDE7, #FFF9C4); color: #F57F17; }
    .landing-tagline {
        text-align: center;
        font-size: 1.1rem;
        color: #7B68AE;
        margin: 0.5rem 0 0.2rem 0;
    }
    .landing-hint {
        text-align: center;
        font-size: 0.9rem;
        color: #A0522D;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="friends-header">
    <div class="friends-title">F·R·I·E·N·D·S</div>
    <div class="friends-subtitle">☕ The One Where You Ask Anything ☕</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.markdown("### About")
    st.markdown(
        "Your ultimate **Friends** TV series companion! "
        "Ask me anything — trivia, character analysis, fan theories, "
        "behind-the-scenes facts, or just chat about your favorite episodes."
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**Try asking...**")
    example_prompts = [
        "Why did Ross say Rachel's name at the altar?",
        "What's the story behind Smelly Cat?",
        "Were Ross and Rachel really on a break?",
        "Tell me about the apartment number change",
        "Compare Chandler and Joey's friendship to Ross and Rachel's romance",
    ]
    for prompt in example_prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    try:
        st.session_state.client = get_openai_client()
    except ValueError as e:
        st.error(str(e))
        st.stop()

# Landing page with character caricatures (shown only when chat is empty)
if not st.session_state.messages:
    st.markdown("""
    <div class="characters-grid">
        <div class="char-card char-ross">
            <div class="char-avatar">🦖</div>
            <div class="char-name">Ross Geller</div>
            <div class="char-actor">David Schwimmer</div>
            <div class="char-quote">"We were on a BREAK!"</div>
        </div>
        <div class="char-card char-rachel">
            <div class="char-avatar">👗</div>
            <div class="char-name">Rachel Green</div>
            <div class="char-actor">Jennifer Aniston</div>
            <div class="char-quote">"It's like all my life everyone's told me, 'You're a shoe!'"</div>
        </div>
        <div class="char-card char-monica">
            <div class="char-avatar">👩‍🍳</div>
            <div class="char-name">Monica Geller</div>
            <div class="char-actor">Courteney Cox</div>
            <div class="char-quote">"I KNOW!"</div>
        </div>
        <div class="char-card char-chandler">
            <div class="char-avatar">🃏</div>
            <div class="char-name">Chandler Bing</div>
            <div class="char-actor">Matthew Perry</div>
            <div class="char-quote">"Could this BE any more awkward?"</div>
        </div>
        <div class="char-card char-joey">
            <div class="char-avatar">🍕</div>
            <div class="char-name">Joey Tribbiani</div>
            <div class="char-actor">Matt LeBlanc</div>
            <div class="char-quote">"How you doin'?"</div>
        </div>
        <div class="char-card char-phoebe">
            <div class="char-avatar">🎸</div>
            <div class="char-name">Phoebe Buffay</div>
            <div class="char-actor">Lisa Kudrow</div>
            <div class="char-quote">"Smelly cat, smelly cat, what are they feeding you?"</div>
        </div>
    </div>
    <div class="landing-tagline">🛋️ Your favorite six are here. Ask them anything!</div>
    <div class="landing-hint">Type a question below to start chatting...</div>
    """, unsafe_allow_html=True)

# Display conversation history
for message in st.session_state.messages:
    avatar = "☕" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Check if the last message needs a response (from sidebar button click)
needs_response = (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
    and (len(st.session_state.messages) < 2 or st.session_state.messages[-2]["role"] != "assistant"
         or st.session_state.messages[-1] != st.session_state.messages[-2])
)

# Handle new user input from chat box
user_input = st.chat_input("Ask me anything about Friends! ☕")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    needs_response = True

# Generate response if needed
if needs_response and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="☕"):
        with st.spinner("Thinking..."):
            response = get_response(
                st.session_state.client,
                st.session_state.messages,
            )
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
