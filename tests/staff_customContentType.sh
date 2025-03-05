cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl localhost:8070/cgibin/custom_contentType.py | diff - customContentType_expected.out 
echo
sleep 2
curl -I localhost:8070/cgibin/custom_contentType.py | diff - customContentType_contentType_expected.out
kill $PID
