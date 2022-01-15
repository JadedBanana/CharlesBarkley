# Jadi3Pi README

Welcome to Jadi3Pi! This is a Discord bot developed by me over the span of the
virus to take up some of my spare time. If you're reading this, first of all, uh,
wow. I never thought I'd get this far? You're more than welcome to contribute / 
propose changes if you like, I have no problem with that. It's a perfectly 
open-source bot, so you can do whatever, just don't steal my bot and implement it
somewhere else without my permission. That's all.

## Setup

Setting up an instance of Jadi3Pi involves three main steps (final step optional): 
[Python Setup](#python-setup), [Environment Setup](#environment-setup), and 
[Database Setup](#database-setup) 

### <a name="python-setup"></a>Python Setup

**NOTE!: Jadi3Pi is only tested on Windows and Linux. No other operating systems
are confirmed to function correctly.**

Jadi3Pi is written entirely in Python, using the developer-provided `discord.py`
library. As such, it depends heavily on asynchronous commands, meaning that at
minimum, **Python 3.7** is required to run the program. However, **Python 3.9**
or higher is recommended.

In addition to `discord.py`, it also uses some other libraries, all of which are
outlined in the `requirements.txt` file. To quickly and easily install all of them
at once, open a command-line or terminal and input the following:

```python -m pip install -r requirements.txt```

This will automatically install all the packages required for the bot to run.

### <a name="environment-setup"></a>Environment Setup

After Python installation is completed, the bot requires one more thing to launch.
Take note of the [`.env.template`](.env.teplate) file in the outermost directory; 
this is a template for the `.env` file that you must create in order to customize 
the environment variables for running. Every variable referenced in 
[`.env.template`](.env.template) is required for the `.env` file. See 
[`env.example`](.env.example) for an example.

Here is an explanation for every `.env` variable:
- **DEPLOYMENT_CLIENT**: Determines if the bot listens to users outside the
  DEVELOPER_DISCORD_IDS list. If set to 0, it will not; if set to 1, it will.
- **LAUNCH_RUN_CRONCHECK**: The way I have it set up, the bot is run from a 
  cronjob that runs [`launcher.py`](launcher.py) once every two minutes; this 
  variable stores whether to run the check that prevents two from running at 
  the same time. If set to 0, the bot will launch immediately and can run 
  concurrently on the same machine; if set to 1, the bot will have a 55-second 
  launch delay and cannot run while another is running.
- **DEVELOPER_DISCORD_IDS**: Stores the Discord ID's of which users to consider 
  developers (and thus which users to allow to use developer-only commands).
- **LOGGING_LEVEL**: The logging level.
  - 0 = DEBUG
  - 1 = INFO
  - 2 = WARNING
  - 3 = ERROR
  - 4 = CRITICAL
- **LOG_TO_FILE**: Whether to log to a file or not.
- **LOGS_DIR**: The logging directory. I usually have it just set to `logs`.
- **BOT_TOKEN**: The bot token. This is found in the Discord Developer Portal. 
  I won't go into too much detail here, since there are
  [tutorials](https://www.writebots.com/discord-bot-token) out there on
  how to find your token.
- **SQLALCHEMY_DATABASE_URL**: The SQLAlchemy-formatted database URL. See
  [this page](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)
  for more information.
- **EXIT_ON_DATABASE_FAILURE**: Whether to terminate the program if a connection
  to the database cannot be made.
- **DISABLE_COMMANDS_WITH_MISSING_DATABASE_TABLES**: Whether to disable commands
  by default if they are missing tables in the database or the database cannot
  be reached.
- **CLEAR_TEMPORARY_DATABASE_TABLES_ON_STARTUP**: Whether to clear all the rows
  from database tables that store exclusively *temporary* data. This includes
  the `hg_current_game_phases` and `hg_current_game_actions` tables.
- **YOUTUBE_API_KEY**: The YouTube API Key. See 
  [this page](https://developers.google.com/youtube/v3) for more information.
- **WEATHER_API_KEY**: The OpenWeatherMap API Key. See 'Current Weather Data'
  section on [this page](https://openweathermap.org/api) for more information.
- **HUNGER_GAMES_EXPIRE_SECONDS**: How many seconds it takes for a Hunger Games
  instance to expire.
- **HUNGER_GAMES_EXPIRE_CHECK_INTERVAL**: How often to check if a Hunger Games game
  is expired, in seconds.
- **UNO_EXPIRE_SECONDS**: How many seconds it takes for an Uno instance to expire.
- **UNO_EXPIRE_CHECK_INTERVAL**: How often to check if an Uno game is expired, in 
  seconds.
- **UNO_BUTTONS_TIMEOUT_SECONDS**: How long before the buttons on UNO embeds 
  (lobby, hands, postgame) stop responding to user input.
- **UNO_DISABLE_OLD_VIEW_ON_REFRESH**: Whether to disable the buttons on the old embed
  when the `uno` command is called again during the lobby phase.
- **UNO_ALLOW_DUPLICATE_PLAYERS_IN_GAME**: Whether to allow duplicate players in Uno
  instances. Usually used for debugging purposes.
- **MAL_DEFAULT_ANIME_USER**: The default user that the `randomanime` command uses
  to pull its random anime. Ideally, this should be a user with a shit-ton of anime
  on their list.
- **MAL_ANIME_COUNT**: The number of total anime on MAL_DEFAULT_ANIME_USER's list.
- **MAL_DEFAULT_MANGA_USER**: The default user that the `randommanga` command uses
  to pull its random manga. Ideally, this should be a user with a shit-ton of manga
  on their list.
- **MAL_MANGA_COUNT**: The number of total manga on MAL_DEFAULT_MANGA_USER's list.
- **DISABLED_COMMANDS**: A list of commands that should be disabled on startup.
  Developer-only commands cannot be disabled.

### <a name="database-setup"></a>Database Setup

In an effort to reduce memory usage, some more intensive commands make use of
SQLAlchemy's database interfacing to store their active data / constants in a 
database. Without a proper database, many commands, such as `hungergames`, will
be unusable.

The database used by the standard deployment of Jadi3Pi uses PostgreSQL. A
backup has been created of that database's schema, located at 
[`database/schema_template.sql`](database/schema_template.sql). It is highly
recommended that one uses the provided template to create their database, as
any unexpected changes could cause errors in the commands that use those tables.
