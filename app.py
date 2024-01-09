import getPDF
import getCHUNKS
import getVECTORSDB
import streamlit as st
from dotenv import load_dotenv



def main():
    load_dotenv()
    st.set_page_config(page_title="Citation Validator", page_icon=":books:")

    st.header("Verify cited sources :books:")

    with st.sidebar:
        st.subheader("Verify Citations")
        pdf_docs = st.file_uploader("Upload your research paper", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner('Processing'):
                
                raw_text = getPDF.get_pdf_text(pdf_docs)
                chunks = getCHUNKS.get_text_chunks(raw_text)
               # vectorstore = getVECTORSDB.get_vector_store(chunks)


if __name__ == "__main__":
    main()
