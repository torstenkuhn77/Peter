# shell :  python3 /home/pi/skripts/NLW_verb.py
# Netzlaufwerk verbinden :

LW-BUCHSTABE = 'Z'
SERVER       = 'DS-Synology'
SHARE        = 'Sicherungen'
USERNAME     = 'rudi1770'
PASSWORD     = 'Sandra01'

net use LW-BUCHSTABE: \\SERVER\SHARE /user:USERNAME PASSWORD /PERSISTENT:NO


net use Z: \\DS-Synology\Sicherungen /user:rudi1770 Sandra01 /PERSISTENT:NO