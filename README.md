# INST326-Group-104-Project-

### **Explanation of Files:**

**lets_play_mahjong:** Main python file containing Mahjong game. 

**tiles.txt**: Text file containing 108 Mahjong tiles.

**Group_Work_Test:** File from Collaborative Programming Exercise, can be ignored for purposes of the game.

**README.md:** ReadMe file containing explanations on how to run and use the program, proper files, group member contributions, and annotated references. Essentially, this acts as a user guide to get started with playing our game of Mahjong. 


### **How to Run the Program from the Command Line:**
Step 1: Make sure the files, lets_play_mahjong_inst326.py, and tiles.txt, are saved in the same directory.

Step 2: Open terminal (Command Prompt, Mac Terminal, Powershell, Git Bash, etc.) and access the folder that has both files saved in it. 

Step 3: Run the program, type the following into the terminal (Windows)
   python lets_play_mahjong_inst326

### **How to Use the Program and How to Play Python Mahjong:**

-Mahjong tiles are shuffled from tiles.txt

-Each player is given 13 tiles at the beginning of the game, with the first player being the human player, and the remaining 2 being computer players
-When it is your turn: 

   A tile will be drawn from the deck, and you will have your current hand displayed. 
   
   You will then we asked to pick a tile to discard. 
   
-When a tile is discarded, the program will review if other players can form Pong or Chow

   Pong: Formed by two matching tiles
   
   Chow: Formed by a sequence of three consecutive numbers in the same suit, with a discarded tile needing to be included that came from the player on the left
   
-The game keeps going until a player wins or the deck is empty

### **Contributions:**

| Method/Function        | Primary Author | Technique(s) Demonstrated |
| ---------------------- | -------------- | ------------------------- |
| `turn_in_mahjong`      | Anna Wendt     | f-strings                 |
| `tiles_implementation` | Anna Wendt     | with statement            |
| `steal_or_pass`        | Noah Rosier    | list comprehension        |
| `player_turn`          | Noah Rosier    | Use of a key function     |
| `check_steal_options`  | Nathan Brock   | Conditional Expression    |
| `choose_discard`       | Nathan Brock   | Regular Expression        |
| `is_winning_hand`      | William Horan  | Optional Parameters       |
| `can_make_sets`        | William Horan  | sequence unpacking        |


### **Annotated References:**

(2019). The Mahjong Project. The Mahjong Project. https://www.themahjongproject.com/how-to-play/basics
This source was used to understand the basic rules of Chinese Mahjong, and therefore implement those rules into an algorithm. 

Gruppetta, S. (2024, May). Python Sequences: A Comprehensive Guide. Realpython.com; Real Python. https://realpython.com/python-sequences/
This source was used as a refresher, and reference guide for sequences in Python. It was used for the first function of code, which goes through a turn in Mahjong. The game of Mahjong, and the tiles themselves, is a very sequenced-based game, so this source gave more information on how to apply those sequences to Python. 

Python Tutorial. (2021, December 10). Python Regex fullmatch. https://www.pythontutorial.net/python-regex/python-regex-fullmatch/#:~:text=The%20fullmatch()%20function%20returns,regular%20expression%2C%20or%20None%20otherwise.&text=In%20this%20syntax%3A,string%20specifies%20the%20input%20string. This sourced was used to help with the regular expression technique
in our program. It was used to learn how to do use fullmatch() in Regex and create the regular expression in our code. 

South China Morning Post. (2018, August 12). Learn how to play mahjong in 2.5 minutes [Video]. YouTube. https://www.youtube.com/watch?v=qpYF-xmNMew
This source was used to help understand the rules of Mahjiong and the aspects of the game. It was helpful in giving information how to apply certain 
steps of Mahjong into python. 



