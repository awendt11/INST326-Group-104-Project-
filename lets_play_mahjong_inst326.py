def turn_in_mahjong (hand, discard_tile, from_left):
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
    """
