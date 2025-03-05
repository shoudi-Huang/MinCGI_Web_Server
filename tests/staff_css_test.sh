cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl localhost:8070/test.css | diff - css_expected.out 
echo
sleep 2
curl -I localhost:8070/test.txt | grep 'Content-Type' | diff - txt_contentType_expected.out
kill $PID
