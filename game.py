import random
from utilities import takeCommand, speak

def game_play():
    speak("Let's Play ROCK PAPER SCISSORS!")
    print("LET'S PLAY ROCK PAPER SCISSORS!")
    Me_score = 0
    Com_score = 0
    for i in range(5):
        speak("Please choose rock, paper, or scissors.")
        query = takeCommand().lower()
        while query not in ["rock", "paper", "scissors"]:
            speak("Sorry, I didn't understand. Please choose rock, paper, or scissors.")
            query = takeCommand().lower()

        choose = ("rock", "paper", "scissors")  # Tuple
        com_choose = random.choice(choose)

        if query == com_choose:
            speak(com_choose.upper())
            print(f"Score: ME - {Me_score} | COM - {Com_score}")
        elif query == "rock" and com_choose == "scissors" or \
             query == "paper" and com_choose == "rock" or \
             query == "scissors" and com_choose == "paper":
            speak(com_choose.upper())
            Me_score += 1
            print(f"Score: ME - {Me_score} | COM - {Com_score}")
        else:
            speak(com_choose.upper())
            Com_score += 1
            print(f"Score: ME - {Me_score} | COM - {Com_score}")

    speak(f"FINAL SCORE: ME - {Me_score} | COM - {Com_score}")

# Example usage:
# game_play()
