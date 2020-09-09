import importlib
import Bot
import requests
import Moduleloader
import logging
import json
import time
#import ts3.Events as Events
# from utility import parse_json, save_to_txt, read_from_json, wipe_json_file
bot = None

API_KEY = "b15e9ec1247d0cc0965e0883351e5cc7682bd78b890d6ffaa7802a0158457176"



@Moduleloader.setup
def vt_setup(ts3bot):
    global bot
    bot = ts3bot
    print("vt loaded")


@Moduleloader.command('vt_test',)
@Moduleloader.group('Server Admin',)
def test_command(sender, msg):
    print("test")
    Bot.send_msg_to_client(bot.ts3conn, sender," woooorking!")



@Moduleloader.command("vt",)
@Moduleloader.group('.*',)
def check_url(sender, url):
    # try:
    #     response = check_if_already_scanned(url)
    #     print(response)
    #     if response["response_code"] != 0:
    #         response = make_url_request(url)
    #         if response["response_code"] != 0:
    #            pass
    #         analysis = make_analysis_request(response["data"]["id"])
    #     else:
    #         analysis = make_analysis_request(response["data"]["id"])
    #     if analysis["data"]["attributes"]["status"] == "queued":
    #         Bot.send_msg_to_client(bot.ts3conn, sender, f"{url} Wird über VirusTotal gescanned, ich melde mich wenn der Scan fertig ist.")

    #     while analysis["data"]["attributes"]["status"] == "queued":
    #         time.sleep(5)
    #         analysis = make_analysis_request(response["data"]["id"])
        
    #     msg = build_up_msg(analysis["data"]["attributes"]["stats"], analysis["meta"]["url_info"]["url"])
    #     Bot.send_msg_to_client(bot.ts3conn, sender, msg)

    # except (Exception) as err:
    #     logging.warning(f"error while checking virustotal with link: {url} \n{err}")
    #     Bot.send_msg_to_client(bot.ts3conn, sender, f"Tut mir leid, da ist etwas schief gelaufen: \n {err} \n {response}")
    #     print(response)
    
    url = clean_url(url)
    try: 
        response = check_if_already_scanned(url)
        if not response["data"]["id"]:
            response = make_url_request(url)
            analysis = make_analysis_request(response["data"]["id"])
        else:
            analysis = make_analysis_request(response["data"]["id"])
        if analysis["data"]["attributes"]["status"] == "queued":
            Bot.send_msg_to_client(bot.ts3conn, sender, f"{url} Wird über VirusTotal gescanned, ich melde mich wenn der Scan fertig ist.")
            
        while analysis["data"]["attributes"]["status"] == "queued":
            time.sleep(5)
            analysis = make_analysis_request(response["data"]["id"])
        
        msg = build_up_msg(analysis["data"]["attributes"]["stats"], analysis["meta"]["url_info"]["url"])
        Bot.send_msg_to_client(bot.ts3conn, sender, msg)

    except (Exception) as err:
        logging.warning(f"error while checking virustotal with link: {url} \n{err}")
        Bot.send_msg_to_client(bot.ts3conn, sender, f"Tut mir leid, da ist etwas schief gelaufen: \n {err} \n {response} \n Vielleicht hast du das falsche Format benutzt? \"!vt <link>\"""")
        print(response)


def clean_url(url):
    #input =  !vt [URL]https://forum.pleaseignore.com/topic/108488-test-broadcast-please-ignore/[/URL]
    url = str(url)
    url = url.strip("[/URL]").strip("!vt")
    url = url[6:]
    return url


def build_up_msg(results, url):
    result_str = "\n Deine Scan Ergebnisse sind da: \n"
    for key in results:
        result_str = result_str + f"{key} : {results[key]}" + "\n"
    return result_str


def check_if_already_scanned(url):
    # response = requests.get(f"https://www.virustotal.com/vtapi/v2/url/report?apikey={API_KEY}&resource={url}") v2 API
    # return parse_json(response)
    
    headers = {
    'x-apikey': f"{API_KEY}",
    }

    data = {"url": f"{url}"}

    response = requests.post('https://www.virustotal.com/api/v3/urls', data=data, headers=headers)
    return parse_json(response)


def make_url_request(url):
    data = {
    'apikey': f'{API_KEY}',
    'url': f'{url}'
    }

    response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=data)
    return parse_json(response)


def make_analysis_request(id):
    headers = {
    'x-apikey': f"{API_KEY}",}

    response = requests.get(f"https://www.virustotal.com/api/v3/analyses/{id}", headers=headers)
    
    return parse_json(response)

#TODO: save state with @exit wrapper
#TODO: save analysis to file and check the file before submitting another request




    
#urls = ["https://www.tines.io/blog/virustotal-api-security-automation", "https://forum.pleaseignore.com/topic/108488-test-broadcast-please-ignore/", "https://github.com/Murgeye/teamspeak3-python-bot#quotes-1"]

    
#region util

def save_to_txt(filename, data):
    with open(f"{filename}", "a+") as data_file:
        if type(data) == str:
            data_file.write(data + "\n")
        else:
            json.dump(data, data_file, indent=4)

        

def wipe_json_file(filename):
    with open(f"{filename}", "w") as data_file:
        data_file.truncate(0)


def read_from_json(filename):
    ''' returns a list line by line '''
    with  open(f"{filename}", "r") as data_file:
        data = data_file.readlines()
        return data 


def parse_json(response):
    json_response = json.loads(response.text)
    return json_response

#endregion


def main():
    #check_url("me", "https://forum.pleaseignore.com/topic/108488-test-broadcast-please-ignore/")
    #print(clean_url("!vt [URL]https://forum.pleaseignore.com/topic/108488-test-broadcast-please-ignore/[/URL]"))
    pass








if __name__ == "__main__":
    main()

