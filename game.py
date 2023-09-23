import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from leaderboard import Leaderboard
from rooms import rooms
from npcs import npcs
from npcs_actions import witch_challenge, knight_challenge, ghost_challenge, sorcerer_challenge

# Initialize lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Initialize leaderboard
leaderboard = Leaderboard()

# Global game variables
current_room = "hallway"
inventory = []
score = 0



"""
Process the user's input by tokenizing and lemmatizing it, removing stop words.
Return a list of processed tokens.
"""
def process_character(character):
    pass


'''
Call the processed_character() func, 
check if the key words : quit, look, take, inventory, go, talk, unlock; exists in the processed_tokens
return appropriate functions for each of those key words.
If none of the key words exists in the tokens, return "I don't understand that command."
'''
def handle_user_command(character):
    global current_room, score
    pass



'''
Return a string which gives the final score.
'''
def quit_game():
    #write code here
    pass


'''
This func should return the information of the room. 
The information should include the description of the room and
also the the items in the room if any
'''
def look_around():
    #write code here
    pass



'''
Write a function to take an item which is present in the room.
note: you can take only those items which are present in the room.
Every time you take an item, you get 10 points.
Append the item in the inventory.
You are not allowed to take the treasure box till it is locked. 
Once the treasure box is unlocked u can take the treasure box.
Return an appropriate string for the either of the following cases:
1. Treasure box is locked
3. Took the {item}
4. There is nothing to take in the room.
'''
def take_item(tokens):
    item = " ".join(tokens[tokens.index("take") + 1:])
    pass


'''
This function should return a string with the contents of the inventory
'''
def inventory_status():
    for item in inventory:
        print(item,end=" ")


'''
If user has bread with them, the rats will attack the user.
The user looses 30 points. 
Return a string of appropiate msg if rats exists else return None 
'''
def handle_rats():
    pass



'''
Write a function to go to a different room based on the direction specified.
Call handel_rats() function to check if rats exist
Everytime user enters a new room, give the description of the room.
'''
def go_to(tokens):
    direction = tokens[tokens.index("go") + 1]
    pass

'''
Write a function to talk to the npcs.
User can talk to any of the npcs from anywhere in the house.
Each npc has a challenge. Call appropriate npc_challenge() function.
To complete the challenge the user must have the item in the inventory which is required by that specific npc
Every npc_challenge() returns the final score
The talk_to() should return the string "Updated score is {score}" if the user interacts with npcs,
else return the string "{npc['dialogue']} You need {required_item} if you need my help."
If the mentioned npc doesnt exist in npcs then return "{character} is not there!"
'''
def talk_to(tokens):
    character = " ".join(tokens[tokens.index("talk") + 1:])
    item = input("Enter required item: ")
    if character == "witch":
            if item == npcs['item_required']:
                return witch_challenge()
            else:
                print(f"{npcs['witch']['dialogue']} You need {npcs['witch']['required_item']} if you need my help")
    elif character == "knight":
            if item == npcs['item_required']:
                return knight_challenge()
            else:
                print(f"{npcs['knight']['dialogue']} You need {npcs['knight']['required_item']} if you need my help")
    elif character == "ghost":
            if item == npcs['item_required']:
                return ghost_challenge()
            else:
                print(f"{npcs['ghost']['dialogue']} You need {npcs['ghost']['required_item']} if you need my help")
    elif character == "sorcerer":
            if item == npcs['item_required']:
                return sorcerer_challenge() 
            else:
                print(f"{npcs['sorcerer']['dialogue']} You need to answer my riddle if you need my help")
    
    if character == "witch" or "knight" or "ghost" or "sorcerer":
            print(f"Updated score is {score}")
    else: 
            print(f"{character} is not here!")
    
    
        


'''
Write a function to use the old book to unlock the treasure box.
The treasure box can be unlocked only if the user is in the bedroom and has "old_book" in the inventory
Display the "puzzle" any time the user tryies to unlock the treasure box.
Return "You read the old book and found a code. The locked treasure box has been unlocked." once unlocked
Increase 50 points if the tresure box gets unlocked.
Return appropriate message if any of the conditions are not met.
'''
def unlock(tokens):
    if current_room == "bedroom":
        item = input("Enter item required for unlocking the treasure box: ")
        if item == "old book":
            print("You read the old book and found a code. The locked treasure box has been unlocked")
            score += 50
        else:
            print("You don't have appropriate item")
    else:
        print("You should be in bedroom to open treasure box")
            




def play_game():
    print("Welcome to the Haunted House Adventure!")
    print("Type 'quit' to exit the game.")

    while True:
        character = input("> ").strip()
        response = handle_user_command(character)
        print(response)

        if current_room == "bedroom" and "treasure box" in inventory:
            print(rooms["bedroom"]["ending"])
            player_name = input("Enter your name: ")
            leaderboard.update(player_name, score)
            leaderboard.display()
            break

        if "quit" in response.lower():
            player_name = input("Enter your name: ")
            leaderboard.update(player_name, score)
            leaderboard.display()
            break

# Call the play_game function to start the game
play_game()

