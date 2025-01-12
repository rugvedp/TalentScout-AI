import os
import time
import streamlit as st
from groq import Groq  
import os
import json

client = Groq(api_key=os.environ['GROQ_API_KEY'])

# Streamlit page configuration
st.set_page_config(page_icon="💬", layout="wide", page_title="HR Screening Chatbot")

# Function to display an emoji icon
def icon(emoji: str):
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

icon("🤖")

st.subheader("TalentScout", divider="rainbow", anchor=False)
st.caption("Start by saying 'Hi' to the bot to begin the conversation.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are an HR assistant called TalentScout who is conducting interviews. Start by asking the user's full name, email address, phone number, years of experience, desired position(s), current location, and tech stack. Then, ask three questions related to tech stack, experience, and conclude with a thank-you message and also add "We'll be in touch soon" in the thank you message. Just straightforward questions. No need to be fancy. Follow-up questions should be based on the user's response of the previous question, also every single question should be asked one after another."""}
    ]

def generate_response(messages):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        max_tokens=8192,
        temperature=0.7,
        n=1,
        stop="We'll be in touch soon"
    )
    return response.choices[0].message.content.strip()

def display_with_typing_effect(placeholder, text, delay=0.01):
    """
    Display text with a typing effect in Streamlit.
    """
    message = ""
    for char in text:
        message += char
        placeholder.markdown(message + "▌")  # Add a cursor effect
        time.sleep(delay)
    placeholder.markdown(message)  # Final text without cursor


def analyze_first_chunk_and_print_json(txt_file, chunk_size=2000):
    """
    Analyze the first chunk of a chat transcript using Groq to extract personal information 
    and print the extracted JSON.
    """
    
    with open(txt_file, "r") as file:
        transcript = file.read()
        
        # Split transcript into chunks of specified size
        first_chunk = transcript[:chunk_size]
        extraction_prompt = f"""
        Analyze the following chat transcript chunk and extract the user's personal information:
        1. Full Name
        2. Email Address
        3. Phone Number
        4. Years of Experience
        5. Desired Position(s)
        6. Current Location
        7. Tech Stack

        Return the extracted information in strict JSON format with keys as follows:
        {{
            "Full Name": "",
            "Email Address": "",
            "Phone Number": "",
            "Years of Experience": "",
            "Desired Position(s)": "",
            "Current Location": "",
            "Tech Stack": ""
        }}

        Just Return the extracted information in JSON format. Do not include any additional text.
        Chat Transcript Chunk:
        {first_chunk}
        """
        # Analyze the first chunk using the LLM (Groq)
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": extraction_prompt}],
            max_tokens=8192,
            temperature=0.7,
            n=1
        )
        
        extracted_info = response.choices[0].message.content.strip()
        print(extracted_info)

        if extracted_info != "":
            print(extracted_info)
            try:
                personal_info = json.loads(extracted_info)
                print(json.dumps(personal_info, indent=4))
                # Save extracted info as JSON file
                file_name = f"extracted_info_{time.strftime('%Y%m%d_%H%M%S')}.json"
                with open(file_name, "w") as json_file:
                    json.dump(personal_info, json_file, indent=4)
                st.success(f"Extracted information saved as {file_name}")
            except json.JSONDecodeError:
                print("Failed to parse the extracted information.")

def save_transcript_to_file():
    """
    Save the chat transcript to a text file.
    """
    transcript = ""
    for message in st.session_state.messages:
        if message["role"] != "system":  # Exclude system messages
            role = "Bot" if message["role"] == "assistant" else "User"
            transcript += f"{role}: {message['content']}\n"

    file_name = f"chat_transcript.txt"
    with open(file_name, "w") as file:
        file.write(transcript)
    

    st.success(f"Chat transcript saved as {file_name}")
    analyze_first_chunk_and_print_json(file_name)

# Display chat messages from history
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👤'
    if message["role"] == "system" and message["content"].startswith("You are an HR assistant"):
        pass
    else:
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# User input
if user_input := st.chat_input("Your response..."):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user", avatar='👤'):
        st.markdown(user_input)

    # Generate assistant response
    assistant_response = generate_response(st.session_state.messages)

    # If the response is empty, save the transcript and stop further processing
    if not assistant_response:
        save_transcript_to_file()
        st.stop()

    # Append assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Display assistant response with typing effect
    with st.chat_message("assistant", avatar='🤖'):
        placeholder = st.empty()  # Create a placeholder for dynamic updates
        display_with_typing_effect(placeholder, assistant_response)

    # Check for stopping phrase
    if "we'll be in touch soon" in assistant_response.lower():
        save_transcript_to_file()
