"""Aktualizuje kartę Śródmieścia na stronie według liczby wolnych miejsc na Strefie Zajęć.

Wolne miejsca > 0  -> treść z scripts/dks_wolne.html ("dla wszystkich" + "Zapisz się")
Wolne miejsca = 0  -> treść z scripts/dks_pelna.html ("grupa pełna" + "Napisz do mnie")
Nie da się odczytać -> nic nie zmienia.
"""
import re
import sys
import urllib.request

URL = "https://www.strefazajec.pl/course/view/id/89147"
FILE = "index.html"
START = "<!-- DKS-MIEJSCA:START"
END = "<!-- DKS-MIEJSCA:END -->"


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    m = re.search(r"<dt>\s*Wolnych miejsc\s*</dt>\s*<dd>\s*(\d+)\s*</dd>", html)
    if not m:
        print("Nie znaleziono liczby wolnych miejsc - nic nie zmieniam.")
        return
    free = int(m.group(1))
    print(f"Wolnych miejsc: {free}")

    block = read("scripts/dks_wolne.html" if free > 0 else "scripts/dks_pelna.html")
    page = read(FILE)
    i, j = page.find(START), page.find(END)
    if i < 0 or j < 0:
        print("Brak znaczników DKS-MIEJSCA w index.html - nic nie zmieniam.")
        sys.exit(1)
    i = page.index("\n", i) + 1          # zostaw linię ze znacznikiem START
    j = page.rindex("\n", 0, j) + 1      # zostaw wcięcie przed END
    new_page = page[:i] + block + page[j:]
    if new_page != page:
        with open(FILE, "w", encoding="utf-8", newline="") as f:
            f.write(new_page)
        print("Zaktualizowano index.html.")
    else:
        print("Bez zmian.")


if __name__ == "__main__":
    main()
