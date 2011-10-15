#!/bin/sh
PRE_SNAKE="#\*dojotools\*#"
POS_SNAKE="#_#dojotools#_#"

PRE_PASCAL="#\*class_dojotools\*#"
POS_PASCAL="#_#class_dojotools#_#"

PRE_DOWN="#\*down_dojotools\*#"
POS_DOWN="#_#down_dojotools#_#"

PRE_CAMEL="#\*camel_dojotools\*#"
POS_CAMEL="#_#camel_dojotools#_#"


for FILE in `find . -name "*$PRE_SNAKE*"`; do NEW=`echo $FILE | sed -e "s/$PRE_SNAKE/$POS_SNAKE/"`; mv "$FILE" "$NEW"; done
find . -type f -exec sed -i "s/$PRE_SNAKE/$POS_SNAKE/g" {} ";"

for FILE in `find . -name "*$PRE_PASCAL*"`; do NEW=`echo $FILE | sed -e "s/$PRE_PASCAL/$POS_PASCAL/"`; mv "$FILE" "$NEW"; done
find . -type f -exec sed -i "s/$PRE_PASCAL/$POS_PASCAL/g" {} ";"

for FILE in `find . -name "*$PRE_DOWN*"`; do NEW=`echo $FILE | sed -e "s/$PRE_DOWN/$POS_DOWN/"`; mv "$FILE" "$NEW"; done
find . -type f -exec sed -i "s/$PRE_DOWN/$POS_DOWN/g" {} ";"

for FILE in `find . -name "*$PRE_CAMEL*"`; do NEW=`echo $FILE | sed -e "s/$PRE_CAMEL/$POS_CAMEL/"`; mv "$FILE" "$NEW"; done
find . -type f -exec sed -i "s/$PRE_CAMEL/$POS_CAMEL/g" {} ";"
