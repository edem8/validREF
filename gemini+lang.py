import urllib
from dotenv import load_dotenv
import warnings
import os
from pathlib import Path as p
from pprint import pprint

from getPDF import get_pdf
import pandas as pd
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma




def main():
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = ChatGoogleGenerativeAI(model="gemini-pro", t_emperature=0)

    pdf_path = "Data/citations&NER.pdf"
    pages = get_pdf(pdf_path)
    

    prompt_template = """Answer the question as precise as possible using the provided context. If the answer is
                    not contained in the context, say "answer not available in context" \n\n
                    Context: \n {context}?\n
                    Question: \n {question} \n
                    Answer:
                  """

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    stuff_chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
  #  question = "What are the REFERENCES made in this article?. Provide a list in the order of which they appear"
   # question = "Which REFERENCES in this article do not contain a DOI number?. Provide a list in the order of which they appear"
    question = "Extract the last citation in this article. If it does not have a DOI number, Go to Researchgate attach it's associated DOI number."

    stuff_answer = stuff_chain.invoke(
        {"input_documents": pages[11:], "question": question}, return_only_outputs=True
    )

    pprint(stuff_answer)





if __name__=="__main__":
    main()