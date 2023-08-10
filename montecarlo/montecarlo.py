import pandas as pd
import numpy as np
import random

class Die:
    """
    Fibricates a 'die' object that has specified faces and weights.

    Attributes:
        _die_data (pandas.DataFrame): This is the dataframe that stores face values and weights.
    """

    def __init__(self, faces: np.ndarray):
        """
        Initializes the die object with specified 'faces'.

        Args:
            faces (numpy.ndarray): An array containing distinct face values of the die.

        Raises:
            TypeError: If faces is not a NumPy array.
            ValueError: If faces do not have distinct values.
        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("Input must be a NumPy array.")

        if len(faces) != len(np.unique(faces)):
            raise ValueError("Faces must have distinct values.")

        weights = np.ones_like(faces, dtype=float)
        data = {'Weights': weights}
        if np.issubdtype(faces.dtype, np.number):
            self._die_data = pd.DataFrame(data, index=faces)
        else:
            self._die_data = pd.DataFrame(data, index=faces.astype(str))

    def set_weight(self, face, weight):
        """
        This controls the weight for a specific face value.

        Arguments:
            face: The face value for which the weight is to be set.
            weight: The weight value assigned.

        Raises:
            IndexError: If the face value is invalid.
            TypeError: If the weight is not a numeric value.
        """
        if face not in self._die_data.index:
            raise IndexError("Invalid face value.")
        if not (isinstance(weight, (int, float)) or np.issubdtype(type(weight), np.number)):
            raise TypeError("Weight must be a numeric value or castable as numeric.")

        self._die_data.loc[face, 'Weights'] = weight

    def roll(self, num_rolls: int = 1) -> list:
        """
        This method simulates rolling of the die multiple times.

        Argument:
            num_rolls (int): The number of times the die is rolled.

        Returns:
            list: A list of outcomes from rolling the die.
        """
        outcomes = random.choices(self._die_data.index, weights=self._die_data['Weights'], k=num_rolls)
        return outcomes

    def get_die_state(self) -> pd.DataFrame:
        """
        This will return a copy of the die's data frame.

        Returns:
            pandas.DataFrame: A copy of the die data frame.
        """
        return self._die_data.copy()


class Game:
    """
    The game class contains a game consisting of rolling multiple dice.

    Attributes:
        dice: A list of Die objects representing the dice in the game.
        play_data: Data frame that stores the results of the most recent play.
    """
    def __init__(self, dice):
        """
        This initializes the Game class with a list of similar dice.
        This also checks if the list contains Die objects
        Argusment:
            dice (list): A list of already instantiated similar dice (Die objects).
        """
        # Check if the list contains Die objects
        if not all(isinstance(die, Die) for die in dice):
            raise ValueError('All elements in the list must be instances of the Die class.')

        # Check if all dice have the same faces
        faces = set(dice[0].get_die_state().index)
        if not all(set(die.get_die_state().index) == faces for die in dice):
            raise ValueError('All dice must have the same faces.')

        self.dice = dice
        self.play_data = pd.DataFrame()  # Private data frame to store play results

    def play(self, times):
        """
        This method simulates playing the game by rolling the dice a specified number of times.

        Argsuments:
            times (int): The number of times instructed to roll the dice.
        """
        rolls = []
        for i in range(times):
            roll_result = []
            for die in self.dice:
                roll = die.roll()[0]
                roll_result.append(roll)
            rolls.append(roll_result)

        columns = [f"Die_{i}" for i in range(1, len(self.dice) + 1)]
        self.play_data = pd.DataFrame(rolls, columns=columns)

    def show_results(self, form='wide'):
        """
        This method displays the results of the most recent play.

        Args:
            Format options: Options include: 'wide' (default) or 'narrow'

        Returns:
            pandas.DataFrame: The play results data frame.

        Raises:
            ValueError: If an invalid option is provided for the format.
        """
        if form == 'wide':
            return self.play_data.copy()
        elif form == 'narrow':
            narrow_data = pd.DataFrame()
            for idx, col in enumerate(self.play_data.columns):
                rolls = self.play_data[col].tolist()
                roll_numbers = list(range(1, len(rolls) + 1))
                multi_index = pd.MultiIndex.from_tuples([(r, col) for r in roll_numbers], names=['Roll', 'Die'])
                df = pd.DataFrame(rolls, index=multi_index, columns=['Outcome'])
                narrow_data = pd.concat([narrow_data, df])
            return narrow_data
        else:
            raise ValueError("Invalid option for 'form'. Please choose 'wide' or 'narrow'.")

class Analyzer:
    """
    Analyzes the results of a single game and computes various descriptive properties.

    Attributes:
        game (Game): A Game object whose results will be analyzed.
    """

    def __init__(self, game):
        """
        Initializes an Analyzer object with a Game object.

        Args:
            game (Game): A Game object whose results will be analyzed.

        Raises:
            ValueError: If the input is not a Game object.
        """
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")

        self.game = game

    def jackpot(self):
        """
        Jackpot computes the number of jackpot occurrences in the game.

        Returns:
            int: The number of jackpots in the game.
        """
        jackpot_count = 0
        results = self.game.show_results('wide')
        for i, row in results.iterrows():
            if all(value == row.iloc[0] for value in row):
                jackpot_count += 1
        return jackpot_count

    def face_counts_per_roll(self):
        """
        Counts how many times a given face is rolled in each event.

        Returns: A data frame with an index of the roll number, face values as columns,
        and count values in the cells (in the 'wide' format).
        """
        # Getting the distinct faces
        faces = self.game.show_results().melt().value.unique()

        # Initializing a DataFrame to store the counts
        counts_df = pd.DataFrame(columns=faces, index=range(self.game.show_results().shape[0]))

        # Looping through the rolls and computing the counts
        for roll_number, row in self.game.show_results().iterrows():
            counts = row.value_counts()
            for face in faces:
                counts_df.loc[roll_number, face] = counts.get(face, 0)

        return counts_df

    def combo_count(self):
        """
        Determines unique combinations of faces rolled, along with their counts.

        Returns:
            pandas DataFrame with distinct combinations and associated counts.
        """
        results = self.game.show_results('narrow')
        combo_counts = results.groupby('Roll')['Outcome'].apply(tuple).value_counts().reset_index()
        combo_counts.columns = ['Combo', 'Count']
        return combo_counts

    def permutation_count(self):
        """
        This method will compute unique permutations of faces rolled, along with their counts.

        Returns:
            pandas DataFrame with distinct permutations and associated counts.
        """
        results = self.game.show_results('narrow')
        permutation_counts = results.groupby('Roll')['Outcome'].apply(list).value_counts().reset_index()
        permutation_counts.columns = ['Permutation', 'Count']
        return permutation_counts
