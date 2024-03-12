import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from IPython.display import display
from IPython.display import Markdown
from langchain.prompts import PromptTemplate
import textwrap



def main():

    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    chain = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

    def to_markdown(text):
        text = text.replace(".", " *")
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

    prompt_template = """ Answer the question as  precise as possible using the provided context.
                    If the answer is not in the context, say "answer not available in context" \n\n
                    Context: \n {context}? \n
                    Question: \n {question} \n
                    Answer: 
                    """
    prompt = Prompt_template()

    result = chain.invoke("what is a mixture?")
    print (result.content)




if __name__ == "__main__":

    main()
