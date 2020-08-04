from OneLineSolver import OneLineSolver
from PuzzleCrawler import PuzzleCrawler


class Puzzle:
    def __init__(self, puzzle_id: str):
        self._crawler = PuzzleCrawler(puzzle_id)

        self._row_groups = self._crawler.row_group
        self._col_groups = self._crawler.col_group

        self._color_count = len(self._crawler.color_table)

        self._n, self._m = len(self._row_groups), len(self._col_groups)
        self._row_masks = [[(1 << self._color_count) - 1] * self._m
                           for _ in range(self._n)]
        self._col_masks = [[(1 << self._color_count) - 1] * self._n
                           for _ in range(self._m)]

        self._solver = OneLineSolver(max(self._n, self._m))

    def solve(self) -> bool:
        dead_rows = [False] * self._n
        dead_cols = [False] * self._m
        prev_sum = float("inf")
        while True:
            [print(i) for i in self._row_masks]
            print("-----------------------")
            if not self._update_state(self._solver, dead_rows, dead_cols):
                print("Can't update the puzzle state")
                return False
            cur_sum = self._update_cell_values()
            if cur_sum == prev_sum:
                print("The solution process has stopped")
                break
            prev_sum = cur_sum
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

    def _update_groups_state(self, solver: OneLineSolver, dead: list,
                             groups: list, masks: list):
        for i in range(len(groups)):
            if not dead[i]:
                # self._update_cell_values()
                if not solver.update_state(groups[i], masks[i]):
                    return False
                is_dead = True
                for num in masks[i]:
                    if bin(num).count('1') != 1:
                        is_dead = False
                        break
                dead[i] = is_dead
                # self._update_cell_values()
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


if __name__ == '__main__':
    puzzle = Puzzle("4374")
    puzzle.solve()
