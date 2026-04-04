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
    
# Check for Pong, which can made formed if player already has two matching tiles
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