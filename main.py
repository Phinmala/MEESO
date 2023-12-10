import speech_recognition as sr
from meeso import voice_input_mode, typing_input_mode
from config import get_openai_client

def main_menu():
    print("\nMain Menu:")
    print("1. Voice Input Mode")
    print("2. Typing Input Mode")
    print("3. Change TTS Option")
    print("4. Exit")
    return input("Enter your choice: ")

def main():
    client = get_openai_client()
    assistants = client.beta.assistants.list(order="desc", limit="20")
    if not assistants.data:
        print('>> Creating MEESO...')
        assistant = client.beta.assistants.create(
            name="MEESO",
            instructions="You're an assistant named MEESO, it stands for Molly's Expert in Efficient Specialized Operations.",
            model="gpt-3.5-turbo",
            tools=[{"type": "code_interpreter"}],
        )
        assistant_id = assistant.id
    else:
        assistant_id = assistants.data[0].id

    print('assistant.id: ' + assistant_id)

    existing_thread_id = "thread_zYVPSfD048pQbxqoLmmuKyPJ"
    thread_details = client.beta.threads.retrieve(thread_id=existing_thread_id)
    print("Thread Details:")
    print(thread_details)
    print("\n>> WELCOME TO MEESO!")
    tts_choice = input("Choose TTS option (1 for OpenAI, 2 for Google TTS, 3 for NONE): ").strip()

    while True:
        choice = main_menu()
        if choice == '1':
            voice_input_mode(assistant_id, client, existing_thread_id, tts_choice)
        elif choice == '2':
            typing_input_mode(assistant_id, client, existing_thread_id, tts_choice)
        elif choice == '3':
            tts_choice = input("Choose TTS option (1 for OpenAI, 2 for Google TTS, 3 for NONE): ").strip()
            continue  # Immediately prompt for next action
        elif choice == '4':
            print(">> Exiting MEESO Assistant.")
            break  # Exit the application
        else:
            print("[ERROR] Invalid input method")


if __name__ == "__main__":
    main()
