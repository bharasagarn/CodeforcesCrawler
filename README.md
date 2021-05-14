# Codeforces Crawler
A web app to provide various functionalities related to user's Codeforces handle.

Functionalities (Ideas):
- Pi chart for solved problems tags
- Rating plot
- Number of problems solved bar chart for given time window
- Upsolve section
- Unsolved problems section
- Suggest problem
- Upcoming contests
- Add reminder in calendar for contest
- Update icon for every data shown, modifying in DB

ToDo:
- Create ER diagram of DBs needed
- Create a horizontal prototype categorizing above functionalities
- Code

**How to run:**
- Activate python virtual environment using:
```
source CFCrawlerEnv/bin/activate
```
- Install all the dependencies using:
```
pip install -r req.txt
```
- Run server:
```
python3 manage.py runserver
```
[In case there is __sqlite3 error, install libsqlite3-dev and rebuild python3]