# USNewsScrape

## get-all-rankings.py
* Gets all online ed rankings and stores them in individual CSV files within same folder
* Need to download ChromeDriver in order to run, find info here: [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home "ChromeDriver") (quick download)
* Replace ChromeDriver path in line 19 with your download path

## all-school-stats.py
* Uses same ChromeDriver, path in line 22
* Loops thru all CSVs (`get-all-rankings.py` must be ran before `all-school-stats.py`)
* Provides school information in text file, with folder for each category
