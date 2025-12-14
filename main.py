'''
Just to meet the requirement of the assignment to specify what parts of the code were written by AI, I want to credit ChatGPT for writing all of the descriptions and instructions for the AI models (prompts, empire PDFs, units text files, etc.). I have also used the Copilot autocomplete built into VS Code throughout the writing of this code file to help speed up the coding process, but I have personally written and structured all of the code logic, functions, and main program flow.

I have not used the modelfiles that ChatGPT created in this final program as, in my testing and iterating of this project, I found them to be more destructive to the responses than truly helpful. Thus, I am only using the base Llama 3.2 model for both empires as I have been getting stronger generations with it and the prompt, PDFs, and text files (passed to the model to differentiate empire behavior).
'''

# DEPENDENCIES
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from termcolor import colored

# VARIABLES
PARADIS_PDF_PATH = "/workspaces/langchain-aot-war-simulator/Lore/paradis_internal.pdf"
MARLEY_PDF_PATH = "/workspaces/langchain-aot-war-simulator/Lore/marley_internal.pdf"

PARADIS_UNITS_PATH = "/workspaces/langchain-aot-war-simulator/Lore/paradis_units.txt"
MARLEY_UNITS_PATH = "/workspaces/langchain-aot-war-simulator/Lore/marley_units.txt"

MOVES_TEXT_FILE_PATH = "previous_moves.txt"

model = OllamaLLM(model="llama3.2")

prompt = ChatPromptTemplate.from_template("""
You are {EMPIRE_NAME}. Read the opponent’s last move below and decide your next move. Stay in-character with {EMPIRE_NAME}’s goals and lore, do not repeat the opponent’s move, do not target your own units, and make a sensible action against the enemy. Output only your next move as plain text. Be as detailed as possible, mentioning specific units, locations, and strategies from the Attack on Titan universe.

Opponent’s last move: {OPPONENT_LAST_MOVE}
                                          
It is of the utmost importance that you move using only resources, units, and regiments that your nation has, detailed here: {LORE}
                                          
Only focus on the present situation and do not predict future moves.
                                          
Remember that you are {EMPIRE_NAME}, so you cannot use units, regiments, garrisons, and more that belong to the opposing nation. Please make sure to use as many of your own units in combat as possible and describe their use / action in extreme detail. Here is a list of units available to {EMPIRE_NAME}: {UNITS}

Avoid taking your opponent's side, and only do what benefits your empire the most (based on the goals of your nation outlined in the lore).

You are only to output a 2-3 sentence move that {EMPIRE_NAME} would realistically make in response to the opponent’s last move, nothing more.
""")

parser = StrOutputParser()

# CREATE CHAIN
chain = prompt | model | parser

# DEFINE FUNCTIONS
def load_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    return pages

def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text(path, content):
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)

def clear_text(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("")

def generate_response(empire_name, opponent_last_move, lore, units):
    response = chain.invoke({"EMPIRE_NAME": empire_name, "OPPONENT_LAST_MOVE": opponent_last_move, "LORE": lore, "UNITS": units})
    message = f"{empire_name}:\n{response}\n\n"
    write_text(MOVES_TEXT_FILE_PATH, message)
    if empire_name == "PARADIS":
        message = f"{colored(empire_name, 'blue')}:\n{response}\n\n"
    else:
        message = f"{colored(empire_name, 'green')}:\n{response}\n\n"
    print(message)
    return response

# MAIN LOGIC
def main():
    clear_text("previous_moves.txt")

    while True:
        try:
            num_turns = int(input("Enter number of turns to simulate (excluding opening): "))
            break
        except:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            use_default_opening = int(input("Would you like to use the default opening move or write your own?\n1. Default\n2. Custom\nEnter 1 or 2: "))
            break
        except:
            print("Invalid input. Please enter an integer.")

    if use_default_opening == 1:
        message = f"\n{colored('PARADIS (Default Start):', 'blue')}\nTitan and Scount Regiment (lead by Hange Zoe) assault on major Marleyan city and port, Liberio, destroying key military installations and infrastructure to cripple Marleyan defenses. The attack aims to weaken Marley's hold on the region and pave the way for future offensives. We also want to gain a better understanding of the power of the Titans and our role as subjects of Ymir.\n"
        print(message)
        write_text(MOVES_TEXT_FILE_PATH, f"PARADIS:\nTitan and Scount Regiment (lead by Hange Zoe) assault on major Marleyan city and port, Liberio, destroying key military installations and infrastructure to cripple Marleyan defenses. The attack aims to weaken Marley's hold on the region and pave the way for future offensives. We also want to gain a better understanding of the power of the Titans and our role as subjects of Ymir.\n\n")
        response = generate_response("MARLEY", "PARADIS:\nTitan and Scount Regiment (lead by Hange Zoe) assault on major Marleyan city and port, Liberio, destroying key military installations and infrastructure to cripple Marleyan defenses. The attack aims to weaken Marley's hold on the region and pave the way for future offensives. We also want to gain a better understanding of the power of the Titans and our role as subjects of Ymir.", load_pdf("Lore/marley_internal.pdf"), read_text(MARLEY_UNITS_PATH))
    elif use_default_opening == 2:
        custom_move = input("Enter your custom opening move from the perspective of PARADIS / New Eldian Empire: ")
        write_text(MOVES_TEXT_FILE_PATH, f"PARADIS:\n{custom_move}\n\n")
        print()
        response = generate_response("MARLEY", custom_move, load_pdf("Lore/marley_internal.pdf"), read_text(MARLEY_UNITS_PATH))
    else:
        print("Invalid input. Using default opening move.\n")
        message = f"\n{colored('PARADIS (Default Start):', 'blue')}\nTitan and Scount Regiment (lead by Hange Zoe) assault on major Marleyan city and port, Liberio, destroying key military installations and infrastructure to cripple Marleyan defenses. The attack aims to weaken Marley's hold on the region and pave the way for future offensives. We also want to gain a better understanding of the power of the Titans and our role as subjects of Ymir.\n"
        print(message)
        write_text(MOVES_TEXT_FILE_PATH, f"PARADIS:\nTitan and Scount Regiment (lead by Hange Zoe) assault on major Marleyan city and port, Liberio, destroying key military installations and infrastructure to cripple Marleyan defenses. The attack aims to weaken Marley's hold on the region and pave the way for future offensives. We also want to gain a better understanding of the power of the Titans and our role as subjects of Ymir.\n\n")
        response = generate_response("MARLEY", "PARADIS:\nTitan and Scount Regiment (lead by Hange Zoe) assault on major Marleyan city and port, Liberio, destroying key military installations and infrastructure to cripple Marleyan defenses. The attack aims to weaken Marley's hold on the region and pave the way for future offensives. We also want to gain a better understanding of the power of the Titans and our role as subjects of Ymir.", load_pdf("Lore/marley_internal.pdf"), read_text(MARLEY_UNITS_PATH))

    for i in range(num_turns - 1):
        if i % 2 == 0:
            empire = "PARADIS"
            pdf = PARADIS_PDF_PATH
            units = PARADIS_UNITS_PATH
        else:
            empire = "MARLEY"
            pdf = MARLEY_PDF_PATH
            units = MARLEY_UNITS_PATH
        response = generate_response(empire, response, load_pdf(pdf), read_text(units))

# RUN MAIN
if __name__ == "__main__":
    main()