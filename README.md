This trilateriation calculator is quite old and outside the game (compared to all Progamming Board-based LUA-implemented ore scanners), and requires installation of external libraries such as python. So my advice is to go here https://github.com/juvenius/du_ez_scanner and grab this in-game Progamming Board-based LUA-implemented EZ ore scanner. In addition, instead of 3-point trilateriation, as all other trilateriation calculators use, EZ scanner uses **4-point trilateriation** that returns you a perfect set of coordinates. I'm leaving my original script here just in case somebody wants it for something.

## Requirements
1) Download & Install Python 3.8: https://www.python.org/downloads/
2) Install "numpy" module via CLI: `pip install numpy` (by default pip is located in Python\Scripts\ folder).

## How to Use
1) Surface area of planet you're currently on:<br>
![](https://i.imgur.com/eyYmTv7.png)
2) 3 sets of coordinates from different places (i.e. walk around, the bigger distance between them, the better results are):<br>
![](https://i.imgur.com/DDBomEX.png)
3) 3 sets of ranges from these coordinates (i.e. one range value for each of the coordinates):<br>
![](https://i.imgur.com/xaXFmGU.png)
4) Input should look like this:<br>
`du_trilateration_calc.py 88888.88 ::pos{0,5,-11.1111,-11.1111,-11.1111} 111 ::pos{0,5,-22.2222,-22.2222,-22.2222} 222 ::pos{0,5,-33.3333,-33.3333,-33.3333} 333`
5) As result you will get two set of coordinates (because 3 spheres have 2 intersection points). Choose the one that seems more viable (or just mine in it's direction to see if you get closer or not).
6) If scanner jumps from one ore vein to another, your entire trilateration attempt is wasted. Best to use it when you have one ore vein that you can't find your way to it.
7) Lack of precision will result in completely wrong results. Correct results with low precision might bring you somewhere within 50~100 meters of ore vein.

## Maximum Precision Guide
1) To get maximum precise ore vein's coordinates you'll need to follow this guide.
2) Walk slowly until your next scan ping.
3) When scan ping happen, ensure that your character is no longer moving. 
4) If your character is sliding or falling even from 1cm of height - repeat attempt.
5) After success, copy coordinates at exactly this spot.
6) Open your scanner in calibration mode and measure pixels from upper to bottom line like this (for me it was 574), it will be your divisor parameter:<br>
![](https://i.imgur.com/qR27q8V.png)
7) While in scanner's calibration mode, measure exact amount of pixels from bottom line to the range identifier (119 on the screenshot in my case):<br>
![](https://i.imgur.com/ADJebV0.png)
8) Follow instruction to get precise coordinates and range for two other points.
9) With all these coordinates input should look like this (with divisor parameter at the very end):<br>
`du_trilateration_calc.py 88888.88 ::pos{0,5,-11.1111,-11.1111,-11.1111} 111 ::pos{0,5,-22.2222,-22.2222,-22.2222} 222 ::pos{0,5,-33.3333,-33.3333,-33.3333} 333 777`
10) Usulay it brings me within 10~30 meters of ore vein and I only have to search for correct location with direction detector, which is piece of cake.
11) Do remember that scanner shows range to the closest ore voxel in ore vein, not to the ore vein's center, thus do not expect it to bring you to the ore vein directly, unless you were extremely lucky and scanner was hooked to the same ore voxel in the ore vein all the time.
