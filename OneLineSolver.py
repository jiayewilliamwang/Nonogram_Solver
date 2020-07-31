#!/usr/bin/env python
# -*- coding: utf-8 -*-


class OneLineSolver:
    def __init__(self, side_length: int):
        self._cache = [[0] * side_length for _ in range(side_length)]   # *
        self._calc_fill = [[0] * side_length for _ in range(side_length)]
        self._cache_cnt = 0

        self._result_cell = [None] * side_length

    def update_state(self, groups: list, cells: list) -> bool:
        self._cache_cnt += 1
        self._result_cell = [0] * len(cells)
        if not self._can_fill(groups, cells):
            return False
        cells[:] = self._result_cell
        return True

    def _can_fill(self, groups: list, cells: list,
                  cur_group=0, cur_cell=0) -> int:
        if cur_cell == len(cells):
            return cur_group == len(groups)
        cached = self._cache[cur_group][cur_cell]
        answer = self._calc_fill[cur_group][cur_cell]
        if cached == self._cache_cnt:
            return answer

        if self._can_place_color(cells, 0, cur_cell, cur_cell) \
                and self._can_fill(groups, cells, cur_group, cur_cell + 1):
            self._set_place_color(0, cur_cell, cur_cell)
            answer = 1

        if cur_group < len(groups):
            cur_color = groups[cur_group][1]
            l_bound = cur_cell
            r_bound = cur_cell + groups[cur_group][0] - 1

            can_place = self._can_place_color(cells, cur_color, l_bound, r_bound)
            place_white = False

            next_cell = r_bound + 1
            if can_place:
                if cur_group + 1 < len(groups) and \
                        groups[cur_group + 1][1] == cur_color:
                    place_white = True
                    can_place = self._can_place_color(cells, 0, next_cell, next_cell)
                    next_cell += 1
            if can_place:
                if self._can_fill(groups, cells, cur_group + 1, next_cell):
                    answer = 1
                    self._set_place_color(cur_color, l_bound, r_bound)
                    if place_white:
                        self._set_place_color(0, r_bound + 1, r_bound + 1)
        self._calc_fill[cur_group][cur_cell] = answer
        self._cache[cur_group][cur_cell] = self._cache_cnt
        return answer

    def _set_place_color(self, color: int, l_bound: int, r_bound: int) -> None:
        for i in range(l_bound, r_bound + 1):
            self._result_cell[i] |= (1 << color)

    @staticmethod
    def _can_place_color(cells: list, color: int,
                         l_bound: int, r_bound: int) -> bool:
        if r_bound >= len(cells):
            return False
        mask = 1 << color
        for i in range(l_bound, r_bound + 1):
            if not (cells[i] & mask):
                return False
        return True


if __name__ == '__main__':

    obj = OneLineSolver(5)
    cell = [15, 15, 15, 15, 15]
    # groups = [[2, 3], [2, 3]]
    groups = [[4, 3]]
    print(obj.update_state(groups, cell))
    print(cell)
