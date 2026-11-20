## Konsultacja wstecz

Skrócony zapis uruchomienia `python se/silnik.py`. Po strzałkach podano odpowiedzi, a listy opcji pominięto.

```text
=== Wnioskowanie wstecz ===
Którą frakcję wybierasz? → Przymierze
Jaki klimat świata bardziej Ci odpowiada? → Nietypowe pochodzenie
Ile form rasowych postaci chcesz mieć? → 2
Co jest dla Ciebie najciekawsze w rasie? → Wilkołak
Polecam: Worgen
Reguły: P2 -> R7
```

Silnik najpierw pobrał frakcję i klimat, aby wyznaczyć nurt regułą P2. Dla tej gałęzi reguły sprawdzają liczbę form i preferencję, więc pytanie o motyw zostało pominięte. Zapisane odpowiedzi służyły kolejnym regułom bez powtarzania pytań.

## Strategia rozwiązywania konfliktów

Priorytet wynika z kolejności reguł w bazie JSON. Wnioskowanie w przód zapisuje wniosek pierwszej reguły, której przesłanki są znane i spełnione podczas przeglądu, a kolejne reguły nie nadpisują ustalonej wartości. Wnioskowanie wstecz wybiera pierwszą regułę, której przesłanki uda się potwierdzić rekurencyjnie.

Reguły R1 (Człowiek) i R2 (Gnom) w bazie źródłowej wymagają różnych preferencji. Aby sprawdzić konflikt, w kopii bazy w pamięci nadano R2 takie same przesłanki jak R1. Przy kolejności R1, R2 oba tryby wskazały Człowieka, a przy kolejności R2, R1 wskazały Gnoma. Przykład pokazuje wpływ kolejności konkurujących reguł na wynik.
