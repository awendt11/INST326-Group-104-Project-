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
        IndexError if tile string isn't number + suit format
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
    
    args:
    hand (list): list of 14 tiles that you have
    
    returns:
    bool: True if it is a winning hand, False if its not winning
    
    Side effects:
    None
    
    Raises: 
    none
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
    
    args:
    hand(list): list of tiles leeft after removing a pair
    
    returns:
    bool: True if the remaining tiles can make valid sets, False if they cant
    
    side effects:
    None
    
    Raises:
    none
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
    """
    if len(hand) != 14:
        raise ValueError("Hand must contain exactly 14 tiles") 
    # Hand must have 14 tiles

    for tile in hand:
        if len(tile) != 2 or not tile[0].isdigit():
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
