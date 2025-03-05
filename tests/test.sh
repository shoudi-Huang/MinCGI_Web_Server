cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
kill $PID
echo 

i=0
for t in *.sh;
do
	if [ $t != "test.sh" ];
	then
		echo $t
		bash $t
		echo
		i=$((i+1))
	fi
done

echo Finish $i Tests
