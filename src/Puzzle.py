from src.OneLineSolver import OneLineSolver
from src.PuzzleCrawler import PuzzleCrawler
from selenium.webdriver.support.color import Color

import math
import argparse


class Puzzle:
    def __init__(self, puzzle_id: str):
        self._crawler = PuzzleCrawler(puzzle_id)

        self._row_groups = self._crawler.row_groups
        self._col_groups = self._crawler.col_groups
        self._puzzle_grid = self._crawler.puzzle_grid

        self._color_table = self._crawler.color_table
        self._color_panel = self._crawler.color_panel

        self._color_count = len(self._color_table)

        self._n, self._m = len(self._row_groups), len(self._col_groups)

        self._row_masks = [[(1 << self._color_count) - 1] * self._m
                           for _ in range(self._n)]
        self._col_masks = [[(1 << self._color_count) - 1] * self._n
                           for _ in range(self._m)]

        self._solver = OneLineSolver(max(self._n, self._m))

    def solve(self) -> bool:
        dead_rows = [False] * self._n
        dead_cols = [False] * self._m
        painted = [[False] * self._m for _ in range(self._n)]

        prev_sum = float("inf")
        while True:
            self._paint(self._row_masks, painted)
            if not self._update_state(self._solver, dead_rows, dead_cols):
                print("Can't update the puzzle state")
                return False
            cur_sum = self._update_cell_values()
            if cur_sum == prev_sum:
                print("The solution process has stopped")
                break
            prev_sum = cur_sum
        self._paint(self._row_masks, painted)
        return True

    def _update_state(self, solver: OneLineSolver, dead_rows: list,
                      dead_cols: list) -> bool:
        row_masks = self._row_masks.copy()
        col_masks = self._col_masks.copy()
        row_groups = self._row_groups.copy()
        col_groups = self._col_groups.copy()

        if not self._update_groups_state(solver, dead_rows,
                                         row_groups, row_masks):
            return False
        if not self._update_groups_state(solver, dead_cols,
                                         col_groups, col_masks):
            return False
        return True

    @staticmethod
    def _update_groups_state(solver: OneLineSolver, dead: list,
                             groups: list, masks: list):
        for i in range(len(groups)):
            if not dead[i]:
                if not solver.update_state(groups[i], masks[i]):
                    return False
                is_dead = True
                for num in masks[i]:
                    if bin(num).count('1') != 1:
                        is_dead = False
                        break
                dead[i] = is_dead
        return True

    def _update_cell_values(self) -> int:
        total = 0
        row_masks = self._row_masks.copy()
        col_masks = self._col_masks.copy()
        for row in range(self._n):
            for col in range(self._m):
                row_masks[row][col] &= col_masks[col][row]
                col_masks[col][row] &= row_masks[row][col]
                total += row_masks[row][col]
        return total

    def _paint(self, masks, painted):
        cur_color = Color.from_string(
            self._color_panel.value_of_css_property("background-color")).hex
        cur_color = self._color_table[cur_color]
        for i in range(self._n):
            for j in range(self._m):
                goal_color = math.log2(masks[i][j])
                if goal_color.is_integer() and not painted[i][j]:
                    if goal_color:
                        self._update_color_panel(cur_color, int(goal_color))
                        self._puzzle_grid[i][j].click()
                        cur_color = int(goal_color)
                    painted[i][j] = True

    def _update_color_panel(self, cur_color, goal_color):
        click_count = (goal_color - cur_color) % (self._color_count - 1)
        for _ in range(click_count):
            self._color_panel.click()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=str)
    args = parser.parse_args()
    puzzle = Puzzle(args.id)
    puzzle.solve()

