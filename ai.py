import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain


def ai(citations):

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4",
        max_tokens=200,
    )


    
    apa_style = """
            APA Parenthetic format: /
            1. (Mintah, 2020) or (Mintah, 2015, p. 2) for one author/
            2. (Obeng & Anthony, 2013) or (Obeng & Anthony, 2010, pp. 112-113). for two authors/
            3. (Appah et al., 2016) or (Appah et al., 2001, para. 5). for three+ authors/

            APA Narrative format: /
            1. Allan, (2020) /
            2. Obeng and Anthony, (2013) /
            3. Appah et al., (2016) /

            APA multiple citings(must be aplhabetical order for Parenthetic format): /
            1. (Evans & McLeod, 2017; Gallant, 2014; Ryan et al., 2019) /

            APA multiple citings(can be any order for Narrative format): /
            1. McConomy (2015), Ternes (2010), and Guenther (2018)  /

            APA missing information (Parenthetic format): /
            1. (Smith, n.d.)
            
            """

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f'say "match" if user input matches precisely an APA 7th edition in-text citation style and "no-match" otherwise. Refer to {apa_style}',
            ),
            ("user", "{input}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    matches = []
    unmatches = []
    for citation in citations:
        response = chain.invoke({"input": citation})

        if response == "match":
            matches.append(citation)
        else:
            unmatches.append(citation)

    return matches, unmatches
