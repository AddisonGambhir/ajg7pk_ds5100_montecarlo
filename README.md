# ajg7pk_ds5100_montecarlo


This module essentially models a 'Monte Carlo' simulation involving dice rolls. The Die class lets you model and manipulate a die with specified faces and weights, the Game class lets you play games with multiple dice, and the Analyzer class offers tools to analyze the results of those games.



Documentation of class features and methods: 
class Die(builtins.object)
 |  Die(faces: numpy.ndarray)
 |  
 |  Fibricates a 'die' object that has specified faces and weights.
 |  
 |  Attributes:
 |      _die_data (pandas.DataFrame): This is the dataframe that stores face values and weights.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, faces: numpy.ndarray)
 |      Initializes the die object with specified 'faces'.
 |      
 |      Args:
 |          faces (numpy.ndarray): An array containing distinct face values of the die.
 |      
 |      Raises:
 |          TypeError: If faces is not a NumPy array.
 |          ValueError: If faces do not have distinct values.
 |  
 |  get_die_state(self) -> pandas.core.frame.DataFrame
 |      This will return a copy of the die's data frame.
 |      
 |      Returns:
 |          pandas.DataFrame: A copy of the die data frame.
 |  
 |  roll(self, num_rolls: int = 1) -> list
 |      This method simulates rolling of the die multiple times.
 |      
 |      Argument:
 |          num_rolls (int): The number of times the die is rolled.
 |      
 |      Returns:
 |          list: A list of outcomes from rolling the die.
 |  
 |  set_weight(self, face, weight)
 |      This controls the weight for a specific face value.
 |      
 |      Arguments:
 |          face: The face value for which the weight is to be set.
 |          weight: The weight value assigned.
 |      
 |      Raises:
 |          IndexError: If the face value is invalid.
 |          TypeError: If the weight is not a numeric value.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)

Help on class Game in module montecarlo.montecarlo:

class Game(builtins.object)
 |  Game(dice)
 |  
 |  The game class contains a game consisting of rolling multiple dice.
 |  
 |  Attributes:
 |      dice: A list of Die objects representing the dice in the game.
 |      play_data: Data frame that stores the results of the most recent play.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, dice)
 |      This initializes the Game class with a list of similar dice.
 |      This also checks if the list contains Die objects
 |      Argusment:
 |          dice (list): A list of already instantiated similar dice (Die objects).
 |  
 |  play(self, times)
 |      This method simulates playing the game by rolling the dice a specified number of times.
 |      
 |      Argsuments:
 |          times (int): The number of times instructed to roll the dice.
 |  
 |  show_results(self, form='wide')
 |      This method displays the results of the most recent play.
 |      
 |      Args:
 |          Format options: Options include: 'wide' (default) or 'narrow'
 |      
 |      Returns:
 |          pandas.DataFrame: The play results data frame.
 |      
 |      Raises:
 |          ValueError: If an invalid option is provided for the format.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)

Help on class Analyzer in module montecarlo.montecarlo:

class Analyzer(builtins.object)
 |  Analyzer(game)
 |  
 |  Analyzes the results of a single game and computes various descriptive properties.
 |  
 |  Attributes:
 |      game (Game): A Game object whose results will be analyzed.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, game)
 |      Initializes an Analyzer object with a Game object.
 |      
 |      Args:
 |          game (Game): A Game object whose results will be analyzed.
 |      
 |      Raises:
 |          ValueError: If the input is not a Game object.
 |  
 |  combo_count(self)
 |      Determines unique combinations of faces rolled, along with their counts.
 |      
 |      Returns:
 |          pandas DataFrame with distinct combinations and associated counts.
 |  
 |  face_counts_per_roll(self)
 |      Counts how many times a given face is rolled in each event.
 |      
 |      Returns: A data frame with an index of the roll number, face values as columns,
 |      and count values in the cells (in the 'wide' format).
 |  
 |  jackpot(self)
 |      Jackpot computes the number of jackpot occurrences in the game.
 |      
 |      Returns:
 |          int: The number of jackpots in the game.
 |  
 |  permutation_count(self)
 |      This method will compute unique permutations of faces rolled, along with their counts.
 |      
 |      Returns:
 |          pandas DataFrame with distinct permutations and associated counts.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
