# TalentScout

## Overview:
This project is a Streamlit-based HR screening chatbot that leverages Groq's AI models to conduct interview-like interactions with candidates. The chatbot collects responses from users, generates personalized replies, and extracts relevant information from these interactions. The primary goal is to automate the early stages of hiring by capturing personal and professional details in a structured format.

## Key Features:
- **Conversation Flow**: The chatbot starts by asking for basic information like full name, email, phone number, years of experience, desired position, and tech stack. It continues with follow-up questions, concluding with a thank-you message.
- **Response Generation**: Powered by Groq's conversational AI model (`llama3-70b-8192`), the chatbot responds with relevant and contextually appropriate replies.
- **Typing Effect**: To engage users, the chatbot uses a typing effect that simulates natural conversation.
- **Data Extraction**: From the conversation transcript, the chatbot extracts specific personal information using Groq’s text analysis. This information is then parsed into JSON format.
- **File Handling**: The chatbot saves the entire conversation as a `.txt` file and also extracts the first chunk to save as a `.json` file containing the structured data.
- **User Interaction**: Users input their responses, and the chatbot processes these interactions, appending messages to the conversation history for future analysis.

## Installation & Setup:
To run this project, you need:
1. **Streamlit**: Install Streamlit using `pip install streamlit`.
2. **Groq API**: Make sure you have an active API key from Groq.
3. **Python**: Python 3.6+ is required.

## How It Works:
### 1. Chat Interface:
- The chatbot starts with a welcome message and instructs users to say "Hi" to initiate interaction.
- It captures user inputs, generates AI-driven responses, and stores chat history in a session state.

### 2. Response Generation:
- The chatbot communicates with Groq’s AI model to generate responses. These responses are tailored to follow up on the user’s previous interactions.

### 3. Typing Effect:
- To simulate a natural conversation flow, a typing effect is added to each message before it is displayed.

### 4. Transcript Handling:
- All user and assistant messages are saved as a `.txt` file for later reference.
- The first 2000 characters of the transcript are extracted and processed to extract relevant personal information (e.g., full name, email, phone number, etc.).

### 5. JSON Extraction:
- Using Groq’s chat completion API, the first chunk of the transcript is analyzed to extract personal details in JSON format.
- If personal information is found, it’s saved into a `.json` file, which can be downloaded for further review.

### 6. Save and Analysis:
- After each interaction, the conversation history is saved to a text file.
- The first chunk of the transcript is extracted and processed to extract personal information using Groq.
- The extracted information is printed, formatted, and saved as a `.json` file for future use.

## Features:
- **Automatic Save**: Conversations and extracted information are automatically saved to files.
- **Typing Simulation**: Messages appear with a realistic typing effect to enhance user engagement.
- **Structured JSON Output**: Extracted personal details from the conversation are formatted into a structured JSON for easy parsing.

## Example Workflow:
1. A user interacts with the chatbot by answering questions about their personal and professional details.
2. The chatbot processes these responses using Groq's AI model to generate responses.
3. It saves the entire conversation as a `.txt` file and extracts personal information from the first chunk of the chat.
4. This extracted information is printed and saved as a `.json` file for future use.

## Prerequisites:
- **Groq API Key**: Ensure you have an API key from Groq to connect and send requests to the conversational model.
- **Environment Setup**: Make sure Streamlit is installed and that you have access to the required dependencies (Groq Python library, etc.).

## How to Run:
1. Clone this repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Set up your Groq API key in the environment variables (`os.environ['GROQ_API_KEY']`).
4. Run the Streamlit app with `streamlit run app.py`.

## Notes:
- The chatbot is designed to handle multiple interactions, continuously saving conversation history and performing analyses.
- The personal information extraction uses Groq's text analysis capabilities to ensure reliable extraction from the conversation.
- Proper error handling is included to manage cases where JSON extraction might fail.

## Contact:
For any queries or support, feel free to reach out to me
