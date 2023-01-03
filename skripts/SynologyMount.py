# mnt
echo "NAS-Server DS-Synology wird verbunden ..."
# Muster aus : https://tangielskyblog.wordpress.com/2019/06/23/raspberry-pi-mit-synology-nas-verbinden/
# sudo mount -t cifs -o credentials=/home/pi/passwd-nas,uid=1000,gid=1000,dir_mode=0700,file_mode=0600,vers=1.0 //daten/home /mnt/daten/home
sudo mount -t cifs -o user=pi,password=ascona2018,domain=WORKGROUP,uid=1000,gid=1000,dir_mode=0700,file_mode=0600,vers=1.0 //DS-Synology/home /mnt/DS-Synology/home



# zum Aushängen :
# sudo umount //DS-Synology/home
# oder alternativ
# sudo umount /mnt/DS-Synology/home