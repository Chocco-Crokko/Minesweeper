import unittest
import Parser


class ParserTest(unittest.TestCase):
    def test_get_area(self):
        first = [(0, 1), (1, 0), (1, 1)]
        self.assertEqual(first, Parser.get_area(0, 0, 4, 3))

        second = [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]
        self.assertEqual(second, Parser.get_area(0, 1, 4, 3))

        third = [(2, 1), (2, 2), (3, 1)]
        self.assertEqual(third, Parser.get_area(3, 2, 4, 3))

    def test_parse(self):
        field, m, n, _ = Parser.parse_field('input1')
        self.assertEqual(4, m)
        self.assertEqual(3, n)

        self.assertEqual(4, field[1][1])
        self.assertEqual(2, field[2][1])

        for i in (0, 3):
            for j in range(3):
                self.assertEqual(Parser.EMPTY_CELL, field[i][j])

        for i in (1, 2):
            for j in (0, 2):
                self.assertEqual(Parser.EMPTY_CELL, field[i][j])

    def test_get_groups(self):
        groups = Parser.parse_groups('input1')

        group = groups[0]
        cells = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)}
        self.assertEqual(4, group.w)
        self.assertEqual(cells, group.cells)

        group = groups[1]
        cells = {(1, 0), (1, 2), (2, 0), (2, 2), (3, 0), (3, 1), (3, 2)}
        self.assertEqual(2, group.w)
        self.assertEqual(cells, group.cells)
