# Youtube: https://www.youtube.com/watch?v=d2GBO_QjRlo
from selenium import webdriver
#from secrets import password
from time import sleep
import getpass

class InstaBot:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.instagram.com/')
        self.username = username
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
        self.driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(4)
    
    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/following')]".format(self.username))\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/followers')]".format(self.username))\
            .click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]

        with open('unfollower_'+username+'.txt', 'w') as f:
            for item in not_following_back:
                f.write("%s\n" % item) 
        print('The total number of Unfollowers: {}'.format(len(not_following_back)))
        print('Unfollowers have been saved in a text file: unfollower_{}.txt'.format(username))
        #print(not_following_back)

    def _get_names(self):
        sleep(2)
        # sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        # self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        # sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        return names

if __name__ == '__main__':
    print('Made with Love by Ashish: @ashi_s.h')
    username = input('Enter Instagram\'s User Name: ')
    print('We will never save your password')
    password = getpass.getpass('Enter Password: ')
    my_bot = InstaBot(username, password)
    my_bot.get_unfollowers()