cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl localhost:8070/home.js | diff - js_expected.out 
echo
sleep 2
curl -I localhost:8070/home.js | grep 'Content-Type' | diff - js_contentType_expected.out 
kill $PID
