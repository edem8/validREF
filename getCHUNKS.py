from langchain.text_splitter import CharacterTextSplitter

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len
    )

    chunks =  text_splitter.split_text(raw_text)
    return chunks