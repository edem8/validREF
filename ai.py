import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain


style_guides = {
    "MLA 9th edition": """
        MLA style guide/

        One Author    /
        Format: (Author's Last Name Page Number)/

        Example: (Hunt 358) /

        Two Authors /
        Format: (Author's Last Name and Author's Last Name Page Number) /

        Example: (Case and Daristotle 57) /

        Three or More Authors /
        Format:  (Author's Last Name et al. Page Number) /

        Example: (Case et al. 57) /

        Unknown Author /
        Where you would normally put the author's last name, instead use the first one, two, or three words from the title. Do not use initial articles such as "A", "An" or "The". Provide enough words to clarify which sources from your works-cited list that you are referencing.  /

        Follow the formatting of the title. For example, if the title in the works-cited list is in italics, italicize the words from the title in the in-text citation, and if the title in the works-cited list is in quotation marks, put quotation marks around the words from the title in the in-text citation. /

        Format: (Title Page Number) /

        Examples: /

        (Cell Biology 12) /

        ("Nursing" 12) /

        Multiple Sources
        To cite more than one source when you are paraphrasing, separate the in-text citations with a semi-colon. /

        Format: (Author's Last Name Page Number; Author's Last Name Page Number). / 

        Examples: /

        (Smith 42; Bennett 71).  /

        (It Takes Two; Brock 43). /

        Note: In MLA style, the sources within the in-text citation do not need to be in alphabetical order.
    """,
    "APA 7th edition": """
        APA style guide /
    
        1. One Author /

        Parenthetical Citation: (Author's Last Name, Year) /
        Example: (Case, 2011)/
        Narrative Citation: Author's Last Name (Year)/
        Example: Case (2011)/
        
        2. Two Authors /

        Parenthetical Citation: (First Author's Last Name & Second Author's Last Name, Year) /
        Example: (Case & Daristotle, 2011) /
        Narrative Citation: First Author's Last Name and Second Author's Last Name (Year) /
        Example: Case and Daristotle (2011) /

        3. Three or More Authors /


        Parenthetical Citation: (First Author's Last Name et al., Year) /
        Example: (Case et al., 2011) /
        Narrative Citation: First Author's Last Name et al. (Year) /
        Example: Case et al. (2011) /

        4. Group Author with Abbreviation /

        First Citation: /
        Parenthetical Citation: (Full Name of Group Author [Abbreviation], Year) /
        Example: (World Health Organization [WHO], 2020) /
        Narrative Citation: Full Name of Group Author (Abbreviation, Year) /
        Example: World Health Organization (WHO, 2020) /
        Subsequent Citations: /
        Parenthetical Citation: (Abbreviation, Year) /
        Example: (WHO, 2020) /
        Narrative Citation: Abbreviation (Year) /
        Example: WHO (2020) /
        
        5. Group Author Without Abbreviation /

        Parenthetical Citation: (Full Name of Group Author, Year) /
        Example: (Yale University, 2020) /
        Narrative Citation: Full Name of Group Author (Year) /
        Example: Yale University (2020) /
        
        6. In-Text Citation for More than One Source /

        Parenthetical Citation: Separate multiple citations with a semi-colon. List sources alphabetically by author's last name or the first word of the title if no author is given. /
        Example: (Jones, 2015; Smith, 2014) /
        Example: (Beckworth, 2016; "Nursing," 2015) /
        Narrative Citation: Separate multiple citations with a comma and "and" before the last citation. List sources alphabetically by author's last name or the first word of the title if no author is given. /
        Example: Jones (2015), Smith (2014) /
        Example: Beckworth (2016) and "Nursing" (2015)

    """,
}


def ai(citations, style):

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4",
        max_tokens=200,
    )

    def create_prompt(style):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f'say "match" if user input matches precisely the {style} in-text citation style and "no-match" otherwise. Refer to {style_guides[style]}',
                ),
                ("user", "{input}"),
            ]
        )

    prompt = create_prompt(style)
    chain = prompt | llm | StrOutputParser()

    matches = []
    unmatches = []
    for citation in citations:
        response = chain.invoke({"input": citation})
        if response == "match":
            matches.append(citation)
        else:
            unmatches.append(citation)

    corrected = []
    if unmatches:
        corrected = correct(unmatches, llm, style)

    return matches, unmatches, corrected


def correct(unmatches, llm, style):
    def create_correct_prompt(style):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"correct the following citation according to {style} in-text citation style. Refer to {style_guides[style]}",
                ),
                ("user", "{input}"),
            ]
        )

    prompt = create_correct_prompt(style)
    chain = prompt | llm | StrOutputParser()

    corrected = []
    for citation in unmatches:
        corrected_citation = chain.invoke({"input": citation})
        corrected.append(corrected_citation)

    return corrected
