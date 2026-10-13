# Od czego zależą zarobki programistów?

Eksploracyjna analiza danych z ankiety **Stack Overflow Developer Survey 2018**. Projekt zaliczeniowy z analizy danych w Pythonie.

**Raport online:** https://Olgaolga020.github.io/NAZWA_REPO/

## Zakres

Dane pochodzą z dobrowolnej ankiety online, którą wypełniło 98 855 programistów z całego świata. Do analizy wybrano osiem kolumn: kraj, status zatrudnienia, wykształcenie, kierunek studiów, staż kodowania, wiek, zadowolenie z pracy i roczne zarobki w USD. Zmienną zależną są zarobki.

Postawiono trzy pytania badawcze:

1. Co mocniej różnicuje zarobki: kraj czy doświadczenie?
2. Czy kierunek studiów wiąże się z wyższą pensją, gdy porównuje się osoby z tego samego kraju i o podobnym stażu?
3. Czy zadowolenie z pracy rośnie wraz ze stażem?

## Przebieg analizy

**Etap 1. Czyszczenie danych.** Przedziały tekstowe (staż, wiek) zamieniono na liczby, a skalę słowną zadowolenia na stopnie od 1 do 7. Zdiagnozowano braki (`missingno`, testy zależności od zatrudnienia, kraju i stażu) i uznano, że mechanizm najbardziej przypomina MAR. Ustalono dwie reguły poprawności: zarobki w przedziale 1 000–500 000 USD oraz staż niewiększy niż wiek pomniejszony o 5 lat. Odrzucono 2 741 zarobków (5,7% zadeklarowanych) i poprawiono 256 sprzecznych wartości stażu. Obserwacje odstające wyznaczono metodą IQR w obrębie kraju i zachowano w danych. Staż uzupełniono metodą KNN (k = 14, na podstawie wieku), co dotyczyło 153 wartości. Zarobków i zadowolenia nie imputowano, bo są badanymi zmiennymi. Do dalszych analiz przyjęto 43 673 pracujące osoby z wiarygodną pensją.

**Etap 2. Wizualizacje.** Rozkład zarobków, mapa median wg kraju, zarobki a staż w czterech krajach, zarobki wg kierunku studiów, zadowolenie wg stażu oraz interaktywny wykres struktury próby (D3.js).

**Etap 3. Analiza.** Korelacje rangowe, regresje liniowe na logarytmie zarobków z odpornymi błędami standardowymi (HC3), test Kruskala-Wallisa z wielkością efektu.

## Najważniejsze wyniki

| Pytanie | Wynik |
|---|---|
| Kraj czy staż | Sam kraj wyjaśnia 50,3% zmienności logarytmu zarobków, sam staż 18,7%, oba razem 57,3%. Przy tym samym kraju rok stażu oznacza średnio 3,7% wyższe zarobki. |
| Kierunek studiów | Osoby po informatyce zarabiają o 19,5% mniej niż osoby po kierunkach spoza IT. Po uwzględnieniu kraju i stażu różnica spada do 5,3% (95% CI: od −6,7% do −3,9%). |
| Zadowolenie ze stażem | Korelacja Spearmana wynosi 0,06, a wielkość efektu jest pomijalna (ε² = 0,003). Dziesięć lat stażu to +0,10 pkt na skali 1–7, a po uwzględnieniu kraju +0,04 pkt (95% CI: od +0,01 do +0,06). |

## Ograniczenia

- Ankieta była dobrowolna, a największe grupy pochodzą z USA i Indii.
- Zarobków nie podało 51,7% respondentów, a brak zależał od kraju i stażu, więc mediany mogą być zawyżone.
- Zarobki podano w dolarach nominalnych, bez poprawki na koszty życia.
- Staż i wiek są środkami przedziałów, a nie dokładnymi wartościami.
- Dane mają charakter obserwacyjny. Wyniki opisują zależności, a nie przyczyny.
- Zadowolenie zmierzono jednym pytaniem, a ankieta nie zawierała pytań o stres ani wypalenie.

## Struktura repozytorium

```
├── README.md
├── projekt_mini.ipynb        notebook z analizą
├── eksport.py                eksport notebooka do raportu HTML
├── requirements.txt          wersje bibliotek
├── data/
│   └── so2018_czyste.csv     dane po czyszczeniu
└── docs/
    └── index.html            raport HTML
```

## Uruchomienie

1. Pobrać plik `survey_results_public.csv` ze strony zbioru na Kaggle i umieścić w folderze `data/`. Plik surowy nie jest dołączony do repozytorium ze względu na rozmiar.
2. Utworzyć środowisko i zainstalować biblioteki:
```
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
```
3. Otworzyć `projekt_mini.ipynb` i uruchomić wszystkie komórki.
4. Wygenerować raport poleceniem `python eksport.py` (wynik w `docs/index.html`).

Użyto Pythona 3.14 oraz bibliotek pandas, seaborn, scipy, scikit-learn, statsmodels, missingno i plotly.

## Dane

Źródło: Stack Overflow Developer Survey 2018, udostępniony na Kaggle: https://www.kaggle.com/datasets/stackoverflow/stack-overflow-2018-developer-survey. Warunki licencji podano na stronie zbioru. Plik `data/so2018_czyste.csv` powstał w wyniku czyszczenia opisanego w notebooku.

## Autor

Olga Dawidowicz, AGIIst 2026.