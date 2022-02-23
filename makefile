build_container: load_git_submodules
	sudo docker build -t priv-accept:latest priv-accept

load_git_submodules:
	git submodule update --init --recursive

run: clean
	sudo python3 main.py

clean:
	sudo mn -c

