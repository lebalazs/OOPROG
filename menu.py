import os
import sys
from szoba import Szoba, EgyagyasSzoba, KetagyasSzoba
from szalloda import Szalloda
from foglalas import Foglalas
import msvcrt
from termcolor import colored
from datetime import date
import datetime

class Menu:
    def __init__(self, foglalasok: Foglalas):
        self._foglalasok = foglalasok
        '''menüpontok:'''
        self.menucont = [
            ['A','Szoba hozzáadása          '],
            ['H','Hotel adatok megtekintése '],
            ['-'],
            ['U','Új foglalás               '],
            ['L','Foglalás lemondása        '],
            ['M','Foglalások megtekintése   '],
            ['E','Foglalás ellenőrzése      '],
            ['-'],
            ['X','Kilépés                   '],
        ]
        self.menu()

    '''számbekérő min-max és default értékkel:'''
    def get_valid_number(self,ptxt,pmin,pmax,defval=-999):
        while True:
            sdefval = '' if defval==-999 else ' [Alap érték ENTER-rel: '+str(defval)+']: '
            inp = input(ptxt+sdefval)
            if inp == "" and defval != -999:
                return defval
            else:
                try:
                    number = int(inp)
                    if number >= pmin and number <=pmax:
                        return number
                    else:
                        print(colored(f"A szám nem lehet kisebb mint {pmin} és nem lehet nagyobb, mint {pmax}. Próbálja újra.","magenta"))
                except ValueError:
                    print(colored("Ez nem egy érvényes szám. Próbálja újra.","red"))


    '''dátum bekérő, holnapi vagy későbbi dátummal:'''
    def get_valid_date(self) -> date:
        while True:
            tomorrow = date.today() + datetime.timedelta(days=1)
            ev = int(tomorrow.strftime("%Y"))
            ho = int(tomorrow.strftime("%m"))
            nap = int(tomorrow.strftime("%d"))
            ev = self.get_valid_number("Kérem a foglalási évet: ",ev,ev+1,ev)
            ho = self.get_valid_number("Kérem a foglalási hónapot: ",1,12,ho)
            nap = self.get_valid_number("Kérem a foglalási napot: ",1,31,nap)
            try:
                datum = date(ev, ho, nap)
                if datum >= tomorrow:
                    return datum
                else:
                    print(colored(f"HIBA - A dátum nem lehet ma vagy korábbi!","red"))
            except Exception as e:
                print(colored(f"HIBA - {ev}-{ho}-{nap} nem egy érvényes dátum :(  -  {e}","red"))


    '''gombnyomásra várakozó'''
    def wait(self):
        print(colored('---  Nyomjon meg egy gombot a folytatáshoz  ---','green'))
        msvcrt.getch()

    '''header kirajzoló:'''
    def printHeader(self,title):
        w = int(34)
        n = (w-len(title))//2+len(title)
        print("".rjust(w,"*"))
        print(colored(title.rjust(n," "),"red"))
        print("".rjust(w,"*"))


    '''menü kirajzoló'''
    def menudraw(self):
        os.system('cls')
        w = int(34)
        szn = self._foglalasok.szalloda.nev
        n = (w-len(szn))//2+len(szn)
        print("".rjust(w,"*"))
        print("MENÜ".rjust((w-4)//2+4," "))
        print(colored(szn.rjust(n," "),"red"))
        print("".rjust(w,"*"))
        for i in self.menucont:
            if i[0] != '-':
                print("   "+colored(i[0],"yellow")+" - "+i[1])
            else:
                print("".rjust(w,"-"))
        print("".rjust(w,"*"))

    ''' menu '''
    def menu(self):
        c = ''
        while c.upper()!='X':
            self.menudraw()
            c = msvcrt.getch().decode('utf-8').upper()
            os.system('cls')

            match c:
                case 'X':
                    print('---  VISZONTLÁTÁSRA!  ---')
                    sys.exit(0)
                case 'A':
                    self.addRoom()
                    self.wait()
                case 'H':
                    print(self._foglalasok.szalloda.leiras())
                    self.wait()
                case 'U':
                    self.bookRoom()
                    self.wait()
                case 'L':
                    self.cancelRoom()
                    self.wait()
                case 'M':
                    print(self._foglalasok.showFoglalas())
                    self.wait()
                case 'E':
                    self.checkBook()
                    self.wait()


    '''menü kezelő függvények/eljárások:'''
    def addRoom(self):
        self.printHeader('SZOBA HOZZÁADÁSA A HOTELHEZ')
        szobaszam = self.get_valid_number("Kérem az új szoba számát (101-200 között): ",101,200)
        agyszam = self.get_valid_number("Egy (1) vagy kétágyas (2) szoba",1,2,1)
        erkely = (1 == self.get_valid_number("Van erkély (0 - nincs, 1 - van) ",0,1,0))
        ar = self.get_valid_number("Kérem adja meg a szoba árát: ",1,1000000)
        if agyszam==1:
            sextrak = input("Kérem vesszővel (,) elválasztva sorolja fel az extrákat (ha nincs, ENTER): ")
            extrak = sextrak.split(",")
        try:
            if agyszam==1:
                self._foglalasok.szalloda.addSzoba(EgyagyasSzoba(ar,szobaszam,erkely,extrak))
            else:
                self._foglalasok.szalloda.addSzoba(KetagyasSzoba(ar,szobaszam,erkely))
            print(colored("A szoba a szállodához lett adva","green"))
            print("\n"+self._foglalasok.szalloda.leiras())    
        except Exception as e:
            print(colored(f"HIBA - {e}. A szoba nem lett felvéve","red"))

    def bookRoom(self):
        self.printHeader('ÚJ FOGLALÁS')
        print(colored("A szálloda szobái","yellow"))
        print("\n"+self._foglalasok.szalloda.leiras()+"\n")    

        datum = self.get_valid_date()
        szobaszam = self.get_valid_number("Kérem a szoba számát: ",101,200)
        try:
            ar=self._foglalasok.foglalas(szobaszam,datum.strftime("%Y-%m-%d"))
            print(colored(f"Foglalás sikeres! Szobaszám: {szobaszam}, dátum: "+datum.strftime("%Y-%m-%d")+". Ár: "+str(ar),"green"))

        except Exception as e:
            print(colored(f"Foglalás Hiba: {e}","red"))


    def cancelRoom(self):
        self.printHeader('FOGLALÁS LEMONDÁSA')
        print(self._foglalasok.showFoglalas())
        datum = self.get_valid_date()
        szobaszam = self.get_valid_number("Kérem a szoba számát: ",101,200)
        try:
            ar=self._foglalasok.lemondas(szobaszam,datum.strftime("%Y-%m-%d"))
            print(colored(f"Foglalás lemondása sikeres! Szobaszám: {szobaszam}, dátum: "+datum.strftime("%Y-%m-%d"),"green"))

        except Exception as e:
            print(colored(f"Lemondás Hiba: {e}","red"))

    def checkBook(self):
        self.printHeader('FOGLALÁS ELLENŐRZÉSE')
        print(self._foglalasok.showFoglalas())
        datum = self.get_valid_date()
        szobaszam = self.get_valid_number("Kérem a szoba számát: ",101,200)
        try:
            status=self._foglalasok.checkSzobaStatus(szobaszam,datum.strftime("%Y-%m-%d"))
            col = "red" if status == "Foglalt" else "green"
            print(colored(f"A #{szobaszam} szoba "+datum.strftime("%Y-%m-%d")+" napon "+status,col))

        except Exception as e:
            print(colored(f"Foglalás ellenőrzési Hiba: {e}","red"))






 

