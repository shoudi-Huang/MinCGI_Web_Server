cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl -I localhost:8070/test.png | grep 'Content-Type' | diff - png_contentType_expected.out 
echo
sleep 2
curl localhost:8070/test.xml | diff - xml_expected.out
echo
sleep 2
curl -I localhost:8070/test.xml | grep 'Content-Type' | diff - xml_contentType_expected.out
echo
sleep 2
curl -I localhost:8070/test.jpg | grep 'Content-Type' | diff - jpg_contentType_expected.out
echo
sleep 2
curl -I localhost:8070/test.jpeg | grep 'Content-Type' | diff - jpeg_contentType_expected.out
kill $PID
