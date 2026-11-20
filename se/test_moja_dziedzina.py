"""Testy Z2. Uruchom: python se/test_moja_dziedzina.py."""
from pathlib import Path

from silnik import wczytaj_baze, wnioskuj_w_przod, wnioskuj_wstecz


def sprawdz(baza, nazwa, wejscie, wynik, oczekiwany_slad, pytania, slad_w_przod=None):
    zadane = []

    def zapytaj(atrybut, powod):
        assert any(warunek[0] == atrybut for warunek in powod["jesli"])
        zadane.append(atrybut)
        return wejscie[atrybut]

    cel = baza["cel"]
    kopia = wejscie.copy()
    fakty, slad = wnioskuj_w_przod(baza, wejscie)
    assert wejscie == kopia
    assert fakty.get(cel) == wynik, (nazwa, fakty)
    assert slad == (oczekiwany_slad if slad_w_przod is None else slad_w_przod), (nazwa, slad)
    slad = []
    assert wnioskuj_wstecz(baza, cel, {}, zapytaj, slad) == wynik, nazwa
    assert slad == oczekiwany_slad, (nazwa, slad)
    assert zadane == pytania, (nazwa, zadane)
    print(f"[OK] {nazwa} | oba tryby: {wynik} | pytania: {', '.join(zadane)}")


def main():
    baza = wczytaj_baze(Path(__file__).parent.parent / "wiedza" / "moja dziedzina.json")
    wspolne = ["frakcja", "klimat"]
    przez_motyw = wspolne + ["motyw", "preferencja"]
    przez_formy = wspolne + ["liczba_form_rasowych", "preferencja"]
    czlowiek = dict(frakcja="Przymierze", klimat="Klasyczne fantasy", motyw="Miasta",
                    preferencja="Królestwo i rycerstwo")
    sprawdz(baza, "Klasyczne Przymierze", czlowiek, "Człowiek", ["P1", "R1"], przez_motyw)
    sprawdz(baza, "Dolna granica (1)", dict(frakcja="Przymierze", klimat="Nietypowe pochodzenie",
            liczba_form_rasowych=1, preferencja="Światłość"), "Draenei", ["P2", "R6"], przez_formy)
    sprawdz(baza, "Górna granica (2)", dict(frakcja="Przymierze", klimat="Nietypowe pochodzenie",
            liczba_form_rasowych=2, preferencja="Wilkołak"), "Worgen", ["P2", "R7"], przez_formy)
    sprawdz(baza, "Nietypowa Horda", dict(frakcja="Horda", klimat="Mrok, magia, technika",
            motyw="Technika/smoki", preferencja="Sprytne wynalazki"), "Goblin", ["P4", "R15"], przez_motyw)
    sprawdz(baza, "Brak pasującego nurtu", dict(frakcja="Horda", klimat="Klasyczne fantasy"),
            None, [], wspolne)

    # Reguły źródłowe R1 i R2 wykluczają się preferencją. Wariant testowy
    # nadaje R2 przesłanki R1, zachowując oba różne wnioski i plik JSON.
    r1, r2 = baza["reguly"][4:6]
    assert (r1["id"], r2["id"]) == ("R1", "R2")
    konkurent = dict(r2, jesli=r1["jesli"])
    pozostale = baza["reguly"][:4] + baza["reguly"][6:]
    for pierwsza, druga in ((r1, konkurent), (konkurent, r1)):
        wariant = dict(baza, reguly=[pierwsza, druga, *pozostale])
        sprawdz(wariant, f"Konflikt R1/R2, pierwsza {pierwsza['id']}", czlowiek,
                pierwsza["to"][1], ["P1", pierwsza["id"]], przez_motyw)
    print("\nZaliczone przypadki własnej bazy: 7/7")


if __name__ == "__main__":
    main()
