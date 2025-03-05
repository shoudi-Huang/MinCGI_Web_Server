sleep 2
python3 ../webserv.py broken_cfg3.cfg | diff - missing_field.out
