from bot import Bot
from interface import Interface

robo = Bot()
best_shows = robo.obtain_show_details()
top_100_shows = robo.prepare_details()
user_interface = Interface(shows=best_shows, shows_library=top_100_shows)