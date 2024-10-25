import os
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
import openai
from langchain.schema import HumanMessage
from langchain.chat_models import ChatOpenAI


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PyPDF2.PdfReader(pdf)
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


def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message


def get_vectorstore(text_chunks, persist_dir="faiss_index"):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceEmbeddings()

    # Check if the vectorstore already exists
    if os.path.exists(persist_dir):
        # Load existing vectorstore from disk
        vectorstore = FAISS.load_local(persist_dir, embeddings=embeddings)

        # Add new embeddings to the existing vectorstore
        vectorstore.add_texts(text_chunks)
    else:
        # Create new vectorstore and save it
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    
    # Save the updated or new vectorstore to disk
    vectorstore.save_local(persist_dir)
    
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def get_conversation_chain_no_pdf():
    return ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.0)


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def handle_userinput_no_pdf(user_question):
    OpenAIGPT4 = get_conversation_chain_no_pdf()
    response = OpenAIGPT4.invoke(([HumanMessage(content=user_question)]))
    st.session_state.chat_history = response

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with your personal PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)
    else:
        st.write("Please upload a pdf.")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click 'Start'", accept_multiple_files=True)
        if st.button("Start"):
            with st.spinner("Starting..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
        else:
            st.session_state.conversation = get_conversation_chain_no_pdf()


if __name__ == '__main__':
    main()
