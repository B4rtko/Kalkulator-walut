import sys
from gui import ExchangeGui
from data_get import ExchangeData


def program_run():
    """
    function decides if user wants to use GUI or perform just one exchange using just the terminal
    """
    if len(sys.argv) == 4:
        data = ExchangeData()
        if sys.argv[1] not in data.df.index:
            raise ValueError(f"Nieznana waluta: {sys.argv[1]}")
        if sys.argv[2] not in data.df.index:
            raise ValueError(f"Nieznana waluta: {sys.argv[2]}")
        try: float(sys.argv[3])
        except ValueError:
            raise ValueError(f"{sys.argv[3]} nie jest rozpoznawaną przez system liczbą")

        amount = data.exchange(sys.argv[1], sys.argv[2], float(sys.argv[3]))
        print(f"{sys.argv[3]} {sys.argv[1]} = {amount} {sys.argv[2]}")
    else:
        ExchangeGui(ExchangeData())


if __name__ == "__main__":
    program_run()


# PROGRAM POBIERA DANE Z TABELI KURSÓW A ZE STRONY NBP JEŚLI JEST POŁĄCZENIE Z INTERNETEM, JEŚLI NIE - Z PLIKU kursy.csv
# ZAPISANEGO PRZY OSTATNIM URUCHOMIENIU PROGRAMU PODCZAS GDY POŁĄCZENIE Z INTERNETEM BYŁO DOSTĘPNE. INTERFEJS OFERUJE
# KILKA UDOGODNIEŃ: PODPISANIE JAKIEGO RODZAJU JEST WYBRANA WALUTA (NP. DOLAR, FUNT, ZŁOTY - NIE ZASTOSOWAŁEM PEŁNYCH
# NAZW PONIEWAŻ DŁUGOŚCI TYCH NAZW SĄ NA TYLE ZRÓŻNICOWANE ŻE BYŁOBY TO TRUDNE ABY TO JAKOŚ SENSOWNIE UJEDNOLICIĆ),
# PRZYCISK SWITCH, KTÓRY ZAMIENIA WALUTY POCZĄTKOWĄ ORAZ DOCELOWĄ MIEJSCAMI, PODPISY SYMBOLI WALUT W JAKIEJ WPISUJEMY
# I W JAKIEJ OTRZYMUJEMY WYNIK, ABY CAŁY PROCES BYŁ WYGODNIEJSZY I CZYTELNIEJSZY ORAZ WSPARCIE DLA PRZYCISKU
# ESC (WYŁĄCZANIE PROGRAMU) I ENTER (PRZELICZNANIE WALUT)
#
# PROGRAM URUCHAMIAMY PROSTO Z EDYTORA LUB Z LINI KOMEND. DODATKOWE ARGUMENTY NIE SĄ WYMAGANE ALE NIE SĄ TEŻ TRAKTOWANE
# JAKO BŁĄD - SĄ IGNOROWANE. WYJĄTEK STANOWI PODANIE 3 ARGUMENTÓW W USTALONEJ KOLEJNOŚCI: waluta_początkowa,
# waluta_docelowa, ilość. WTEDY PROGRAM WYKONUJE OBLICZENIA BEZ ZAŁĄCZANIA GUI.
#
# W TRAKCIE DZIAŁANIA PROGRAM, GDY JEST DOSTĘPNE POŁĄCZENIE Z INTERNETEM, TWORZY DODATKOWO
# DWA PLIKI W FOLDERZE W KTÓRYM SIĘ ZNAJDUJE: kursy.csv ZAWIERAJĄCY POBRANE DANE ORAZ tytuł.txt SŁUŻĄCY JAKO INFORMACJA
# DLA UŻYTKOWNIKA WYŚWIETLANA GDY PROGRAM KORZYSTA Z DANYCH ARCHIWALNYCH, KTÓRE MOGĄ NIE BYĆ AKTUALNE.
#
# KOMENDA WYWOŁANIA W CMD ABY WŁĄCZYĆ GUI: py Zad_1.py
# KOMENDA WYWOŁANIA W CMD DLA OBLICZENIA JEDNEGO PRZEWALUTOWANIA BEZ GUI: py Zad_1.py PLN USD 12.50


