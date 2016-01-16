## Pathtreker

### Setup

Download the Toronto Centerlines dataset and extract it to centerlines/

Download the Intersections dataset and extract it to centerline-intersection/

Download the Address Points dataset and extract it to address/

Run `pip install -r requirements.txt` to install required modules

Run these commands to serialize the datasets:
```
python picklegraph.py
python pickleaddress.py
python picklestreet.py
```

### Running Part 1

Copy `input11_short` and `input12_long` to the directory

Run `python solve.py`

### Running Part 2

Run `python return_directions.py` to start the server

Go to http://localhost:5000/static/index.html for the interface
