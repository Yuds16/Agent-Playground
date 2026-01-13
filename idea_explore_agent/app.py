import streamlit as st
import asyncio
from agent import root_agent

# Set up the page
st.set_page_config(page_title="Idea Explore Agent", page_icon="🤖")
st.title("Idea Explore Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to explore?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get agent response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Run the agent (sync wrapper for async call if needed, or direct if synchronous)
        # ADK agents are typically synchronous or have a run method. 
        # Checking agent.py, it imports Agent from google.adk.agents.llm_agent
        # Assuming we can just call agent.run(prompt) or similar.
        
        # Since I don't see the exact signature of Agent in the file, 
        # I'll assume standard ADK usage: response = agent.run(prompt)
        # But wait, looking at agent.py, it's just 'from google.adk.agents.llm_agent import Agent'
        # I'll assume synchronous run for now based on standard ADK patterns, or handle async if it returns a coroutine.
        
        try:
            # Create a simple wrapper to capture output if adk prints to stdout/logs 
            # (though adk usually returns a response object).
            response = root_agent.run(prompt)
            
            # If response is an object, try to extract text. 
            # If it's a string, just use it.
            if hasattr(response, 'text'):
                full_response = response.text
            else:
                full_response = str(response)
                
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"Error: {str(e)}"
            message_placeholder.error(full_response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
