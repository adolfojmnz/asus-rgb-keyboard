## ASUS Keyboard RGB Lights Changer

The `main.py` file includes a series of utilities to set different colors in a ASUS RGB Keyboard.
The `db.py` file includes utilities to create a SQLite3 db and populate it with the data in the `colors.csv` file.
<br>


### Usage
The `main.py` utitlies can check on the database the current active color,
the next color, the previous color and specif colors.

#### Set the next color
```python
python main.py --next
```

#### Set the previous color
```python
python main.py --prev
```

#### Set a specific color
```python
python main.py --color 25
```
<br>


### Requirements

#### Asus-Linux
The library [asus-linux](https://asus-linux.org) is required.
Follow their guides on how to install the library.

#### Sqlite3
The sqlite3 library is required.
It is probably included in most distros' package manager,
but check the official website for general guidence. [Sqlite3](https://www.sqlite.org/index.html)
