import argparse 
import json 
import random

def tiles_implementation(filename="tiles.txt"):
    """
    Loads tiles from a file.
    
    Args:
        filename: (str): File name
        
    Returns:
        list: List of the tile strings
        
    Author: Anna
    Includes: with statement
    """
    tiles = []
    
    with open(filename, "r") as file:
        for line in file:
            tile = line.strip()
            if tile:
                tiles.append(tile)
                
    return tiles

class Mahjong: 
    """
    Manages the state of the Mahjong game and the logic of the game. 
    
    Attributes: 
        tile_deck (list): the shared deck of tiles 
        player_names (list): a list of the 3 players in the game 
        
    """
    def __init__(self, player_names): 
        """
        Intializes the deck with the tiles. 
        
        Args: 
        
            player_names (list): A list of strings containg the name of players 
        
         """
        
        self.tile_deck = tiles_implementation()
        random.shuffle(self.tile_deck)

        self.players = []

        for name in player_names:
            new_player = Player(name)
            self.players.append(new_player)
        
    def deal(self): 
        """
        Deals 13 tiles to each player from the tile deck
        """
        for player in self.players: 
            for item in range(13): 
                player.hand.append(self.tile_deck.pop())
                
class Player: 
    """
    Represents an individual player in our Mahjong Game. 
    
    Attributes: 
    
        name (str): the name of the player 
        hand (list): a list of strings representing the players current hand 
    
    """
    
    def __init__(self, name): 
        self.name = name 
        self.hand = [] 

        
    

def turn_in_mahjong(hand, discard_tile, from_left):
    """
    Run one Mahjong turn and determine what actions are allowed after a tile is discarded. 

    Args: 
	    hand (list of strings): The tiles currently in the player's hand
	    discard_tile (string): The tile that was most recently discarded
	    from_left(bool): True if the discarded tile came from the player to the left

    Returns:
	    Str: A short description of what happened during the turn
    
    Side effects:
	    The players hand may change when tiles are added or removed
    
    Raises:
        ValueError if the move is not allowed 
        
    Author: Anna
    Includes: f strings
    """
    # Relying on tiles having letters abbreviation for bamboo dots and characters
    if (
        len(discard_tile) != 2 or
        not discard_tile[0].isdigit() or
        discard_tile[1] not in ["B", "D", "C"]
    ):
        raise ValueError("Invalid tile format.")
# Check for Pong, which can made formed if player already has two matching tiles
# Use of f string
    if hand.count(discard_tile) >= 2:
        hand.remove(discard_tile)
        hand.remove(discard_tile)
        return f"Pong formed with the discarded {discard_tile}!"
    
# Check for Chow, which is formed with three consecutive numbers of the same suit
# Chow only allowed if tile came from player on the left
    if from_left:
        try:
            tile_number = int(discard_tile[0])
            tile_suit = discard_tile[1]
            
            # Assuming we do a number + suit abbreviation for tiles
            # Use of f strings
            possible_chow_sequences = [
                [f"{tile_number-2}{tile_suit}", f"{tile_number-1}{tile_suit}"],
                [f"{tile_number-1}{tile_suit}", f"{tile_number+1}{tile_suit}"],
                [f"{tile_number+1}{tile_suit}", f"{tile_number+2}{tile_suit}"],
            ]
             
            for sequence in possible_chow_sequences:
                if all(tile in hand for tile in sequence):
                    hand.remove(sequence[0])
                    hand.remove(sequence[1])
                    return f"Chow formed with the discarded {discard_tile}"
                
        except (ValueError, IndexError):
            raise ValueError("Tile format invalid.")
        
    return "No moves can be made. Next turn!"


def is_winning_hand(hand):
    """
    checks if the hand you have gives you a win
    
    Args:
        hand (list): list of 14 tiles that you have
    
    Returns:
        bool: True if it is a winning hand, False if its not winning
    
    Side effects:
        None
    
    Raises: 
        None
    """
    
    if len(hand) != 14:
        return False
    
    hand = sorted(hand)
    
    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            
            if hand[i] == hand[j]:
                
                new_hand = []
                
                for k in range(len(hand)):
                    if k != i and k != j:
                        new_hand.append(hand[k])
                        
                if can_make_sets(new_hand):
                    return True
    
    return False

