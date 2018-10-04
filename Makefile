Memory:
	echo "#!/bin/bash" > Memory
	echo "pypy3 memory.py \"\$$@\"" >> Memory
	chmod u+x Memory
