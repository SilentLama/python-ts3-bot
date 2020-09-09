import importlib    
from Moduleloader import *
import Moduleloader
import Bot
import logging
from ts3.TS3Connection import TS3QueryException
import ts3.Events as Events
from datetime import datetime
__version__ = "0.4"
bot = None
logger = logging.getLogger("bot")


@Moduleloader.setup
def setup(ts3bot):
    global bot
    bot = ts3bot
    print("utils loaded")


@command('hello',)
@group('Server Admin',)
def hello(sender, msg):
    Bot.send_msg_to_client(bot.ts3conn, sender, "Hello Admin!")


@command('hello',)
@group('Moderator',)
def hello(sender, msg):
    Bot.send_msg_to_client(bot.ts3conn, sender, "Hello Moderator!")


@command('hello',)
@group('Normal',)
def hello(sender, msg):
    Bot.send_msg_to_client(bot.ts3conn, sender, "Hallo.. Peasant")


@command('kickme', 'fuckme')
@group('.*',)
def kickme(sender, msg):
    ts3conn = bot.ts3conn
    ts3conn.clientkick(sender, 5, "Whatever.")


# @command('news',)
# @group('.*',)
# def show_news(sender, msg):
#     Bot.send_msg_to_client(bot.ts3conn, sender, "Heute gibt es noch nichts neues")

@command('suggest',)
@group('.*',)
def note_suggestion(sender, msg):
    try:
        msg = msg.replace("!suggest", "")
        with open("./data/suggestions.txt", "a") as file:
            file.write(f"{datetime.now()} ({sender}):{msg} \n")
            file.close()
        Bot.send_msg_to_client(bot.ts3conn, sender, f"\nIch habe deinen Vorschlag eingetragen: \n{datetime.now()} {msg}")
    except (Exception) as err:
        Bot.send_msg_to_client(bot.ts3conn, sender, f"\n Da ist etwas schief gelaufen: \n {err}")

@command('get_suggest',)
@group('Server Admin',)
def list_suggestions(sender, msg):
    try:
        with open("./data/suggestions.txt", "r") as file:
            suggestions = "".join(file.readlines())
            file.close()
        Bot.send_msg_to_client(bot.ts3conn, sender, f"\nHier sind alle Vorschläge: \n {suggestions}")
    except (Exception) as err:
        Bot.send_msg_to_client(bot.ts3conn, sender, f"\n Da ist etwas schief gelaufen: \n {err}")
    

@command('help',)
@group('.*',)
def get_help(sender, msg):
    commands = ["!whoami", "!hello", "!vt <link>", "!fuckme", "!kickme", "!news", "!suggest"]
    Bot.send_msg_to_client(bot.ts3conn, sender, commands)


@command('mtest',)
def mtest(sender, msg):
    print("MTES")
    channels = msg[len("!mtest "):].split()
    print(channels)
    ts3conn = bot.ts3conn
    print(ts3conn.channelfind(channels[0]))
 


@command('multimove', 'mm')
@group('Server Admin', 'Moderator')
def multi_move(sender, msg):
    """
    Move all clients from one channel to another.
    :param sender: Client id of sender that sent the command.
    :param msg: Sent command.
    """
    channels = msg.split()[1:]
    source_name = ""
    dest_name = ""
    source = None
    dest = None
    ts3conn = bot.ts3conn
    if len(channels) < 2:
        if sender != 0:
            Bot.send_msg_to_client(ts3conn, sender, "Usage: multimove source destination")
            return
    elif len(channels) > 2:
        channel_name_list = ts3conn.channel_name_list()
        for channel_name in channel_name_list:
            if msg[len("!multimove "):].startswith(channel_name):
                source_name = channel_name
                dest_name = msg[len("!multimove ") + len(source_name)+1:]
    else:
        source_name = channels[0]
        dest_name = channels[1]
    if source_name == "":
        Bot.send_msg_to_client(ts3conn, sender, "Source channel not found")
        return
    if dest_name == "":
        Bot.send_msg_to_client(ts3conn, sender, "Destination channel not found")
        return
    try:
        channel_matches = ts3conn.channelfind(source_name)
        channel_candidates = [chan for chan in channel_matches if chan.get("channel_name", '-1').startswith(source_name)]
        if len(channel_candidates) == 1:
            source = channel_candidates[0].get("cid", '-1')
        elif len(channel_candidates) == 0:
            Bot.send_msg_to_client(ts3conn, sender, "Source channel could not be found.")
        else:
            channels = [chan.get('channel_name') for chan in channel_candidates]
            Bot.send_msg_to_client(ts3conn, sender, "Multiple source channels found: " + ", ".join(channels))
    except TS3QueryException:
        Bot.send_msg_to_client(ts3conn, sender, "Source channel not found")
    try:
        channel_matches = ts3conn.channelfind(dest_name)
        channel_candidates = [chan for chan in channel_matches if chan.get("channel_name",
            '-1').startswith(dest_name)]
        if len(channel_candidates) == 1:
            dest = channel_candidates[0].get("cid", '-1')
        elif len(channel_candidates) == 0:
            Bot.send_msg_to_client(ts3conn, sender, "Destination channel could not be found.")
        else:
            channels = [chan.get('channel_name') for chan in channel_candidates]
            Bot.send_msg_to_client(ts3conn, sender, "Multiple destination channels found: " + ", ".join(channels))
    except TS3QueryException:
        Bot.send_msg_to_client(ts3conn, sender, "Destination channel not found")
    if source != None and dest != None:
        try:
            client_list = ts3conn.clientlist()
            client_list = [client for client in client_list if client.get("cid", '-1') == source]
            for client in client_list:
                clid = client.get("clid", '-1')
                logger.info("Found client in channel: " + client.get("client_nickname", "") + " id = " + clid)
                ts3conn.clientmove(int(dest), int(clid))
        except TS3QueryException as e:
            Bot.send_msg_to_client(ts3conn, sender, "Error moving clients: id = " +
                    str(e.id) + e.message)


@command('version',)
@group('.*')
def send_version(sender, msg):
    Bot.send_msg_to_client(bot.ts3conn, sender, __version__)


@command('whoami',)
@group('.*')
def whoami(sender, msg):
    Bot.send_msg_to_client(bot.ts3conn, sender, "Geht dich nichts an!")


@command('stop',)
@group('Server Admin',)
def stop_bot(sender, msg):
    Moduleloader.exit_all()
    bot.ts3conn.quit()
    logger.warning("Bot was quit!")


@command('restart',)
@group('Server Admin', 'Moderator',)
def restart_bot(sender, msg):
    Moduleloader.exit_all()
    bot.ts3conn.quit()
    logger.warning("Bot was quit!")
    import main
    main.restart_program()

@command('commandlist',)
@group('Server Admin', 'Moderator',)
def get_command_list(sender, msg):
    Bot.send_msg_to_client(bot.ts3conn, sender, list(bot.command_handler.handlers.keys()))


@command('joinme',)
@group('.*')
def join_my_channel(sender, msg):
    pass


