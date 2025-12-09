from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
import os

# IMPORTANT VARIABLES

# - PARADIS
PDF_PATH_PARADIS = "/workspaces/langchain-aot-war-simulator/Lore/paradis_internal.pdf"
DB_DIR_PARADIS = "./sql_chroma_db/paradis"
MODEL_NAME_PARADIS = "paradis-aot:latest"

# - MARLEY
PDF_PATH_MARLEY = "/workspaces/langchain-aot-war-simulator/Lore/marley_internal.pdf"
DB_DIR_MARLEY = "./sql_chroma_db/marley"
MODEL_NAME_MARLEY = "marley-aot:latest"

# CREATE LLM MODELS
paradis_model = OllamaLLM(model=MODEL_NAME_PARADIS)
marley_model = OllamaLLM(model=MODEL_NAME_MARLEY)

# CREATE PROMPT TEMPLATE
prompt = ChatPromptTemplate.from_template("""
You are taking your next turn in a two-faction geopolitical strategy simulation. Carefully read and internalize the following lore documents containing factual information about the world, factions, military structures, political dynamics, and historical context: {lore}.

If there are any present previous moves, be sure to retaliate rationally. The previous moves made this session are: {previous_moves}

Based only on your SYSTEM identity instructions, the retrieved lore above, and your stored memory, determine exactly ONE realistic strategic move that advances your faction’s objectives while responding directly to your opponent’s behavior. Assume the consequences of past actions implicitly without external resolution and do not write narrative or explanation. Output only the following structured format: ACTION_TYPE: <Diplomacy | Military | Espionage | Propaganda | Economic | Technology | Fortification | Deterrence> TARGETS: <Who or what is affected> METHOD: <How the move is executed> RESOURCES: <Assets or personnel committed> INTENSITY: <Low | Moderate | High> OBJECTIVE: <Strategic purpose of this move>.
""")

parser = StrOutputParser()

# CREATE CHAINS
chain_paradis = prompt | paradis_model | parser
chain_marley = prompt | marley_model | parser

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text(path, content):
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)

def load_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    return pages

def chunk_pdf(document):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 700,
        chunk_overlap = 200,
        length_function = len,
        add_start_index = True
    )
    chunks = text_splitter.split_documents(document)
    return chunks

def build_or_load_vectors(empire, chunks):
    embedding = FastEmbedEmbeddings()
    if empire == "paradis":
        if os.path.exists(DB_DIR_PARADIS) and os.listdir(DB_DIR_PARADIS):
            print("Loading existing vector databases...")
            vector_store = Chroma(persist_directory=DB_DIR_PARADIS, embedding_function=embedding)
        else:
            vector_store = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=DB_DIR_PARADIS)
        return vector_store
    elif empire == "marley":
        if os.path.exists(DB_DIR_MARLEY) and os.listdir(DB_DIR_MARLEY):
            print("Loading existing vector databases...")
            vector_store = Chroma(persist_directory=DB_DIR_MARLEY, embedding_function=embedding)
        else:
            vector_store = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=DB_DIR_MARLEY)
        return vector_store

def format_documents(sections):
    output_string = ""
    for s in sections:
        output_string += s.page_content
    return output_string

def generate_response(chain, retriever):
    document_chain = retriever.invoke(query)
    context = format_documents(document_chain)
    result = chain.invoke({
        "lore": context,
        "previous_moves": load_text("/workspaces/langchain-aot-war-simulator/previous_moves.txt")
    })
    
#############################################################################################################

result = chain_paradis.invoke({
    "lore": load_pdf("/workspaces/langchain-aot-war-simulator/Lore/paradis_internal.pdf"),
    "previous_moves": load_text("/workspaces/langchain-aot-war-simulator/previous_moves.txt")
})


print(result)
write_text("/workspaces/langchain-aot-war-simulator/previous_moves.txt", result)

result = chain_marley.invoke({
    "lore": load_pdf("/workspaces/langchain-aot-war-simulator/Lore/marley_internal.pdf"),
    "previous_moves": load_text("/workspaces/langchain-aot-war-simulator/previous_moves.txt")
})

print(result)
write_text("/workspaces/langchain-aot-war-simulator/previous_moves.txt", result)