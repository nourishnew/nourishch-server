from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

from pinecone import Pinecone
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set up environment variables (replace these with your actual keys)


@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    query = data.get('query')
    print("query is")
    print(query)
    index_name= "nourishch"
    model_name = 'text-embedding-ada-002'
    print(os.environ["OPENAI_API_KEY"])
    print(os.environ["PINECONE_API_KEY"])
    print("heloooooooooooooooooooooooooooooooooo")
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    
    llm = ChatOpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-3.5-turbo",
        temperature=0.0
    )

    # Initialize a LangChain object for retrieving information from Pinecone.
    knowledge = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    )

    # Initialize a LangChain object for chatting with the LLM
    # with knowledge from Pinecone. 
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=knowledge.as_retriever()
    )
    return jsonify({'answer': qa.invoke(query).get("result")})

if __name__ == '__main__':
    app.run(debug=True,port=5001)