# Nonogram Solver

This is an online Nonogram solver by using Selenium and dynamic programming. It 
is a command-line based program write in Python. Check [Nonogram](https://en.wikipedia.org/wiki/NonogramA)
for more information. 

The program will use web crawling to get the puzzle from [nonograms.org](https://www.nonograms.org/). 
Then solve the puzzle. Finally, display the solved puzzle on the website. 

The program currently only works with colored-puzzles. Black-white solve features
will be added later. 

I am not the creator of the solving algorithm. Very appreciate this article: 
["Solving colored Japanese crosswords with the speed of light"](https://izaron.github.io/post/solving-colored-japanese-crosswords-with-the-speed-of-light/)
that I found during the pre-project stage. This is most straightforward way to 
achieve my goal among all other articles I searched.  

## Prerequisites

- [Python3.6+](https://www.python.org/downloads/)
    - f-string formatting offered in Python3.6
- Selenium
```shell script
pip install selenium
```
- BeautifulSoup
```shell script
pip install beautifulsoup4
```
- argparse
```shell script
pip install argparse
```
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (recommend to use the latest version)

## TO-DO
- Complete the Usage section
- Add black-white puzzle features
- Fancy the commandline arguments. 