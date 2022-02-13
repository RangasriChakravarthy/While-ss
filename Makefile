all:
	rm -rf ./while-ss
	echo "#!/usr/bin/env python3" > ./while-ss
	cat main.py >> ./while-ss
	chmod +x ./while-ss

clean:
	echo "In clean"
