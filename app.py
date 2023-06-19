import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from extrcomb import scrape
from loginlogic import login

def get_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            bot_message = message.content
            if "sorry" in bot_message.lower() or "no relevant data" in bot_message.lower():
                google_search_link = '<a href="https://www.google.com/search?q={}">Search on Google</a>'.format(user_question)
                bot_message = bot_message + "<br>" + google_search_link
            st.write(bot_template.replace("{{MSG}}", bot_message), unsafe_allow_html=True)

def login_page():
    st.markdown(
        """
        <style>
        body {
            background-color: #FFFFFF;  /* Set a different background color */
        }
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }

        .logo {
            width: 200px;  /* Adjust the image width */
            margin-bottom: 20px;
        }

        .title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;  /* Adjust the title color */
        }

        .input {
            width: 300px;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        .button {
            width: 150px;
            padding: 10px;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        .button:hover {
            background-color: #45a049;
        }

        .error {
            color: red;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    logo_image = Image.open('/home/alen/Desktop/llm_model/static/kerala-technological-university-ktu-3-638.jpg')  # Replace with the path to your logo image
    st.image(logo_image, caption="", width=200)


    st.markdown('<h1 class="title">Welcome to the KTU Chatbot</h1>', unsafe_allow_html=True)

    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login", key="login"):
        if login(username, password):
            # Set the login flag to True
            st.session_state.login_status = True
            st.success("Login successful!")
        else:
            st.error("Invalid password")

    st.markdown("Don't have an account? Sign up below.")
    if st.button("Sign up", key="signup"):
        # Add the signup logic here
        st.write("Sign up clicked!")


def chat_page():
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chat with AsKmE Chatbot :books:")
    user_question = st.text_input("Ask a question about KTU notifications:")
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        pdf_path = "/home/alen/Desktop/llm_model/notification_data/notification.pdf"
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_path)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)

        st.subheader("Latest Notification")
        latest_notification = get_pdf_text("/home/alen/Desktop/mini_project_19-06-23/announcements.pdf")
        if st.button("Refresh"):
            latest_notification = scrape()
        st.write(latest_notification)


def main():
    load_dotenv()  # Load environment variables from .env file

    # Initialize the login flag using Streamlit's SessionState
    if "login_status" not in st.session_state:
        st.session_state.login_status = False

    st.set_page_config(page_title="Login and Chat Example")

    if not st.session_state.login_status:
        login_page()
    else:
        chat_page()

if __name__ == '__main__':
    main()
