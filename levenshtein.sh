#!/bin/bash
source=$1
q=$2

python3  -c "import time;import Levenshtein as L;print(L.distance('$source','$q'));"
