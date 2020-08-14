#!/usr/bin/env python
# -*- coding: utf-8 -*-


class OneLineSolver:
    def __init__(self, side_length: int) -> None:
        self._cache = [[0] * (side_length + 1)
                       for _ in range(side_length + 1)]
        self._calc_fill = [[0] * (side_length + 1)
                           for _ in range(side_length + 1)]
        self._cache_cnt = 0

        self._result_cell = [0] * side_length

    def update_state(self, groups: list, cells: list) -> bool:
        self._cache_cnt += 1
        self._result_cell = [0] * len(cells)
        if not self._can_fill(groups, cells):
            return False
        for i in range(len(cells)):
            cells[i] = self._result_cell[i]
        return True

    @staticmethod
    def _can_place_color(cells: list, color: int,
                         l_bound: int, r_bound: int) -> bool:
        if r_bound >= len(cells):
            return False
        mask = 1 << color
        for i in range(l_bound, r_bound + 1):
            if (cells[i] & mask) == 0:
                return False
        return True

    def _set_place_color(self, color: int, l_bound: int, r_bound: int) -> None:
        for i in range(l_bound, r_bound + 1):
            self._result_cell[i] |= (1 << color)

    def _can_fill(self, groups: list, cells: list,
                  current_group=0, current_cell=0) -> int:
        if current_cell == len(cells):
            return current_group == len(groups)
        cached = self._cache[current_group][current_cell]
        answer = self._calc_fill[current_group][current_cell]
        if cached == self._cache_cnt:
            return answer
        answer = 0
        if self._can_place_color(cells, 0, current_cell, current_cell) and \
                self._can_fill(groups, cells, current_group, current_cell + 1):
            self._set_place_color(0, current_cell, current_cell)
            answer = 1
        if current_group < len(groups):
            current_color = groups[current_group][1]
            l_bound = current_cell
            r_bound = current_cell + groups[current_group][0] - 1

            can_place = self._can_place_color(cells, current_color,
                                              l_bound, r_bound)
            place_white = False

            next_cell = r_bound + 1
            if can_place:
                if current_group + 1 < len(groups) and \
                        groups[current_group + 1][1] == current_color:
                    place_white = True
                    can_place = self._can_place_color(cells, 0, next_cell,
                                                      next_cell)
                    next_cell += 1
            if can_place:
                if self._can_fill(groups, cells, current_group + 1, next_cell):
                    answer = 1
                    self._set_place_color(current_color, l_bound, r_bound)
                    if place_white:
                        self._set_place_color(0, r_bound + 1, r_bound + 1)
        self._calc_fill[current_group][current_cell] = answer
        self._cache[current_group][current_cell] = self._cache_cnt
        return answer
