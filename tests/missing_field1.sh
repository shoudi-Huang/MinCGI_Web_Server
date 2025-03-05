sleep 2
python3 ../webserv.py broken_cfg1.cfg | diff - missing_field.out
