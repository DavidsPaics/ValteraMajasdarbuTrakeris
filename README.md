# Fenomenālais codeforces mājasdarbu punktu skaitītājs

## Instalācija

1.  `git clone https://github.com/DavidsPaics/ValteraMajasdarbuTrakeris.git`
2.  Iekopē mājasdarbu rezultātus `data/majasdarbi.txt`
3.  Iekopē visus lietotāju vārdus, ko izsekot `data/lietotaji.txt`
4.  `pip install -r requirements.txt`
5.  `python main.py`

## Lietošana

1. Ieraksti Codeforces uzdevuma ID
2. Uzspied enter

## Datu formāts

Dati tiek saglabāti šādā formātā:

```
LietotajaVards - punkti ([..]bonusPunkti)
```

Bonusa punkti tiek rēķināti šādi (katrai rindiņai):

1.  Aizstāj "- " ar ""
2.  Sadala rindu 2-3 daļās pēc atstarpēm
3.  No 3. daļas izdzēš pirmo un pēdējo simbolu (parasti "()")
4.  No atlikušā izdzēš visus simbolus, kas nav cipari
5.  Atlikušos ciparus secīgi savieno skaitlī

## Kārtošana

Kārtošanai tiek izmantota formula `punkti + (bonusPunkti*0.99999999999)`