def can_make_sets(hand):
    """
    Checks if the remaining tiles can be split into sets
    
    Args:
        hand(list): list of tiles left after removing a pair
    
    Returns:
        bool: True if the remaining tiles can make valid sets, False if they cant
    
    Side effects:
        None
    
    Raises:
        None
    """
    
    if len(hand) == 0:
        return True
    first = hand[0]
    
    count = 0
    for tile in hand:
        if tile == first:
            count += 1
            
    if count >= 3:
        new_hand = []
        removed = 0
        
        for tile in hand:
           if tile == first and removed < 3:
               removed += 1
           else:
               new_hand.append(tile)
        
        if can_make_sets(sorted(new_hand)):
            return True
    if len(first) == 2 and first[0].isdigit():
        number = int(first[0])
        suit = first[1]
        
        second = str(number + 1) + suit
        third = str(number + 2) + suit
        
        has_second = False
        has_third = False
        
        for tile in hand:
            if tile == second:
                has_second = True
            if tile == third:
                has_third = True
                
        if has_second and has_third:
            new_hand = []
            removed_first = False
            removed_second = False
            removed_third = False
            
            for tile in hand:
                if tile == first and removed_first == False:
                    removed_first = True
                elif tile == second and removed_second == False:
                    removed_second = True
                elif tile == third and removed_third == False:
                    removed_third = True
                else: 
                    new_hand.append(tile)
                    
            if can_make_sets(sorted(new_hand)):
                return True
    return False

# Small function with conditional expression
# Makes the data for the next function a little more readable for players rather than just
# giving the number of the tiles
def tile_classification(tile_count):
    """
    Classifies a tile according to how many times its in an individual's hand.
    
    Args:
        tile_count: int, Number of times a tile appears.
        
    Returns:
        str: A keyword that describes how many times the tile occurs in an individual's hand.
        Including single, pair and multiple. 
        
    Side effects:
        None
        
    Raises:
        None
    """
    
    return "single" if tile_count == 1 else "pair" if tile_count == 2 else "multiple"

# Added this function to analyze the players hand and help the player in deciding how
# strong their hand is, maybe helping them figure out what to discard?
# We can remove it too if it doesn't work in the end
def hand_summary(hand):
    """
    Review and summarize hand in Mahjong to analyze tiles and duplicates.
    
    Args:
        hand: (list of str): Tiles in players hand
        
    Returns:
        dict: Information about the players hand
    """
    
    tile_set = set(hand)
    
    counts = {tile: hand.count(tile) for tile in tile_set}
    
    repeat_tiles = {tile for tile in tile_set if counts[tile] > 1}
    
    return {
        "tile_set" : tile_set,
        "counts" : counts,
        "repeat_tiles" : repeat_tiles
    }
    

def choose_discard(hand):
    """
    Chooses which tile a player should discard after drawing

    Args:
        hand(list of str): A list of 14 tile identifiers representing the 
        player's current hand after drawing

    Returns:
        String: the tile that should be discarded

    Side effects:
        None

    Raises:
        ValueError: If the hand does not contain exactly 14 tiles or if any 
        tile representation is incorrect
        
        ValueError: If tile does not contain 2 charactors. The tile number and 
        suite type
    
    Author: Nathan Brock
    """
    if len(hand) != 14:
        raise ValueError("Hand must contain exactly 14 tiles") 
    # Hand must have 14 tiles

    for tile in hand:
        if len(tile) != 2 or not tile[0].isdigit(): # conditional expression
            raise ValueError("Tile representation is incorrect")
        # each tile must be 2 charactors long like 3b or 7d

    def score_tile(tile, tiles): # look at each tile
        score = 0 
        # set variable for score. lowest score (how useful it is) will be removed
        number = int(tile[0]) # identify number for sequence
        suit = tile[1] # identify suits

        if tiles.count(tile) >= 2: # checks how many times tile appears
            score += 3  

        #check if tile has any concurent tiles (ex. 1b, 2b, 3b)
        if f"{number-1}{suit}" in tiles:
            score += 1
        if f"{number+1}{suit}" in tiles:
            score += 1
        if f"{number-2}{suit}" in tiles:
            score += 1
        if f"{number+2}{suit}" in tiles:
            score += 1

        return score
    worst_tile = min(hand, key=lambda tile: score_tile(tile, hand)) # which tile looks best to discard
    return worst_tile

