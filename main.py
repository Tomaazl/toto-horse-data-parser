from horse_parser import *
# Usage
if __name__ == "__main__":
    
    hevosdata = parse_lahdot("ohjelmatiedot.R_13.07.2025.pdf") # Korvaa haluamalla käsiohjelmatiedostolla.
    hevosdata.to_excel("Hevosdata_Riihimaki.xlsx", index=False) # Korvaa haluamallasi nimellä.
