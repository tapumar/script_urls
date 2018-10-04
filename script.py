import json
import time
import threading
from urllib import request
from progress.bar import Bar
from datetime import datetime

while(True):
    logger = {'erros':[]}
    error = []
    filename = "lista_urls.txt"
    nomeJson = str(datetime.now()) +".json"
    with open(filename) as casas:
        casas = list(casas)
        bar = Bar('Loading', fill='@', suffix='%(percent)d%%',max= 1000)
        casas = casas[1:]

    def execute_url_list(casa):
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

        with open(nomeJson, 'w') as fp:
            json.dump(logger, fp)

    threads = [threading.Thread(target=execute_url_list, args=(casa,)) for casa in casas]

    #Rotina da Thread
    print("Start")
    for thread in threads:
        thread.start()
        bar.next()
    for thread in threads:
        thread.join()
    bar.goto(1000)
    print()
    print("Done!")
    time.sleep(300)
