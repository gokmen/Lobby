
install:
	cp -rf lobby /usr/lib/python2.7/site-packages/
	ln -s /usr/lib/python2.7/site-packages/lobby/server.py /usr/bin/lobby-server
	chmod +x /usr/lib/python2.7/site-packages/lobby/server.py
	ln -s /usr/lib/python2.7/site-packages/lobby/client.py /usr/bin/lobby-client
	chmod +x /usr/lib/python2.7/site-packages/lobby/client.py

uninstall:
	rm -rf /usr/lib/python2.7/site-packages/lobby
	rm -rf /usr/bin/lobby-client /usr/bin/lobby-server

clean:
	find -name *.pyc | xargs rm -rf

