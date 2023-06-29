from bot_assistant import Bot_assistant
from userinterface import ConsoleInterface

if __name__ == "__main__":
    interface = ConsoleInterface()
    ba = Bot_assistant(interface)
    ba.main()
