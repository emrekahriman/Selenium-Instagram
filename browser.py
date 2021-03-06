from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from time import sleep


user = input('Kullanıcı Adı: ')
pw = input('Şifre: ')



class Browser:
    def __init__(self, link):
        self.link = link
        self.browser = webdriver.Firefox(executable_path='geckodriver.exe')  # geckodriver yolunu yazıyoruz
        Browser.goInstagram(self)
       
        
    def goInstagram(self):
        self.browser.get(self.link)
        sleep(2)
        Browser.login(self)
        #Browser.getFollowers(self)  #Takipcileri Getir
        #Browser.getFollowing(self)  #Takip Ettiklerimi Getir
        Browser.getComments(self)   #Linki verilen gonderiye ait yorumları getir


    def login(self):
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')

        username.send_keys(user)
        password.send_keys(pw)

        loginBtn = self.browser.find_element_by_css_selector('.L3NKy > div:nth-child(1)')
        loginBtn.click()
        sleep(4)

        self.browser.get(self.link + '/' + user)
        sleep(3)


    def scrollDown(self):
        jsKomut = """
        sayfa = document.querySelector('.isgrP');
        sayfa.scrollTo(0, sayfa.scrollHeight);
        var sayfaSonu = sayfa.scrollHeight;
        return sayfaSonu; 
        """
        sayfaSonu = self.browser.execute_script(jsKomut)
        while True:
            son = sayfaSonu
            sleep(2)
            sayfaSonu = self.browser.execute_script(jsKomut)
            if son == sayfaSonu:
                break

    
    def getFollowers(self):
        self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
        sleep(3)
        Browser.scrollDown(self)  #Tüm takipçileri çekmek için scrollbar'ı aşağı kaydıracak fonksiyonu çağırıyoruz
        followers = self.browser.find_elements_by_css_selector('.FPmhX.notranslate._0imsa')
        i = 0
        for follower in followers:
            i +=1
            print('{0:4} -> {1}'.format(i, follower.text))


    def getFollowing(self):
        self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
        sleep(3)
        Browser.scrollDown(self)  #Tüm takipçileri çekmek için scrollbar'ı aşağı kaydıracak fonksiyonu çağırıyoruz
        followers = self.browser.find_elements_by_css_selector('.FPmhX.notranslate._0imsa')
        i = 0
        for follower in followers:
            i +=1
            print('{0:4} -> {1}'.format(i, follower.text))



    def getComments(self):
        self.browser.get('https://www.instagram.com/p/CI3lfc-AXTB/')
        sleep(3)
        while True:
            try:
                yorumYukleBtn = self.browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button/span')
                yorumYukleBtn.click()
                sleep(2)
            except NoSuchElementException:
                break
        comments = self.browser.find_elements_by_css_selector('.C4VMK')
        i = 0
        for comment in comments:
            i += 1
            print('{0:4} -> {1}'.format(i, comment.text))
