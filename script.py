import json
import time
import threading
from urllib import request
from progress.bar import Bar
from datetime import datetime

filename = "lista_urls.txt"

def create_json(nomeJson, logger):
    with open(nomeJson, 'w') as fp:
        json.dump(logger, fp)
def execute_url_list(casa, logger):
    try:
        start = time.time()
        result = request.urlopen(casa)
        end = time.time()
        if result.status != 200:
            log = {'url':casa,'status':result.status,'tempo':end-start}
            logger['erros'].append(log)
    except Exception as e:
        end = time.time()
        if e:
            log = {'url':casa, 'status':str(e),'tempo':end-start}
            logger['erros'].append(log)
    return (logger)
    create_json(nomeJson, logger)

def threads(casas, logger, nomeJson):
    bar = Bar('Loading', fill='@', suffix='%(percent)d%%',max= 1000)
    threads = [threading.Thread(target=execute_url_list,
              args=(casa,logger, nomeJson, )) for casa in casas]
    print("Start")
    for thread in threads:
        thread.start()
        bar.next()
    for thread in threads:
        thread.join()
    bar.goto(1000)


def main():
    while(True):
        logger = {'erros':[]}
        nomeJson = str(datetime.now()) +".json"
        with open(filename) as casas:
            casas = list(casas)
            casas = casas[1:]
        threads(casas, logger, nomeJson)
        print()
        print("Done!")
        time.sleep(300)



if __name__ == '__main__':
    main()
