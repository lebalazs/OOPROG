from szoba import Szoba, EgyagyasSzoba, KetagyasSzoba
from szalloda import Szalloda
import datetime
from termcolor import colored

class Foglalas:
    def __init__(self, szalloda: Szalloda):
        self._szalloda = szalloda
        self._foglalasok = []

    @property 
    def szalloda(self):
        return self._szalloda


    def foglalas(self, szobaszam:int, datum: datetime):
        sz = self.checkSzoba(szobaszam)
        if not isinstance(sz, Szoba):
            print("NINCS ILYEN SZOBA")
        else:
            #print(sz.leiras())
            i = self._searchFoglalas(szobaszam,datum)
            if i>=0:
                if self._foglalasok[i][2] != 'T':
                    self._foglalasok[i][2] = 'T'
                    return sz.ar
                else:
                    raise ValueError('Ez a szoba ebben az időpontban már foglalt!')
            else:
                self._foglalasok.append([szobaszam,datum,'T'])
                return sz.ar

    def lemondas(self, szobaszam:int, datum: datetime):
        i = self._searchFoglalas(szobaszam,datum)
        if i>=0 and self._foglalasok[i][2]=='T':
            self._foglalasok[i][2] = 'C'
        else:
            raise ValueError('Ez a szoba ebben az időpontban nem foglalt!')
    
    def checkSzobaStatus(self, szobaszam:int, datum: datetime):
        ret = 'F' #F=Szabad, T=foglalt, C=Lemondott
        i = self._searchFoglalas(szobaszam,datum)
        if i>=0:
            ret = self._foglalasok[i][2]
        match ret:
            case 'T':  return 'Foglalt'
            case 'C':  return 'Lemondott'
            case 'F':  return 'Szabad'
    
    def checkSzoba(self,szobaszam:int) -> Szoba:
        return self._szalloda.checkSzoba(szobaszam)
    
    def _searchFoglalas(self, szobaszam:int, datum: datetime) -> int:
        ret = -1
        for i in range(len(self._foglalasok)):
            if self._foglalasok[i][0] == szobaszam and self._foglalasok[i][1] == datum:
                ret=i
                break
        return ret   

    def showFoglalas(self):
        print(colored("Foglalások","yellow"))
        for fogl in self._foglalasok:
            match fogl[2]:
                case 'T':  statusz = 'Foglalt'
                case 'C':  statusz = 'Lemondott'
                case 'F':  statusz = 'Szabad'
            
            print(f"Szoba: {fogl[0]} - Dátum: {fogl[1]}: {statusz}")


