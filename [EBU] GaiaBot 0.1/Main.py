'''

@author: king.vivi@gmail.com
@note: This is for python 2.7, and requires the Mechanize library

'''
from Gaia import Gaia

if __name__ == '__main__':
    username = raw_input("Enter your username:")
    password = raw_input("Enter your password:")
    
    bot = Gaia(username, password)
    
    print "Daily Cash"
    
    for dailyId in [1,2,3,4,5,8]:
        print bot.dailyChance( dailyId )
  
    print "Profit:" ,bot.getProfit()