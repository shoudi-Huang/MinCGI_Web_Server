sleep 2
python3 ../webserv.py invalid | diff - invalid_path.out
