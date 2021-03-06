
install:
	cp -rf lobby /usr/lib/python*/site-packages/
	rm -rf /usr/bin/lobby-server
	ln -s /usr/lib/python*/site-packages/lobby/server.py /usr/bin/lobby-server
	chmod +x /usr/lib/python*/site-packages/lobby/server.py
	rm -rf /usr/bin/lobby-client
	ln -s /usr/lib/python*/site-packages/lobby/client.py /usr/bin/lobby-client
	chmod +x /usr/lib/python*/site-packages/lobby/client.py

uninstall:
	rm -rf /usr/lib/python*/site-packages/lobby
	rm -rf /usr/bin/lobby-client /usr/bin/lobby-server

clean:
	find -name *.pyc | xargs rm -rf

