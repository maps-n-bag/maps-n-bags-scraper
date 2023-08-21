# Maps n Bags [Scraper]

## Setup
```
pip install virtualenv
virtualenv venv
```
- For Windows:
```
venv\Scripts\activate
```
- For Linux:  
Please beware of the fact that this is a windows specific scraper, so you might need to change the code a bit to make it work on linux.  
Specifically in the `main.py` file, you need to change the `driver_path` variable to the path of your chromedriver.  
```
source venv/bin/activate
```

Then continue as usual:
```
pip install -r requirements.txt
```

## Usage
```
python <file_name>
```

## Notes
- At this point idk why but --headless makes my code not working, so I commented it out.
- search_raw is the file directly from the tutorial on medium.
- should use full xpath instead of relative xpath
- need to make this wait until loaded, not like time.sleep(5)