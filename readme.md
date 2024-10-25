## Guide
-----
**ChatBot PDF Local**

A ChatBot application that allows you to upload PDF documents and query their content for insights, summaries, or specific information. This guide covers the steps required to get the project running locally and tips for effective usage.


## 🚀 Features
 **PDF Document Upload**: Load your own documents to ask questions directly about their content.
 **Conversational Interaction**: Interact with your documents as if you're chatting with them, using natural language queries.


## Dependencies and Installation
-----
Follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

3. Obtain an API key from OpenAI and add it to the `.env.example` (remove the 'example' from file name) file in the project directory.
```commandline
OPENAI_API_KEY=your_openai_api_key
```

## Usage
-----
Follow these steps:

1. Start the Streamlit Application. Run this from your terminal:
   ```
   streamlit run app.py
   ```

2. Upload Your Documents: Open the application in your web browser, and use the interface to upload your PDF documents.

3. Ask Questions: Enter questions about the document in the provided chat area, and receive responses directly related to the uploaded content.


-----
## 📑 Example Queries
Here are some example questions to ask your documents:

Basic Summary: "Can you summarize the key points of this document?"
Specific Information: "What are the details mentioned in Section 3?"
Contextual Questions: "What is the author’s main argument in this document?"


-----
## 📝 Notes
Document Size: For best performance, ensure your document isn't excessively large, as very large PDFs may take longer to process.
Supported Formats: The app currently supports PDF files only.
Limitations: Responses depend on the quality of the uploaded document and the context provided in your query.