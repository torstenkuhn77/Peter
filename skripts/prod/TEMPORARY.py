        ##### neue Routine ##############################################################
        SEN = GVS.SensList[i]                     # (i2) Sensor     aus GVS.SensList
        STP = str(GVS.SensTab.get(SEN + '_Stp'))  # (i1) timestamp  aus GVS.SensTab
        TMP = str(GVS.SensTab.get(SEN + '_Tmp'))  # (i3) Temperatur aus GVS.SensTab
        if 'Fehler' in STP :                      # Sensor Auslesen war fehlerhaft
            STP = "\n" + 20 * ' ' + Fore.RED + STP
        else :
            STP = Fore.GREEN                      # Sensor Auslesen war korrekt
        TextzuSEN = STP + ' '  + SEN + ' ' + TMP + ' '
        if i == 0 :
            TextzuSEN = 19 * ' ' + TextzuSEN
        Text = TextzuSEN + Text
        ##### neue Routine ##############################################################