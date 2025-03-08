# Course: CSC525
# Sean Bohuslavsky

# Import the necessary libraries
import streamlit as st
import nlp

# Set the title and caption
st.title('StatChat')
st.caption('\U0001F3C0 A NBA Statistical Chatbot')

# Set the sidebar
st.sidebar.title('About StatChat')
info = st.sidebar.tabs(['Info'])
st.sidebar.write('StatChat is a chatbot that can answer questions about NBA statistics for the current NBA season. StatChat will provide you with the requested information in real-time.')
st.sidebar.subheader("Supported Statistics")
st.sidebar.write("The following statistics are supported by StatChat:")
st.sidebar.write("- Points (P/T)")
st.sidebar.write("- Rebounds (P/T)")
st.sidebar.write("- Assists (P/T)")
st.sidebar.write("- Steals (P/T)")
st.sidebar.write("- Blocks (P/T)")
st.sidebar.write("- Turnovers (P/T)")
st.sidebar.write("- Field Goals Made/Attempted/Percentage (P/T)")
st.sidebar.write("- Three Point Made/Attempted/Percentage (P/T)")
st.sidebar.write("- Free Throw Made/Attempted/Percentage (P/T)")
st.sidebar.write("- Offensive/Defensive Rebounds (P/T)")
st.sidebar.write("- Wins (T)")
st.sidebar.write("- Losses (T)")
st.sidebar.write("- Win Percentage (T)")

# Set the chatbot
if "messages" not in st.session_state:
    sug1, sug2, sug3 = nlp.get_sugges()
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I am StatChat. Ask me anything about NBA statistics for the current NBA season!\n\n Here are some example questions I can answer: \n\n {} \n\n {} \n\n {}".format(sug1, sug2, sug3)}]

# Chatbot
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input():
    
    # Get user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Send user input to NLP and get response
    response = nlp.proc(prompt)
    
    # Send response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)