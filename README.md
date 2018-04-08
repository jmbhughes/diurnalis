# diurnalis
I keep my journal and research logs in a LaTeX file because LaTeX is absolutely amazing. [Here](journal.tex) is the LaTeX template and the [pdf file](journal.pdf) that it compiles.

More tools will be created over time to accompany it. Right now, there is a [reader](Reader.py) built in Python that extracts the entries separately for analysis. This will allow for the creation of interesting graphics and exploring patterns in the writing.

## Beemind
[Beeminder](https://www.beeminder.com/overview) is "goal-tracking with teeth." you can track habits and keep them on track with flexible goals. If you miss a goal, you pay a small sum of money. I want to keep track of my journaling to encourage myself to meet a daily minimum. The [Beemind.py](Beemind.py) script will read in the journal and push your daily writing up to Beeminder using an API call. I run it periodically at a set time with crontab.
```
0  *  *  *  * python /home/marcus/diurnalis/Beeminder.py
```
For the Beeminder portion, you will need to update the all-caps variables at the top of [Beeminder.py](Beeminder.py) for your use. You will also need to create an `auth.txt` file which has two lines: the first being your Beeminder username and the second being your Beeminder authentication token, which you can find in the [documentation](http://api.beeminder.com/#personal-authentication-token).

## TODO
- add new features. what's needed?
- clean up the `auth.txt` so there's just one config file for username and goal_slug and authentication_token etc and with a parameterized version of `Beemind.py` so it can run on different tasks

## The name?
[Diurnalis](https://en.wiktionary.org/wiki/diurnalis) is an [obsolete term](http://www.yourdictionary.com/diurnalis) for a journal or diary. 