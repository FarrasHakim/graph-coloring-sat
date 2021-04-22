## Tri Coloring Graph Problem

#### 1. Cara menjalankan di windows

- Install cygwin dari link [ini](http://www.cygwin.com/) (Install yang versi 32bit karena yang 64bit error)
- Jalankan setup-x86.exe lalu install seperti biasa
- Download minisat dari link [ini](http://minisat.se/downloads/MiniSat_v1.14_cygwin)
- Pindahkan ke lokasi cygwin (defaultnya `C:\cygwin\bin`)
- Pastikan python 3 terinstall dan ada di PATH.
- Pastikan cygwin ada di PATH. Contoh: `C:\cygwin\bin` terletak di PATH
- Masuk ke folder "graph coloring sat" lalu buka cmd
- Jalankan `pip install -r requirements.txt`
- Jalankan `python src.py`

#### 2. Cara menjalankan di wsl

- Update repository:

```
sudo apt update
```

- Install package minisat dengan command berikut:

```
sudo apt install minisat
```

- Install package python3 dan pip3

```
sudo apt install python3 python3-pip
```

- Install package yang terdapat di requirements

```
pip3 install -r requirements.txt
```

- Install chrome di wsl

```

```

- Jalankan `python3 src.py`

### Build Executable Application

1. Install required package

```
pip install -r requirements.txt
```

2. Build executable files using this command

```
python -m eel graph.py web --hidden-import eel --onefile --noconsole --windowed
```
