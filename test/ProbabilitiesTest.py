import unittest
import Parser
import Probabilities


class ProbabilitiesTest(unittest.TestCase):
    def test_get_probs(self):
        game = Parser.parse_game('inputs/input1')

        probs = Probabilities.get_probs(game.groups)
        Probabilities.print_probs(probs, game)

