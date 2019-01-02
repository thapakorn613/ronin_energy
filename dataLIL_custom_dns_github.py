#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#
#--------------- Python code for READ and POST to datalogging LIL --------------------#
#-------------------------------------------------------------------------------------#
#------------------ A/C Energy Consumption Measurement System ------------------------#
#---------------------- Department of Computer Engineering ---------------------------#
#------------ Faculty of Engineering, Chiang Mai University, Thailand ----------------#
#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#

import urllib2,urllib,httplib,socket,ssl,time,json,os,sys
import read_rs485_github

# Import setting json file
cur_path = os.path.abspath(os.path.dirname(sys.argv[0]))
key_path = os.path.join(cur_path,'apikey_write.json')
config_path = os.path.join(cur_path,'config.json')

keyFile = open(key_path)
key = json.load(keyFile)
keyFile.close()

configFile = open(config_path)
config = json.load(configFile)
configFile.close()

# Init variable
error_count = 0
id = int(config['start_id'])

# Custom dns by using socket / httplib method
def MyResolver(host):
  if host == config['host']:
    return config['ip_host']
  else:
    return host

class MyHTTPConnection(httplib.HTTPConnection):
  def connect(self):
    self.sock = socket.create_connection((MyResolver(self.host),self.port),self.timeout)

class MyHTTPSConnection(httplib.HTTPSConnection):
  def connect(self):
    sock = socket.create_connection((MyResolver(self.host), self.port), self.timeout)
    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)

class MyHTTPHandler(urllib2.HTTPHandler):
  def http_open(self,req):
    return self.do_open(MyHTTPConnection,req)

class MyHTTPSHandler(urllib2.HTTPSHandler):
  def https_open(self,req):
    return self.do_open(MyHTTPSConnection,req)


opener = urllib2.build_opener(MyHTTPHandler,MyHTTPSHandler)
urllib2.install_opener(opener)

# Post data function
def senddata(data):
    body = urllib.urlencode(data)
    h = urllib2.Request(config['post_url'], body)
    try:
        resp = urllib2.urlopen(h)
        return resp.read()
    except:
        pass

# Main loop programs
while True:
    if id > int(config['end_id']):
        id = int(config['start_id'])
    try:
        data = {'key': key[str(id)], config['field_energy']: read_rs485_github.readenergy(id),config['field_current']: read_rs485_github.readcurr(id)}
    except IOError:
        error_count += 1
        print "Count Error : %s" % error_count
        print "Cannot connect modbus channel : %s" % id
        error =  {'key': key['error_channel'], config['field_err_count']: error_count, config['field_err_channel']: id}
        print senddata(error)
        time.sleep(int(config['delay_time']))
        try:
            data = {'key': key[str(id)], config['field_energy']: read_rs485_github.readenergy(id),config['field_current']: read_rs485_github.readcurr(id)}
        except IOError:
            id += 1
            continue
    print senddata(data)
    print "Channel : %s" % id
    id += 1
