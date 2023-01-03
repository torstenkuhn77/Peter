#!/usr/bin/env python3
# shell : python3 /home/pi/skripts/prod/Smart_Home.py
#         @/usr/bin/python3 /home/pi/skripts/prod.Smart_Home.py

# Dieses Skript ruft das Skript "testskript.py" auf
# im aufgerufenen Skript muß an erster Stelle "#!/usr/bin/env python" erscheinen (shebang)
# siehe  https://einfachpython.de/scripte-in-python-usrbinenv-python/

import os
os.system('/home/pi/Desktop/prod/Smart_Home_testskript.py')
