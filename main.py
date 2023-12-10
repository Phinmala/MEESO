import speech_recognition as sr
from meeso import voice_input_mode, typing_input_mode
from config import get_openai_client

      
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

    tts_choice = input("Choose TTS option (1 for OpenAI TTS, 2 for Google TTS): ").strip()
    input_method = input("\n>> Choose input method: Type 'voice' for voice recognition or 'type' for typing: ").lower()
    assistant_id = assistants.data[0].id
    if input_method == 'voice':
        voice_input_mode(assistant_id,client, existing_thread_id, tts_choice)
    elif input_method == 'type':
        typing_input_mode(assistant_id, client, existing_thread_id, tts_choice)
    else:
        print("[ERROR] Invalid input method. Please type 'voice' or 'type'.")


if __name__ == "__main__":
    main()
