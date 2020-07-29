from selenium import webdriver


class PuzzleCrawler:
    def __init__(self):
        puzzle_url = "https://www.nonograms.org/nonograms2/i/5660"
        self._driver = webdriver.Chrome()
        self._driver.get(puzzle_url)

        # _row_ele contains both the horizontal block groups length and the grid
        self._col_ele, self._row_ele = self._driver.find_elements_by_xpath(
            '//*[@id="nonogram_table"]/tbody/tr')

        self._puzzle_grid = self.get_puzzle_grid()
        self._color_table = self.get_color_table()

        self._col_group = self.get_col_groups()
        self._row_group = self.get_row_groups()

    def get_color_table(self):
        color_table_ele = self._driver.find_elements_by_xpath(
            "//table[@class='nonogram_color_table']/tbody/tr/td")
        return [color.value_of_css_property("background-color")
                for color in color_table_ele]

    def get_puzzle_grid(self):
        """
        Get the grid of the puzzle. It is going to be modified and
        synchronized when solving the puzzle. Moreover, visualize the solving
        progress
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

    def get_row_groups(self):
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
                bg_color = cell.value_of_css_property("background-color")
                cur_row.append([bg_color, int(cell.text)])
            ans.append(cur_row)
        return ans

    def get_col_groups(self):
        """
        Get the horizontal block groups length.
        :return: list of lists of integers that has length _col. Each sublist
            may not have the same size, but none of them will be empty. The
            summation of each sublist will not be greater than _col.
        """
        col_elements = self._col_ele.find_elements_by_xpath(
            "./td[@class='nmtt']/table/tbody/tr")

        ans = [[] for _ in range(len(self._puzzle_grid[0]))]
        for col in col_elements:
            temp = col.find_elements_by_xpath("./td")
            for i in range(len(temp)):
                if temp[i].get_attribute("class") == "num":
                    bg_color = temp[i].value_of_css_property("background-color")
                    ans[i].append([bg_color, int(temp[i].text)])
        return ans

    @property
    def puzzle_grid(self):
        return self._puzzle_grid

    @property
    def color_table(self):
        return self._color_table

    @property
    def col_group(self):
        return self._col_group

    @property
    def row_group(self):
        return self._row_group


if __name__ == '__main__':
    obj = PuzzleCrawler()
    print(obj.col_group)

