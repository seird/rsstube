build: clean
	pip install -r requirements.txt
	pip install pyinstaller
	pyinstaller rss-tube.spec
	cp -r debian build/debian
	mkdir build/debian/usr/lib
	cp -r dist/rsstube build/debian/usr/lib/rsstube
	dpkg -b build/debian dist/rsstube_amd64.deb

build-macos: clean
	pip install -r requirements.txt
	pip install pyinstaller
	pip install Pillow
	pyinstaller rss-tube-macos.spec

install: build
	sudo dpkg -i dist/rsstube_amd64.deb

uninstall:
	sudo dpkg -r rsstube

clean:
	rm -rf dist build