def steal_or_pass(hand, discard_tile):
    """
    Decide whether to steal a tile from the discard pile of tiles and if you 
    steal a tile, determine which tile to discard in your hand to create 
    your best possible hand. 
    
    
    Args: 
        hand(list of strings): A list of 13 tile identifiers representing the players 
            current concealed hand 
        discard_tile (str): A single tile identifier representing the tile just 
            discarded by another player 
        
    Returns 
        Str: if the player should steal: returns the tile to the discard 
            after stealing a tile from the player. 
            If the player should not steal: returns the string "pass" 
    Side Effects: 
        hand(list of strings): gets appended based on the new tile and discarded tile 
    Raises: 
        ValueError: If the hand does not contain exactly 13 tiles 
    
    
    """

    if len(hand) != 13: 
        raise ValueError("Your hand must contain exactly 13 tiles")
    
    
    potential_hand = hand + [discard_tile] 
    
    if is_winning_hand(potential_hand): 
        steal_tile = True
    elif hand.count(discard_tile) >=2: 
        steal_tile = True 
    else: 
        steal_tile = False 
    
    
    if steal_tile == True: 
        hand.append(discard_tile)
      
        matchless_tile = [tile for tile in hand if hand.count(tile) ==1]
        
        if len(matchless_tile) >0: 
            junk_tile = matchless_tile[0]
        else: 
            junk_tile = hand[0]
            
        hand.remove(junk_tile)
        return junk_tile 
    
    return "pass" 

def player_turn(player, game, human_turn): 
    """
    Executes a full turn in mahjong for a player. Draws a tile, then
    checks if that tile gives them a mahjong, and selecting a tile to discard. 
    
    Author: Noah 
    Techniques: Use of a key function with the sorted command 
    
    Args: 
    
    Returns: 
    
       

    """
    if len(game.tile_deck) == 0: 
        return f"(Deck is empty)", None 
    
    tile = game.tile_deck.pop()
    player.hand.append(tile)

    print(f"{player.name} draws {tile}")
    
    if is_winning_hand(player.hand): 
        print(f"{player.name} wins")
        return "win", None 
    
    sorted_hand = sorted(player.hand, key=lambda tile: (tile[1], int(tile[0])))
    if human_turn: 
        print("Your hand is:", sorted_hand)
        
        discard = input("Choose a tile to discard: ").strip()
        while discard not in player.hand: 
            discard = input("Invalid tile to discard. Pick a new tile to discard: ").strip()
    else: 
        discard = choose_discard(player.hand)
    player.hand.remove(discard)
    print(f"{player.name} discards {discard}")
            
    return "continue", discard     


def check_steal_options(players, current_index, discard):
    """
    Checks if a player can steal the discarded tile to make a Pong or Chow

    Args:
        players: List of Player objects
        current_index: Index of the player who discarded last
        discard: The tile that was last discarded

    Returns:
        If someone steals it returns (player_index, new_discard)
        If nobody steals it returns (None, discard)
    """
    for offset in range(1, len(players)):


        player_index = (current_index + offset) % len(players) # next player
        player = players[player_index]


        # player after can discard
        if offset == 1:
            from_left = True
        else:
            from_left = False


        action = turn_in_mahjong(player.hand, discard, from_left)


        if "Pong" in action or "Chow" in action:
            print(f"{player.name} steals {discard}")
            print(action)


            new_discard = choose_discard(player.hand)
            player.hand.remove(new_discard)


            print(f"{player.name} discards {new_discard}")


            return player_index, new_discard


    return None, discard

def get_next_player_index(current_index, number_of_players):
    """
    Gets the next player's index.

    Args:
        current_index (int): The index of the current player
        number_of_players (int): The number of players

    Returns:
        int: The next player's index

    Side effects:
        None

    Raises:
        None
    """

    current_index = current_index + 1

    if current_index == number_of_players:
        current_index = 0

    return current_index


def game_loop(game):
    """
    Runs the game after the players are made and the tiles are dealt.

    Args:
        game (Mahjong): The Mahjong game

    Returns:
        None

    Side effects:
        Prints the game to the console and changes player hands

    Raises:
        None
    """

    current_player_index = 0
    game_is_running = True

    while game_is_running:
        if len(game.tile_deck) == 0:
            print("The deck is empty. No winner.")
            game_is_running = False
        else:
            current_player = game.players[current_player_index]

            if current_player_index == 0:
                human_turn = True
            else:
                human_turn = False

            result, discard_tile = player_turn(current_player, game, human_turn)

            if result == "win":
                print("Game over.")
                game_is_running = False
            else:
                current_player_index = get_next_player_index(
                    current_player_index,
                    len(game.players)
                )


def main():
    """
    Starts the Mahjong game.

    Args:
        None

    Returns:
        None

    Side effects:
        Creates the game, deals the tiles, and starts the game loop

    Raises:
        None
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--players", nargs=3, default=["You", "Computer 1", "Computer 2"])

    args = parser.parse_args()

    game = Mahjong(args.players)
    game.deal()

    print("Starting Mahjong game!")
    print("You are Player 1.")
    print("Type the tile you want to discard when it is your turn.")
    print()

    game_loop(game)


if __name__ == "__main__":
    main()


