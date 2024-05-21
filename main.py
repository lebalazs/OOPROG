from szoba import Szoba, EgyagyasSzoba, KetagyasSzoba
from szalloda import Szalloda
from foglalas import Foglalas
from menu import Menu
from termcolor import colored
from datetime import date
import datetime


#szálloda létrehozása:
szalloda = Szalloda("Budapest Grand Hotel")

#3 szoba létrehozása:
szalloda.addSzoba(EgyagyasSzoba(15000, 101, False, ["TV", "Minibár"]))
szalloda.addSzoba(EgyagyasSzoba(17000, 102, True, ["TV", "Légkondicionáló"]))
szalloda.addSzoba(KetagyasSzoba(25000, 103, True))

# Foglalások létrehozása:
foglalasok = Foglalas(szalloda)

today = date.today()
tomorrow = date.today() + datetime.timedelta(days=1)
afttom = date.today() + datetime.timedelta(days=2)

foglalasok.foglalas(101,today.strftime("%Y-%m-%d")) #ma
foglalasok.foglalas(101,tomorrow.strftime("%Y-%m-%d")) #holnap
foglalasok.foglalas(103,today.strftime("%Y-%m-%d")) #ma
foglalasok.foglalas(103,tomorrow.strftime("%Y-%m-%d")) #holnap
foglalasok.foglalas(102,afttom.strftime("%Y-%m-%d")) #holnapután

#menü indítása:
Menu(foglalasok)


