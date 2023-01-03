# shell :  python3 /home/pi/skripts/LoredanasGeschenk.py
# Programmcode zum Ermitteln von Loredanas Geschenk
print ('Loredanas Geschenk , Simulation der Varianten A und B mit den oben vorgegebenen Werten :')
print ()
# Variante A : Jahr 2020 ab August , Promille-Satz vom Vermögen am Quartalsende
# vorgegebende Werte :  #########################################################
Jahr     = '2020'                             # Kalenderjahr
V_EndQ   = [0.00,0.00,4684465.50,5436416.25]  # Vermögen am Quartalsende I bis IV
                                              # Stand 15.12.2020
Promille = 3/1000                             # Promille-Satz
Quartale = {'  I':0,' II':0,'III':2,' IV':3 } # Monate im Quartal I bis IV
                                              # Q1 und Q2 nicht aktiv , Beginn August
# Verarbeitung ##################################################################
iQuartal = 0
Summe    = 0
Text     = ''
for Quartal in Quartale :
    Ergebnis = V_EndQ[iQuartal] * Promille * Quartale.get(Quartal) / 12 
    Ergebnis = round(Ergebnis,1) # runden auf eine Nachkommastelle
    Summe = Summe + Ergebnis
    iQuartal = iQuartal + 1
    Text = Text + '   ' + Quartal + ' ' + str(Ergebnis)+'0 SFR'   
# Ausgabe ######################################################################
print ('Variante A Loredanas Geschenk für das Jahr',Jahr,'in Summe',str(Summe) + '0 SFR')
print ('Quartale' + Text)
print ()

# Variante B : Jahre 2021 folgende , Prozentsatz vom Vermögenszuwachs , min. Fixum
# vorgegebende Werte :  #########################################################
Jahr     = '2021'                             # Kalenderjahr
V_Begff  = 5436416.25                         # Vermögen am Jahresbeginn
V_Endff  = 5580000.00                         # Vermögen am Jahresende
V_Zuwachs= V_Endff - V_Begff                  # Vermögenszuwachs
Prozent  = 10/100                             # Prozentsatz
Fix      = 1000.00                            # Fixum
# Verarbeitung : #################################################################
if V_Zuwachs > 0 :                    # Vermögenszuwachs positiv
    if V_Zuwachs * Prozent < Fix :  # Vermögenszuwachs kleiner Fixum
        Ergebnis = Fix                        # Fixum als Minimum
    else :                                    # Vermögenszuwachs größer Fixum
        Ergebnis = V_Zuwachs * Prozent
else :                                        # Vermögenszuwachs negativ
    Ergebnis = Fix                            # Fixum als Minimum
Ergebnis  = round(Ergebnis,1)                 # runden auf eine Nachkommastelle
V_Zuwachs = round(V_Zuwachs,1)
# Ausgabe ######################################################################
print ('Variante B Loredanas Geschenk für das Jahr',Jahr,'ff',str(Ergebnis) + '0 SFR')
print ('Vermögenszuwachs ' + str(V_Zuwachs) + '0 SFR')
print ('(bei Variante B sind Zu-/Abgänge während des Jahres noch nicht berücksichtigt , ')
print ('wie ist der Algorithmus ? )')


# # output nach Programmlauf : ###################################################
# 
# Loredanas Geschenk , Simulation der Varianten A und B mit den oben vorgegebenen Werten :
# 
# Variante A Loredanas Geschenk für das Jahr 2020 in Summe 6419.50 SFR
# Quartale     I 0.00 SFR    II 0.00 SFR   III 2342.20 SFR    IV 4077.30 SFR
# 
# Variante B Loredanas Geschenk für das Jahr 2021 ff 14358.40 SFR
# Vermögenszuwachs 143583.80 SFR
# (bei Variante B sind Zu-/Abgänge während des Jahres noch nicht berücksichtigt , 
# wie ist der Algorithmus ? )
