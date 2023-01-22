# QA Exam Kitchen
Zadatak za automatizaciju

## Postavka

```sh
#1. Kloniraj projekat [https://github.com/andreja-petrovic/qa-exam-kitchen]
$ git clone git@github.com:andreja-petrovic/qa-exam-kitchen

#2. Prebaci se u folder
$ cd zadatak

#3. Intaliraj python venv
$ sudo apt install python3-venv

#4. Kreiraj virtual environment
$ python3 -m venv naziv_tvog_virtual_env

#5. Aktiviraj virtual environment
$ source naziv_tvog_virtual_env/bin/activate

#6. Instaliraj requirements
$ pip install -r requirements.txt

#7. Instaliraj ChromeDriver
- prebaci chromedriver fajl u putanja/do/tvog/chromedriver
```

## Pokretanje testova
Koristi komandu ```pytets``` unutar virtual environment-a za pokretanje testova
- ```pytest``` za pokretanje svih testova u fajlu
- ```pytest test_zadatak.py::ime_testa_koji_pokreces```
  na primer: test_zadatak.py::test_zadatak_1_forma

