cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl localhost:8070/greetings.html | diff - greetings_expected.out 
echo
sleep 2
curl -I localhost:8070/greetings.html | grep 'Content-Type' | diff - html_contentType_expected.out 
kill $PID
