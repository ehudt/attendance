#!/bin/bash
# compress attendance.py output to save space and avoid clutter
cd ~ehudtami/attendance
if [ -f "counter" ];
then
	COUNTER=`cat counter`
else
	COUNTER=1
fi

cd tmp
tar -czvf attendance.$COUNTER.tgz attendance-* 2>&1 >/dev/null
RESULT=$?
cd -
if [ "$RESULT" -eq "0" ]
then
	rm ~/attendance/tmp/attendance-*
	COUNTER=`expr $COUNTER + 1`
	echo $COUNTER > counter
fi

