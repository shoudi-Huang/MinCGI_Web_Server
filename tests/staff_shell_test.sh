cd ..
python3 webserv.py ./tests/shell_config.cfg &
PID=$!
cd -
sleep 2
curl localhost:8070/cgibin/hello.sh | diff - shell_expected.out 
kill $PID
