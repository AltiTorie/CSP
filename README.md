# Sztuczna Inteligencja - laboratorium

## Zad 2 - Problem Spełniania Ograniczeń (PSO, CSP) do rozwiązywania zagadki Einsteina oraz problemu kolorowania mapy

## Opis
Algorytm udostępnia możliwość rozwiązania problemów z ograniczeniami.

Dostępne są 3 algorytmy przeszukiwania: Backtracking, Forward Checking oraz AC3.

Zaimplementowano 3 heurystyki do wyboru zmiennej: TakeFirst, MinimumRemaining, Degree.

Zaimplementowao 2 heurystyki do wyboru kolejnej przypisywanej wartości: TakeOriginal, LeastConstraining.

### Wymagania

Program jest napisany w Python 3.9.

Algorytm wykorzystuje bibliotekę Pillow do wizualizacji osobników oraz bibliotekę shapely do tworzenia grafu (mapy).

### Konfiguracja

Uruchomienie rozwiązywania problemu Einsteina dostępne jest z poziomu pliku [src/Einstein/einstein_solver.py](src/Einstein/einstein_solver.py).
Użycie metody `print_nice_result(result)` pozwala na wypisanie do konsoli czytelnie sformatowanego rezultatu.

Uruchomienie rozwiązywania problemu kolorowania mapy dostępne jest z poziomu pliku [src/Map_coloring/map_coloring_solver.py](src/Map_coloring/map_coloring_solver.py).
Zmiana zmiennych REGIONS_NUM oraz PLANE_SIZE zmieni kolejno: ilość wygenerowanych regionów, wielkość kwadratowej planszy.
Dla problemu kolorowania mapy dostępna jest możliwość wizualizacji rozwiązania za pomocą metody visualize.

W obu przypadkach zmiana parametrów CSPSolver zmieni sposób poszukiwania rozwiązania.


## Dodatkowe informacje

- Wizualizacja mapy (plik [src/Map_coloring/utils/visualizer.py](src/Map_coloring/utils/visualizer.py)) nie została stworzona przeze mnie. 
[Link do repozytorium](https://github.com/lokig99/SI_CSP_MapGenerator). Wprowadziłem pewne modyfikacje ułatwiające mi użycie tego rozwiązania.
 Z racji jednak tego, że wizualizacja nie jest częścią zadania, a pomocniczą funkcjonalnością, uznałem, że mogę ją wykorzystać

- Generowanie mapy (grafów) nie zostało w pełni zaimplementowane przeze mnie. Jako, że tworzenie mapy nie było wylistowane jako punktowane zadanie, uznałem, że skorzystam z pomocy osób trzecich.


##### Arkadiusz Stępniak 246766