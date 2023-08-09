import numpy as np
import pandas as pd
import random

class Die:
    """
    Represents a die with specified faces and weights.

    Attributes:
        faces (numpy.ndarray): An array containing distinct face values of the die.
        weights (numpy.ndarray): Weights associated with each face value.
        _die_data (pandas.DataFrame): Private data frame storing face values and weights.
    """

    def __init__(self, faces):
        """
        Initializes a Die object with specified faces.

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

        self.faces = faces
        self.weights = np.ones_like(faces, dtype=float)
        self._die_data = self._initialize_die_data()

    def _initialize_die_data(self):
        """
        Initializes the private data frame with face values and weights.

        Returns:
            pandas.DataFrame: The initialized data frame.
        """
        data = {'Weights': self.weights}
        if np.issubdtype(self.faces.dtype, np.number):
            data['Faces'] = self.faces
        else:
            data['Faces'] = self.faces.astype(str)
        return data

    def _validate_face(self, face):
        """
        Validates if the given face value is valid for the die.

        Args:
            face: The face value to be validated.

        Raises:
            IndexError: If the face value is invalid.
        """
        if face not in self.faces:
            raise IndexError("Invalid face value.")

    def _validate_weight(self, weight):
        """
        Validates if the given weight is a valid numeric value.

        Args:
            weight: The weight value to be validated.

        Raises:
            TypeError: If the weight is not a numeric value.
        """
        if not (isinstance(weight, (int, float)) or np.issubdtype(type(weight), np.number)):
            raise TypeError("Weight must be a numeric value or castable as numeric.")

    def set_weight(self, face, weight):
        """
        Sets the weight for a specific face value.

        Args:
            face: The face value for which the weight is set.
            weight: The weight value to be set.
        """
        self._validate_face(face)
        self._validate_weight(weight)
        idx = np.where(self.faces == face)[0][0]
        self.weights[idx] = weight

    def roll(self, num_rolls=1):
        """
        Simulates rolling the die multiple times.

        Args:
            num_rolls (int): The number of times the die is rolled.

        Returns:
            list: List of outcomes from rolling the die.
        """
        outcomes = random.choices(self.faces, weights=self.weights, k=num_rolls)
        return outcomes

    def get_die_state(self):
        """
        Returns a copy of the private die data frame.

        Returns:
            pandas.DataFrame: A copy of the die data frame.
        """
        return pd.DataFrame(self._die_data).set_index('Faces')


class Game:
    """
    Represents a game consisting of rolling multiple dice.

    Attributes:
        dice (list): A list of Die objects representing the dice in the game.
        play_data (pandas.DataFrame): Data frame storing the results of the most recent play.
    """

    def __init__(self, dice_list):
        """
        Initializes a Game object with a list of dice.

        Args:
            dice_list (list): A list of Die objects representing the dice in the game.
        """
        self.dice = dice_list
        self.play_data = None

    def play(self, times):
        """
        Simulates playing the game by rolling the dice a specified number of times.

        Args:
            times (int): The number of times to roll the dice.
        """
        rolls = []
        for _ in range(times):
            roll_result = []
            for die in self.dice:
                roll = die.roll()[0]
                roll_result.append(roll)
            rolls.append(roll_result)

        columns = [f"Die_{i}" for i in range(1, len(self.dice) + 1)]
        self.play_data = pd.DataFrame(rolls, columns=columns)

    def show_results(self, form='wide'):
        """
        Displays the results of the most recent play.

        Args:
            form (str): Format for displaying the results. Options: 'wide' (default) or 'narrow'.

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
        Computes the number of jackpot occurrences in the game.

        Returns:
            int: The number of jackpots in the game.
        """
        jackpot_count = 0
        results = self.game.show_results('wide')
        for _, row in results.iterrows():
            if all(value == row.iloc[0] for value in row):
                jackpot_count += 1
        return jackpot_count

    def face_counts_per_roll(self, face_value):
        """
        Computes the counts of a specific face value rolled in each event.

        Args:
            face_value (int or str): The face value to be counted.

        Returns:
            pandas.Series: Series with the count of the specified face value for each roll.
        """
        results = self.game.show_results('narrow')
        face_counts = results[results['Outcome'] == face_value]['Outcome'].groupby('Roll').count()
        return face_counts

    def combo_count(self):
        """
        Computes distinct combinations of faces rolled, along with their counts.

        Returns:
            pandas.DataFrame: DataFrame with distinct combinations and associated counts.
        """
        results = self.game.show_results('narrow')
        combo_counts = results.groupby('Roll')['Outcome'].apply(tuple).value_counts().reset_index()
        combo_counts.columns = ['Combo', 'Count']
        return combo_counts

    def permutation_count(self):
        """
        Computes distinct permutations of faces rolled, along with their counts.

        Returns:
            pandas.DataFrame: DataFrame with distinct permutations and associated counts.
        """
        results = self.game.show_results('narrow')
        permutation_counts = results.groupby('Roll')['Outcome'].apply(list).value_counts().reset_index()
        permutation_counts.columns = ['Permutation', 'Count']
        return permutation_counts

