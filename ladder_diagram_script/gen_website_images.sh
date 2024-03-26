THEME="--default-color white --palette palette.txt"
SIZING="--margin 6 --line-width 5 --beat-spacing 20 --track-spacing 25"
COMMAND="python ladder_diagram.py $SIZING $THEME --siteswap"

$COMMAND 534 --colors red,blue,orange,white --total-beats 18 --out ../images/534.png

$COMMAND 030 --colors white,orange,white --total-beats 6 --out ../images/030.png

$COMMAND 3 --colors orange,blue,red --total-beats 6 --out ../images/3.png

$COMMAND 441 --colors orange,blue,red --total-beats 18 --out ../images/441.png

$COMMAND 645 --colors orange,blue,red,orange,white --total-beats 18 --out ../images/645.png

rm *.svg
