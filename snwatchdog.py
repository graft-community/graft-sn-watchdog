import sys
import subprocess
import requests
import json
from time import gmtime, strftime, sleep
from bcolors import bcolors

class GraftSN(object):

        def __init__(self):

                GraftSN.url = 'http://127.0.0.1:28681/json_rpc'
                GraftSN.payloadcurl = '{"jsonrpc":"2.0","id":"0","method":"get_info"}'
                GraftSN.headerscurl = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                GraftSN.snurl = 'http://127.0.0.1:28690/debug/supernode_list/0'
                GraftSN.stakewallet = '' # Paste your SN stake wallet address inside '' to monitor
                GraftSN.TELEGRAM_TOKEN = "" # Put Here Your TokenID inside "" to send to your Telegram Botfather bot'
                GraftSN.TELEGRAM_CHAT_ID  = "" # Put Here Your ChatID inside "" to send to your Telegram Botfather bot # If you want telegram reporting uncomment any ##self.telegram_tx below
                self.loop()

        def loop(self):
                try:
                    while True:
                        #print ('Loop')
                         
                         try:
                             outputgraftnoded = requests.post(GraftSN.url, data=GraftSN.payloadcurl, headers=GraftSN.headerscurl)
                             jsondatagn = json.loads(outputgraftnoded.text)
                             jsondata = json.loads(outputgraftnoded.text)
                             status = jsondata["result"]["status"]
                             height = self.dectostr(jsondata["result"]["height"])
                             incon = self.dectostr(jsondata["result"]["incoming_connections_count"])
                             outcon = self.dectostr(jsondata["result"]["outgoing_connections_count"])
                             txpoolsize = self.dectostr(jsondata["result"]["tx_pool_size"])
                             self.advprint("Block Height: %s" % height, bcolors.OKGREEN, True)
                             self.advprint(" Status: %s" % status, bcolors.OKGREEN, False)
                             self.advprint(" In Connections: %s" % incon, bcolors.OKGREEN, False)
                             self.advprint(" Out Connections: %s" % outcon, bcolors.OKGREEN, False)
                             self.advprint(" Tx Pool Size: %s" % txpoolsize, bcolors.OKGREEN, False)
                             ##self.telegram_tx("SN 01 " + status + " Block Height: " + height + " In Connections " + incon + " Out Connections " + outcon + " Tx Pool Size: " + txpoolsize)
							 
                         except requests.exceptions.HTTPError as errgnh:
                             self.advprint("GraftNoded Http Error: %s" % errgnh, bcolors.FAIL)
                         except requests.exceptions.ConnectionError as errgnc:
                             self.advprint("GraftNoded Error Connecting: %s" % errgnc, bcolors.FAIL)
                         except requests.exceptions.Timeout as errgnt:
                             self.advprint("GraftNoded Timeout Error: %s" % errgnt, bcolors.FAIL)
                         except requests.exceptions.RequestException as errgn:
                             self.advprint("GraftNoded OOps: Something Else %s" % errgn, bcolors.FAIL)
                         except IndexError as gnindxe:
                             self.advprint("GraftNoded Index Error: %s" % gnindxe, bcolors.FAIL)
                         except ValueError as gnvalerr:
                             self.advprint("GraftNoded Value Error: %s" % gnvalerr, bcolors.FAIL)
                         try:
                             outputgraftserver = requests.get(GraftSN.snurl)
                             jsondatasn = json.loads(outputgraftserver.text)
                             pos=0
                             for i in range(1,len(jsondatasn["result"]["items"])):
                                jsondatasnsw = (jsondatasn["result"]["items"][i])
                                for (k, v) in jsondatasnsw.items():
                                   if str(v) == GraftSN.stakewallet:
                                     pos=i

                             jsondatasnsw = (jsondatasn["result"]["items"][pos])
                             for (k, v) in jsondatasnsw.items():
                                if k == 'LastUpdateAge':
                                  updateage = str(v)
                             self.advprint("SN List Count: %s" % len(jsondatasn["result"]["items"]), bcolors.OKBLUE)
                             self.advprint(" SN Update Age: %s" % updateage, bcolors.OKBLUE, False)
                             ##self.telegram_tx("SN List Count: " + self.dectostr(len(jsondatasn["result"]["items"])) + " SN Update Age: " + updateage)						 
                             if len(jsondatasn["result"]["items"]) <= 5:
                               bashCommandgskill = "killall -9 graft_server"
                               bashCommandgnkill = "killall -9 graftnoded"
                               subprocess.check_output(['bash','-c', bashCommandgskill])
                               subprocess.check_output(['bash','-c', bashCommandgnkill])
                               self.advprint("Reset Graftnoded and Graft_Server", bcolors.FAIL)
                               ##self.telegram_tx("SN 01 Reset Graftnoded and Graft_Server")
                         except requests.exceptions.HTTPError as errgsh:
                             self.advprint("GraftServer Http Error: %s" % errgsh, bcolors.FAIL)
                         except requests.exceptions.ConnectionError as errgsc:
                             self.advprint("GraftServer Error Connecting: %s" % errgsc, bcolors.FAIL)
                         except requests.exceptions.Timeout as errgst:
                             self.advprint("GraftServer Timeout Error: %s" % errgst, bcolors.FAIL)
                         except requests.exceptions.RequestException as errgs:
                             self.advprint("GraftServer OOps: Something Else %s" % errgs, bcolors.FAIL)
                         except IndexError as gsindxe:
                             self.advprint("GraftServer Index Error: %s" % gsindxe, bcolors.FAIL)
                         except ValueError as gsvalerr:
                             self.advprint("GraftServer Value Error: %s" % gsvalerr, bcolors.FAIL)
                         
                         sleep(1800) # Change loop timeout to what you want currently 30mins

                except KeyboardInterrupt:
                    print('KeyboardInterrupt')
                    sys.exit()

        def dectostr(self, dec, prec=8):
                #
                return '{:.0f}'.format(dec) if prec == 8 else '{:.2f}'.format(dec)

        def advprint(self, buf, color=None, newline=True):
                try:
                        cstr =  color + buf + bcolors.ENDC if color != None else buf
                        sys.stdout.write("\n[%s]: " % strftime("%H:%M:%S", gmtime()) + cstr if newline else cstr)
                        sys.stdout.flush()
                except IOError:
                        pass

        def telegram_tx(self, record):
                TELEGRAM_TOKEN = GraftSN.TELEGRAM_TOKEN 
                TELEGRAM_CHAT_ID = GraftSN.TELEGRAM_CHAT_ID
                log_entry = (record);
                payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
                requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN), data=payload).content
                return

        def cpuusage(self, record):
                if float(record) > 28:
                    print('CpuHigh')
                else:
                    bashCommandreboot = "reboot" # For future CPU monitor.
                    subprocess.check_output(['bash','-c', bashCommandreboot])
                return
				
main                = GraftSN()



