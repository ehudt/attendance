#!/bin/bash
# compress attendance.py output to save space and avoid clutter
COUNTER=`cat counter`
if [ $RESULT -ne 0 ]
then
	COUNTER=1
fi
cd tmp
tar -czvf attendance.$COUNTER.tgz attendance-* 2>&1 >/dev/null
RESULT=$?
cd -
if [ $RESULT -eq 0 ]
then
	rm ~/attendance/tmp/attendance-*
	COUNTER=`expr $COUNTER + 1`
	echo $COUNTER > counter
fi

