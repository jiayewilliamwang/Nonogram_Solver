from selenium import webdriver

import re


class PuzzleCrawler:
    def __init__(self):
        puzzle_url = "https://www.nonograms.org/nonograms/i/4353"
        self._driver = webdriver.Chrome()
        self._driver.get(puzzle_url)

        # _row_ele contains both the horizontal block groups length and the grid
        self._col_ele, self._row_ele = self._driver.find_elements_by_xpath(
            '//*[@id="nonogram_table"]/tbody/tr')

        self._col, self._row = self.get_puzzle_size()

    def get_puzzle_size(self):
        """
        Get the size of the puzzle: number of column and row.
        :return: list of two integers, [col, row] where col is number of column
            and row is number of row
        """
        size_element = self._driver.find_element_by_xpath(
            "//div[@class='content']//table//tbody//tr//td")
        return [int(s) for s in re.findall(r'\d+', size_element.text)]

    def get_puzzle_grid(self):
        """
        Get the grid of the puzzle. It is going to be modified and
        synchronized when solving the puzzle. Moreover, visualize the solving
        process.
        :return: list of lists of selenium elements, where size equals to
            _row. Each sub-list has same size equal to _col.
        """
        puzzle_grid = self._row_ele.find_elements_by_xpath(
            "./td[@class='nmtc']/table/tbody/tr")
        grid = []
        for row in puzzle_grid:
            cur_row = []
            for cell in row.find_elements_by_xpath(".//td"):
                cur_row.append(cell)
            grid.append(cur_row)
        return grid

    def get_col_numbers(self):
        """
        Get the horizontal block groups length.
        :return: list of lists of integers that has length _col. Each sublist
            may not have the same size, but none of them will be empty. The
            summation of each sublist will not be greater than _col.
        """
        col_elements = self._col_ele.find_elements_by_xpath(
            "./td[@class='nmtt']/table/tbody/tr")

        # Note: column elements is different than then row elements. It
        # distributes same as rows, but we need to do some reformation.
        ans = [[] for _ in range(self._col)]
        for col in col_elements:
            temp = col.find_elements_by_xpath("./td")
            for i in range(len(temp)):
                if temp[i].get_attribute("class") == "num":
                    ans[i].append(int(temp[i].text))
        return ans

    def get_row_numbers(self):
        """
        Get the vertical block groups length.
        :return: list of lists of integer that has length _row. Each sublist
            may not have the same size, but none of them will empty. The
            summation of each sublist will not be greater than _row.
        """
        row_elements = self._row_ele.find_elements_by_xpath(
            "./td[@class='nmtl']/table/tbody/tr")

        ans = []
        for row in row_elements:
            cur_row = []
            for cell in row.find_elements_by_xpath("./td[@class='num']"):
                cur_row.append(int(cell.text))
            ans.append(cur_row)
        return ans
