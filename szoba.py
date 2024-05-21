from abc import ABC, abstractmethod

class Szoba(ABC):
    def __init__(self, ar:int, szobaszam:int):
        self._ar = ar
        self._szobaszam = szobaszam

    @abstractmethod
    def leiras(self):
        pass

    @property 
    def ar(self):
        return self._ar
    
    @ar.setter
    def ar(self,ar):
        self._ar = ar
    
    @property 
    def szobaszam(self):
        return self._szobaszam


class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam:int, erkely=False, extra_kellekek=[]):
        super().__init__(ar, szobaszam)
        self.erkely = erkely
        self.extra_kellekek = extra_kellekek

    def leiras(self):
        erkely_leiras = "van" if self.erkely else "nincs"
        return f"{self._szobaszam} - Egyágyas szoba: Ár {self._ar} Ft, Erkély: {erkely_leiras}, Extra: {', '.join(self.extra_kellekek)}"



class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam:int, erkely=False):
        super().__init__(ar, szobaszam)
        self.erkely = erkely

    def leiras(self):
        erkely_leiras = "van" if self.erkely else "nincs"
        return f"{self._szobaszam} - Kétágyas szoba: Ár {self._ar} Ft, Erkély: {erkely_leiras}"

