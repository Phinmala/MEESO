from utils import text_to_speech, play_audio, pyttsx3_speech
import speech_recognition as sr
import time
import keyboard


def ask_openai(assistant_id, question, client, existing_thread_id, tts_option):
    message = client.beta.threads.messages.create(
    thread_id=existing_thread_id,
    role="user",
    content=question
)
    run = client.beta.threads.runs.create(
    thread_id=existing_thread_id,
    assistant_id=assistant_id,
    )
    # Wait for the run to complete and retrieve the response
 
    while True:

        run = client.beta.threads.runs.retrieve(
            thread_id=existing_thread_id,
            run_id=run.id
        ) 
        if run.status == 'completed':
            thread_messages = client.beta.threads.messages.list(existing_thread_id)
            for message in thread_messages.data:
                if message.role == "assistant":
                    last_message = message.content[0].text.value
                    #return (last_message)
                    print("MEESO: " + last_message)
                    tts_file = text_to_speech(last_message, tts_option)  # Convert text to speech
                    return tts_file   
            return ">> No response from the assistant.", None
        print('>> MEESO is thinking...')
        time.sleep(2)

def voice_input_mode(assistant_id, client, existing_thread_id, tts_option):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print(">> MEESO Assistant Ready (Voice Mode). Press Enter to start speaking. Recording will stop if silence is detected for 5 seconds.")

    while True:
        print(">> Press Enter to start speaking...")
        keyboard.wait('enter')  # Wait for Enter key to be pressed
        with microphone as source:
            
            try:
                recognizer.adjust_for_ambient_noise(source,duration=2)
                print(">> Listening... Speak now.")
                recognizer.pause_threshold = 2.0
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio).lower()
                print("original string: " + user_input)
                user_input = user_input.replace('miso', 'MEESO')
                user_input = user_input.replace('me so', 'MEESO')
                user_input = user_input.replace('mesa', 'MEESO')

                if user_input == 'exit':
                    print(">> Exiting MEESO Assistant.")
                    break

                print("You: " + user_input)
         
                tts_file = ask_openai(assistant_id, user_input, client, existing_thread_id, tts_option)
                
                if tts_file:
                    play_audio(tts_file)

            except sr.WaitTimeoutError:
                print("[ERROR] No speech detected.")
                continue  # Return to the start of the loop for another input
            except sr.UnknownValueError:
                print("[ERROR] Sorry, I did not understand that.")
            except sr.RequestError as e:
                print(f"[ERROR] Could not request results; {e}")


def typing_input_mode(assistant_id, client, existing_thread_id, tts_option):
    print(">> MEESO Assistant Ready (Typing Mode). Type your query, or type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip().lower()

        if user_input == 'exit':
            print(">> Exiting MEESO Assistant.")
            break
        
        # response = ask_openai(assistant_id, user_input)
        # print("MEESO:", response)
        response, tts_file = ask_openai(assistant_id, user_input, client, existing_thread_id, tts_option)
        print("MEESO:", response)
        if tts_file:
            play_audio(tts_file)