from szoba import Szoba, EgyagyasSzoba, KetagyasSzoba

class Szalloda:
    def __init__(self, nev: str):
        self._nev = nev
        self.szobak = []

    @property 
    def nev(self):
        return self._nev


    def addSzoba(self, szoba: Szoba):
        if isinstance(szoba, Szoba):
            szsz=0
            for szszoba in self.szobak:
                if szoba.szobaszam == szszoba.szobaszam:
                    szsz=1
                    break
            if szsz == 1:
                raise ValueError('Ez a szobaszám már létezik. Nem tudom felvenni a szobát ebbe a szállóba!')
            else:
                self.szobak.append(szoba)                
        else:
            raise TypeError("Csak Szoba típusú objektumokat lehet hozzáadni.")
        
    def checkSzoba(self, szobaszam:int) -> Szoba:
        for sz in self.szobak:
            if sz.szobaszam == szobaszam:
                return sz
        raise TypeError("Nincsen ilyen szoba.")
            

    def leiras(self):
        leirasok = [szoba.leiras() for szoba in self.szobak]
        return f"Szálloda neve: {self._nev}\nSzobák:\n" + "\n".join(leirasok)


