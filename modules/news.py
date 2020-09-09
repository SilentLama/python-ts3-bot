import importlib
import Bot
import Moduleloader
import logging
bot = None




@Moduleloader.setup
def news_setup(ts3bot):
    global bot
    bot = ts3bot
    print("news loaded")


@Moduleloader.command("news",)
@Moduleloader.group('.*',)
def show_news(sender, msg):
    news = "".join(read_from_txt()) 
    Bot.send_msg_to_client(bot.ts3conn, sender, "\n" + news)


@Moduleloader.command("add_news",)
@Moduleloader.group('Server Admin',)
def write_news(sender, msg):
    data = msg.replace("!add_news ", "")
    write_to_txt(data)
    Bot.send_msg_to_client(bot.ts3conn, sender, f"\nNews wurden hinzugefügt: \n{data}")


@Moduleloader.command("delete_news",)
@Moduleloader.group('Server Admin',)
def delete_news(sender, msg):
    wipe_news()
    Bot.send_msg_to_client(bot.ts3conn, sender, "\nAlle News wurden gelöscht.")


def read_from_txt():
    ''' returns a list of the news items '''
    with open("./data/news.txt", "r", encoding="utf8") as news_file:
        news = news_file.readlines()
    
    return news


def write_to_txt(data):
    with open("./data/news.txt", "a", encoding="utf8") as news_file:
        news_file.write(data + "\n")


def wipe_news():
     with open("./data/news.txt", "w", encoding="utf8") as news_file:
         news_file.truncate(0)







if __name__ == "__main__":
    pass