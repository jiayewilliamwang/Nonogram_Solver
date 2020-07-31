from selenium import webdriver


class PuzzleCrawler:
    def __init__(self):
        puzzle_url = "https://www.nonograms.org/nonograms2/i/4374"
        self._driver = webdriver.Chrome()
        self._driver.get(puzzle_url)

        # _row_ele contains both the horizontal block groups length and the grid
        self._col_ele, self._row_ele = self._driver.find_elements_by_xpath(
            '//*[@id="nonogram_table"]/tbody/tr')

        self._puzzle_grid = self._get_puzzle_grid()
        self._color_table = self._get_color_table()

        self._col_group = self._get_col_groups()
        self._row_group = self._get_row_groups()

    def _get_color_table(self) -> dict:
        """
        Get the color table of the puzzle.
        Add color white and value 0 as default.
        :return: {bg_color: i} where bg_color is in "rbga(r, g, b, a)" format.
        i is in range 0 to n, where n is number of colors, exclusive white.
        """
        color_table_ele = self._driver.find_elements_by_xpath(
            "//table[@class='nonogram_color_table']/tbody/tr/td")

        color_table = {"rgba(255, 255, 255, 1)": 0}
        for color in color_table_ele:
            bg_color = color.value_of_css_property("background-color")
            color_table[bg_color] = int(color.text)
        return color_table

    def _get_puzzle_grid(self) -> list:
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
            for cell in row.find_elements_by_xpath("./td"):
                cur_row.append(cell)
            grid.append(cur_row)
        return grid

    def _get_row_groups(self) -> list:
        """
        Get the horizontal colored groups.
        :return: list of lists of pair of integers. Each sublist's length will
            be at least 1, represents the colored groups of each row. For each
            color group is in [length: int, color-reference: int] format.
        """
        row_elements = self._row_ele.find_elements_by_xpath(
            "./td[@class='nmtl']/table/tbody/tr")

        ans = []
        for row in row_elements:
            cur_row = []
            for cell in row.find_elements_by_xpath("./td[@class='num']"):
                bg_color = cell.value_of_css_property("background-color")
                cur_row.append([int(cell.text), self._color_table[bg_color]])
            ans.append(cur_row)
        return ans

    def _get_col_groups(self) -> list:
        """
        Get the vertical colored groups.
        :return: list of lists of pair of integers. Each sublist's length will
            be at least 1, represents the colored groups of each col. For each
            color group is in [length: int, color-reference: int] format.
        """
        col_elements = self._col_ele.find_elements_by_xpath(
            "./td[@class='nmtt']/table/tbody/tr")

        ans = [[] for _ in range(len(self._puzzle_grid[0]))]
        for col in col_elements:
            temp = col.find_elements_by_xpath("./td")
            for i in range(len(temp)):
                if temp[i].get_attribute("class") == "num":
                    bg_color = temp[i].value_of_css_property("background-color")
                    ans[i].append([int(temp[i].text), self._color_table[bg_color]])
        return ans

    # ----- Getters -----
    @property
    def puzzle_grid(self) -> list:
        return self._puzzle_grid

    @property
    def color_table(self) -> dict:
        return self._color_table

    @property
    def col_group(self) -> list:
        return self._col_group

    @property
    def row_group(self) -> list:
        return self._row_group
