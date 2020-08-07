#!/usr/bin/env python
# -*- coding: utf-8 -*-


class OneLineSolver:
    def __init__(self, side_length: int):
        self._cache = [[0] * (side_length + 1)
                       for _ in range(side_length + 1)]
        self._calc_fill = [[0] * (side_length + 1)
                           for _ in range(side_length + 1)]
        self._cache_cnt = 0

        self._result_cell = [0] * side_length

    @staticmethod
    def _can_place_color(cells, color, l_bound, r_bound):
        if r_bound >= len(cells):
            return False
        mask = 1 << color
        for i in range(l_bound, r_bound + 1):
            if (cells[i] & mask) == 0:
                return False
        return True

    def _set_place_color(self, color, l_bound, r_bound):
        for i in range(l_bound, r_bound + 1):
            self._result_cell[i] |= (1 << color)

    def _can_fill(self, groups, cells, current_group=0, current_cell=0):
        if current_cell == len(cells):
            return current_group == len(groups)
        cached = self._cache[current_group][current_cell]
        answer = self._calc_fill[current_group][current_cell]
        if cached == self._cache_cnt:
            return answer
        answer = 0
        if self._can_place_color(cells, 0, current_cell, current_cell) and self._can_fill(groups, cells, current_group, current_cell + 1):
            self._set_place_color(0, current_cell, current_cell)
            answer = 1
        if current_group < len(groups):
            current_color = groups[current_group][1]
            l_bound = current_cell
            r_bound = current_cell + groups[current_group][0] - 1

            can_place = self._can_place_color(cells, current_color, l_bound, r_bound)
            place_white = False

            next_cell = r_bound + 1
            if can_place:
                if current_group + 1 < len(groups) and groups[current_group + 1][1] == current_color:
                    place_white = True
                    can_place = self._can_place_color(cells, 0, next_cell, next_cell)
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

    def update_state(self, groups, cells):
        self._cache_cnt += 1
        self._result_cell = [0] * len(cells)
        if not self._can_fill(groups, cells):
            return False
        for i in range(len(cells)):
            cells[i] = self._result_cell[i]
        return True


# if __name__ == '__main__':
#
#     obj = OneLineSolver(32)
#     cell = [[255] * 32 for _ in range(32)]
#     groups = [[],
#                         [[10, 2]],
#                         [[2, 2], [2, 3], [5, 4], [3, 3], [2, 2]],
#                         [[3, 2], [1, 3], [10, 5], [1, 3], [3, 2]],
#                         [[2, 2], [1, 4], [3, 5], [2, 4], [4, 5], [2, 4], [3, 5],
#                          [1, 4],
#                          [2, 2]],
#                         [[1, 2], [1, 3], [1, 4], [1, 5], [14, 4], [1, 5],
#                          [1, 4], [1, 3],
#                          [1, 2]],
#                         [[1, 2], [1, 3], [20, 4], [1, 3], [1, 2]],
#                         [[2, 2], [1, 3], [20, 4], [1, 3], [2, 2]],
#                         [[1, 2], [1, 3], [22, 4], [1, 3], [1, 2]],
#                         [[2, 2], [2, 3], [20, 4], [2, 3], [2, 2]],
#                         [[1, 2], [26, 3], [1, 2]],
#                         [[1, 2], [4, 3], [3, 6], [12, 3], [3, 6], [4, 3],
#                          [1, 2]],
#                         [[1, 2], [4, 3], [2, 6], [16, 3], [2, 6], [4, 3],
#                          [1, 2]],
#                         [[1, 2], [3, 3], [2, 6], [18, 3], [2, 6], [3, 3],
#                          [1, 2]],
#                         [[1, 2], [2, 3], [2, 6], [1, 3], [6, 6], [6, 3], [6, 6],
#                          [1, 3],
#                          [2, 6], [2, 3], [1, 2]],
#                         [[1, 2], [2, 3], [1, 6], [1, 3], [2, 6], [1, 7], [5, 6],
#                          [4, 3],
#                          [5, 6], [1, 7], [2, 6], [1, 3], [1, 6], [2, 3],
#                          [1, 2]],
#                         [[1, 2], [4, 3], [3, 7], [4, 3], [1, 6], [4, 3], [1, 6],
#                          [4, 3],
#                          [3, 7], [4, 3], [1, 2]],
#                         [[1, 2], [2, 3], [2, 7], [1, 5], [2, 7], [14, 3],
#                          [2, 7], [1, 5],
#                          [2, 7], [2, 3], [1, 2]],
#                         [[1, 2], [1, 3], [2, 7], [2, 5], [1, 7], [16, 3],
#                          [1, 7], [2, 5],
#                          [2, 7], [1, 3], [1, 2]],
#                         [[1, 2], [3, 7], [2, 5], [1, 7], [16, 6], [1, 7],
#                          [2, 5], [3, 7],
#                          [1, 2]],
#                         [[3, 7], [3, 5], [1, 7], [16, 5], [1, 7], [3, 5],
#                          [3, 7]],
#                         [[3, 7], [2, 5], [2, 7], [16, 5], [2, 7], [2, 5],
#                          [3, 7]],
#                         [[7, 7], [16, 6], [7, 7]],
#                         [[7, 7], [16, 6], [7, 7]],
#                         [[5, 7], [2, 3], [14, 6], [2, 3], [5, 7]],
#                         [[3, 7], [4, 3], [12, 6], [4, 3], [3, 7]],
#                         [[1, 2], [6, 3], [8, 6], [6, 3], [1, 2]],
#                         [[2, 2], [6, 3], [4, 6], [6, 3], [2, 2]],
#                         [[2, 2], [12, 3], [2, 2]],
#                         [[2, 2], [8, 3], [2, 2]],
#                         [[8, 2]],
#                         []
#                         ]
#     # groups = [[2, 3], [2, 3]]
#
#     for i in range(len(groups)):
#         obj.update_state(groups[i], cell[i])
#     [print(i) for i in cell]
#     # print(obj.update_state(groups, cell))
#     # group = [[3, 2], [1, 3], [10, 5], [1, 3], [3, 2]]
#     # cell = [255] * 32
#     # obj.update_state(group, cell)
#     # print(cell)
