# Uber Statistics

## Introducere

Aplicatia va genera statistici despre cursele unui utilizator de Uber.
Aplicatia va primi un fisier, din linia de comanda, pe care il va procesa si pe baza informatiilor va afisa,
in terminal, diferite informatii:
-   Total bani cheltuiti
-   Total curse (COMPLETED, CANCELED)
-   Total curse per an
-   Total curse per oras
-   Total curse per luna
-   Distanta totala (in km)
-   Curse per produs
    -   UberX
    -   Comfort
    -   Black
-   Perioada totala petrecuta in curse
    -   Secunde
    -   Minute
    -   Ore
    -   Zi
-   Cea mai scurta cursa (in minute)
-   Cea mai lunga cursa (in minute)

## Instalare

Cloneaza repozitory-ul:

```bash
git clone https://github.com/alexpapuc/curs_tema1.git
```
Navigheaza in folderul proiectului, creaza un virtual environment si instaleaza dependintele:

```bash
cd cursa_tema1_alex
python -m venv venv
pip install -r requirements.txt
```

## Utilizare
-  Deschide un terminal de comanda
-  Activeaza virtual environment-ul creat la pasul anterior
-  Cu virtual environment activat introdu comanda:

```bash
python uber_trips.py trips_data.csv
```
