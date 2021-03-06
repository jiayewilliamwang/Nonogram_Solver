#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup

import re


class PuzzleCrawler:
    def __init__(self, puzzle_id: str):
        self._hex_color_pattern = re.compile("#(?:[0-9a-fA-F]{3}){2}")

        puzzle_url = f"https://www.nonograms.org/nonograms2/i/{puzzle_id}"
        self._driver = webdriver.Chrome()

        self._driver.get(puzzle_url)

        self._puzzle_grid = self._get_puzzle_grid()
        self._n = len(self._puzzle_grid)
        self._m = len(self._puzzle_grid[0])

        self._soup = BeautifulSoup(self._driver.page_source, "html.parser")

        self._color_table = self._get_color_table()
        self._row_groups = self._get_row_groups()
        self._col_groups = self._get_col_groups()
        self._color_panel = self._get_color_panel()

    def _get_color_panel(self):
        return self._driver.find_element_by_id("nmti")

    def _get_color_table(self) -> dict:
        color_table_element = self._soup.find("table", {
            "class": "nonogram_color_table"})
        colors = self._hex_color_pattern.findall(str(color_table_element))
        color_table = {"#ffffff": 0}
        for i in range(len(colors)):
            color_table[colors[i]] = i + 1
        return color_table

    def _get_puzzle_grid(self) -> list:
        puzzle_grid = self._driver.find_elements_by_xpath(
            '//*[@id="nonogram_table"]/tbody/tr[2]/td[2]/table/tbody/tr')
        grid = []
        for row in puzzle_grid:
            grid.append(row.find_elements_by_tag_name("td"))
        return grid

    def _get_row_groups(self) -> list:
        row_groups = []
        rows_element = self._soup.find("td", {"class": "nmtl"}).find_all("tr")
        for row in rows_element:
            cur_row = []
            for col in row.find_all("td"):
                if col.has_attr("style"):
                    color = self._hex_color_pattern.findall(col["style"])[0]
                    pair = [int(col.get_text()), self._color_table[color]]
                    cur_row.append(pair)
            row_groups.append(cur_row)
        return row_groups

    def _get_col_groups(self) -> list:
        col_groups = [[] for _ in range(self._m)]
        cols_element = self._soup.find("td", {"class": "nmtt"}).find_all("tr")
        for col in cols_element:
            cur = col.find_all("td")
            for i in range(len(cur)):
                if cur[i].has_attr("style"):
                    color = self._hex_color_pattern.findall(cur[i]["style"])[0]
                    pair = [int(cur[i].get_text()), self._color_table[color]]
                    col_groups[i].append(pair)
        return col_groups

    # ----- Getters -----
    @property
    def puzzle_grid(self) -> list:
        return self._puzzle_grid

    @property
    def color_table(self) -> dict:
        return self._color_table

    @property
    def col_groups(self) -> list:
        return self._col_groups

    @property
    def row_groups(self) -> list:
        return self._row_groups

    @property
    def color_panel(self):
        return self._color_panel
