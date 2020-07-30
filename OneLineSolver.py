#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class OneLineSolver:
    def __init__(self, side_length, color_count):
        self._cache = np.zeros((side_length + 1, side_length + 1))
        self._calculated_fill = np.zeros((side_length + 1, side_length + 1))
        self._result_cells = np.zeros(side_length, dtype=np.int64)

        self._cache_count = 0

    def update_state(self, groups, cells):
        self._cache_count += 1
        self._result_cells[:len(cells)] = 0

        if not self._can_fill(groups, cells):
            return False

        cells[:] = self._result_cells[:len(cells)]
        return True

    def _can_fill(self, groups, cells, cur_group=0, cur_cell=0):
        if cur_cell == len(cells):
            return cur_group == len(groups)
        cached = self._cache[cur_group][cur_cell]
        ans = self._calculated_fill[cur_group][cur_cell]

        if cached == self._cache_count:
            return ans
        ans = 0

        if self._can_place_color(cells, 0, cur_cell, cur_cell) and \
                self._can_fill(groups, cells, cur_group, cur_cell + 1):
            self._set_place_color(0, cur_cell, cur_cell)
            ans = 1

        if cur_group < len(groups):
            current_color = groups[cur_group][1]
            l_bound = cur_cell
            r_bound = cur_cell + groups[cur_group][0] - 1

            can_place = self._can_place_color(
                cells, current_color, l_bound, r_bound)
            place_white = False

            next_cell = r_bound + 1

            if can_place:
                if cur_group + 1 < len(groups) and \
                        groups[cur_group + 1][1] == current_color:
                    place_white = True
                    can_place = self._can_place_color(
                        cells, 0, next_cell, next_cell)
                    next_cell += 1

            if can_place:
                if self._can_fill(groups, cells, cur_group + 1, next_cell):
                    ans = 1
                    self._set_place_color(current_color, l_bound, r_bound)
                    if place_white:
                        self._set_place_color(0, r_bound + 1, r_bound + 1)

        self._calculated_fill[cur_group][cur_cell] = ans
        self._cache[cur_group][cur_cell] = self._cache_count
        return True

    @staticmethod
    def _can_place_color(cells, color, l_bound, r_bound):
        if r_bound >= len(cells):
            return False
        mask = 1 << color
        for i in range(l_bound, r_bound + 1):
            if not (cells[i] and mask):
                return False
        return True

    def _set_place_color(self, color, l_bound, r_bound):
        for i in range(l_bound, r_bound + 1):
            self._result_cells[i] |= (1 << color)


if __name__ == '__main__':
    side_length_test = 32
    color_count_test = 3
    groups_test = [[10, 2]]
    cells_test = [255 for _ in range(side_length_test)]

    obj = OneLineSolver(side_length_test, color_count_test)
    print(obj.update_state(groups_test, cells_test))
    print(cells_test)
