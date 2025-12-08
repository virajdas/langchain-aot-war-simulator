from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

paradis_model = OllamaLLM(model="paradis-aot:latest")
marley_model = OllamaLLM(model="marley-aot:latest")

# Credit: Template message written by ChatGPT
template = """
You are taking your next turn in a two-faction geopolitical strategy simulation. Carefully read and internalize the following lore documents containing factual information about the world, factions, military structures, political dynamics, and historical context: {lore}. Your memory already contains the complete record of all previous moves made by both your faction and the opposing faction, which together represent the evolving world state. Based only on your SYSTEM identity instructions, the retrieved lore above, and your stored memory, determine exactly ONE realistic strategic move that advances your faction’s objectives while responding directly to your opponent’s behavior. Assume the consequences of past actions implicitly without external resolution and do not write narrative or explanation. Output only the following structured format: NATION_NAME: <Paradis | Marley> ACTION_TYPE: <Diplomacy | Military | Espionage | Propaganda | Economic | Technology | Fortification | Deterrence> TARGETS: <Who or what is affected> METHOD: <How the move is executed> RESOURCES: <Assets or personnel committed> INTENSITY: <Low | Moderate | High> OBJECTIVE: <Strategic purpose of this move>.
"""

prompt = ChatPromptTemplate.from_template(template=template)
chain = prompt | paradis_model

result = chain.invoke({
    "lore": retriever.invoke("Provide relevant lore for the next strategic move in the simulation.")
})

print(result)

chain = prompt | marley_model

result = chain.invoke({
    "lore": retriever.invoke("Provide relevant lore for the next strategic move in the simulation.")
})

print(result)