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
def process_user_input(user_input):
    tokens = word_tokenize(user_input.lower())
    processed_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return processed_tokens


'''
Call the processed_user_input() func, 
check if the key words : quit, look, take, inventory, go, talk, unlock; exists in the processed_tokens
return appropriate functions for each of those key words.
If none of the key words exists in the tokens, return "I don't understand that command."
'''
def handle_user_command(user_input):
    global current_room, score
    processed_tokens = process_user_input(user_input)
    if "quit" in processed_tokens:
        return quit_game()
    
    elif "look" in processed_tokens:
        return look_around()
    
    elif "take" in processed_tokens:
        return take_item(processed_tokens)
    
    elif "inventory" in processed_tokens:
        return inventory_status()
    
    elif "go" in processed_tokens:
        return go_to(processed_tokens)
    
    elif "talk" in processed_tokens:
        return talk_to(processed_tokens)
    
    elif "unlock" in processed_tokens:
        return unlock(processed_tokens)
    else:
        return "I don't understand that command."


'''
Return a string which gives the final score.
'''
def quit_game():
    #write code here
    global score
    return f"Game over. Your final score is {score}"


'''
This func should return the information of the room. 
The information should include the description of the room and
also the the items in the room if any
'''
def look_around():
    global current_room
    room_dict = rooms[current_room]
    room_description = room_dict[description]
    room_items = room_dict[items]
    room_str = f"Description : {room_description}\nItems: {room_items}"
    return room_str


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
    global current_room, score
    item = " ".join(tokens[tokens.index("take") + 1:])
    room_dict = rooms[current_room]

    if "items" in room_dict.getKeys():
        if "treasure box" in room_dict[items] and room_dict[lock]:
            return("Treasure box is locked")
        
        else:
            for i in room_dict[items]:
                inventory.append(i)
                return_str = f"{return_str}, {i}"
            room_dict[items].clear()
            return f"Took the item(s) {return_str}"
    
    else:
        return "There is nothing to take in this room"
            
        

    
    


'''
This function should return a string with the contents of the inventory
'''
def inventory_status():
    print('The items in the inventory is:')
    for i in inventory:
        print(i)


'''
If user has bread with them, the rats will attack the user.
The user looses 30 points. 
Return a string of appropiate msg if rats exists else return None 
'''
def handle_rats():
    global current_room, score
    room_dict = rooms[current_room]
    rat_status = False                  # Initializing rat_status variable
    if "rats" in room_dict.getKeys():       
        rat_status = room_dict[rats]
        if rat_status == True and "bread" in inventory:
            score -= 30
            return "You were attacked by rats, you lost 30 points"
    else:
        return None





'''
Write a function to go to a different room based on the direction specified.
Call handel_rats() function to check if rats exist
Everytime user enters a new room, give the description of the room.
'''
def go_to(tokens):
    global current_room
    direction = tokens[tokens.index("go") + 1]
    room_dict = rooms[current_room]
    room_exits = room_dict[exits]
    current_room = room_exits[direction]
    rat_stat = handle_rats()
    if rat_stat != None:
        return rat_stat
    else:
        room_dict = rooms[current_room]
        room_desc = f"{room_dict[description]}"
        return room_desc
    

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
    pass


'''
Write a function to use the old book to unlock the treasure box.
The treasure box can be unlocked only if the user is in the bedroom and has "old_book" in the inventory
Display the "puzzle" any time the user tryies to unlock the treasure box.
Return "You read the old book and found a code. The locked treasure box has been unlocked." once unlocked
Increase 50 points if the tresure box gets unlocked.
Return appropriate message if any of the conditions are not met.
'''
def unlock(tokens):
    if rooms[current_room]=="bedroom":
        if "old_book" in inventory:
            print(rooms[current_room]['puzzle'])
            score+=50
            return "You read the old book and found a code. The locked treasure box has been unlocked."
        else:
            return "old_book not found"
    else:
        return "You are not in bedroom"




def play_game():
    print("Welcome to the Haunted House Adventure!")
    print("Type 'quit' to exit the game.")

    while True:
        user_input = input("> ").strip()
        response = handle_user_command(user_input)
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

