�� Windows �ϰ�װ SQLite
����� SQLite ����ҳ�棬�� Windows ������Ԥ����Ķ������ļ���

����Ҫ���� sqlite-tools-win32-*.zip �� sqlite-dll-win32-*.zip ѹ���ļ���

�����ļ��� C:\sqlite�����ڴ��ļ����½�ѹ��������ѹ���ļ������õ� sqlite3.def��sqlite3.dll �� sqlite3.exe �ļ���

��� C:\sqlite �� PATH ���������������������ʾ���£�ʹ�� sqlite3 �������ʾ���½����

C:\>sqlite3
SQLite version 3.7.15.2 2013-01-09 11:53:05
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite>



�� Linux �ϰ�װ SQLite
Ŀǰ���������а汾�� Linux ����ϵͳ������ SQLite�����ԣ�ֻҪʹ�������������������Ļ������Ƿ��Ѿ���װ�� SQLite��

$ sqlite3
SQLite version 3.7.15.2 2013-01-09 11:53:05
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite>
���û�п�������Ľ������ô����ζ��û���� Linux �����ϰ�װ SQLite����ˣ������ǰ�������Ĳ��谲װ SQLite��

����� SQLite ����ҳ�棬��Դ���������� sqlite-autoconf-*.tar.gz��

�������£�

$ tar xvzf sqlite-autoconf-3071502.tar.gz
$ cd sqlite-autoconf-3071502
$ ./configure --prefix=/usr/local
$ make
$ make install
�������轫�� Linux �����ϰ�װ SQLite�������԰�����������Ľ�����֤��