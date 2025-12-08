from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os

shared_world_path = '/workspaces/langchain-aot-war-simulator/Lore/shared_world.md'
omniscient_canon_path = '/workspaces/langchain-aot-war-simulator/Lore/omniscient_canon.md'
paradis_internal_path = '/workspaces/langchain-aot-war-simulator/Lore/paradis_internal.md'
marley_internal_path = '/workspaces/langchain-aot-war-simulator/Lore/marley_internal.md'

combined = [shared_world_path, omniscient_canon_path, paradis_internal_path, marley_internal_path]

def access_md(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
            return markdown_content
    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

access_md(shared_world_path)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    for doc_i in range(len(combined)):
        document = Document(
            page_content=access_md(combined[doc_i]),
            id=str(doc_i)
        )
        ids.append(str(doc_i))
        documents.append(document)
    
vector_store = Chroma(
    collection_name="aot_lore",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})