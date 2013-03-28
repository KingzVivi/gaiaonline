import cookielib, re, random

try:
    import mechanize # http://wwwsearch.sourceforge.net/mechanize/
except Exception, err:
    log = open("error.log", "w")
    log.write("Install additional libraries")
    log.close()
    raise Exception(str(err))

class Gaia(object):
    def __init__(self, username, password):
        #---Account Details
        self.username = username
        self.password = password
        self.goldStart = 0
        #---Browser Setup
        self.br = mechanize.Browser() # this will be used as our browser, and will help automate forms
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.cookies = cookielib.LWPCookieJar() #finish building our browser, and cookies 
        self.br.open("http://gaiaonline.com")
        self.br.set_handle_robots(False)
        #---Login
        self.br.select_form(nr=0)
        self.br["username"] = self.username
        self.br["password"] = self.password
        self.br.submit()
        
        self.login = self.br.response().get_data()
        if "Welcome back" in self.login:
            print self.username + " logged in"
            self.goldStart = self.getGold()
            print "Gold : " + self.goldStart
            
    def getProfit(self):
        return (int(self.getGold()) - int(self.goldStart))
       
    def getGold(self):
        gaia = self.br.open("http://www.gaiaonline.com").read()
        self.gold = re.search('<span id="go1d_amt">(.*?)</span>', gaia).group(1)
        return str(self.gold).replace(',', '')
              
    def dailyChance(self, itemId):
        dailyChance = self.br.open("http://www.gaiaonline.com/dailycandy/?mode=ajax&action=issue&list_id=" + str(itemId) ).read()
        #print dailyChance
        if "success" in dailyChance:
            reward = re.search('<name>(.*?)</name>', dailyChance).group(1)
            return reward
        else:
            return False
    
    def dumpsterDive(self ):
        dive = self.br.open("http://www.gaiaonline.com/dumpsterdive/", "mode=showConfirmed").read()
        if "Pete" in dive:
            return "Pete looks a little crazy XD"
        else:
            findReward = re.search('<div id="grant_text1">(.*?)</div>', dive).group(1)
            return findReward
    
    def arenaVoter(self):
        arenas = ["http://www.gaiaonline.com/arena/art/comics/vote/#title",
                  "http://www.gaiaonline.com/arena/art/painting-and-drawing/vote/#title",
                  "http://www.gaiaonline.com/arena/art/photography/vote/#title",
                  "http://www.gaiaonline.com/arena/writing/fiction/vote/#title",
                  "http://www.gaiaonline.com/arena/writing/non-fiction/vote/#title",
                  "http://www.gaiaonline.com/arena/writing/poetry-and-lyrics/vote/#title",
                  "http://www.gaiaonline.com/arena/writing/high-school-flashback/vote/#title",
                  "http://www.gaiaonline.com/arena/gaia/homes/#title",
                  "http://www.gaiaonline.com/arena/gaia/original-avatar/vote/#title",
                  "http://www.gaiaonline.com/arena/gaia/cosplay-avatar/vote/#title"]
        arena = self.br.open( random.choice(arenas) ).read()
        voteUrl = re.search("url:'(.*?)'", arena).group(1)
        self.br.open( "http://www.gaiaonline.com" + voteUrl + str( random.randint(2,4) ), None)
        
if __name__ == '__main__':
    #replace with your usn/pass
    #testing code can be done here
    bot = Gaia("username", "password")
    
