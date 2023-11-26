from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from shutil import which
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from sqlalchemy import create_engine
data = pd.read_csv('realtorsAgentUrls.csv')
urls = list(data['agent_url'].unique())
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driver = webdriver.Firefox(firefox_profile=firefox_profile)
count = 0
for rest_url in urls[count:]:
    print(count,rest_url)
    driver.get(rest_url)
    try:
        try:
            name=driver.find_element(By.XPATH,"//*[@id='profile-section']/div[1]/div[2]/p[1]").text
        except:
            name=""
        try:
            company=driver.find_element(By.XPATH,"//*[@id='profile-section']/div[1]/div[2]/p[2]").text
        except:
            company=""
        try:
            rating=driver.find_elements(By.XPATH,"//*[@id='rev']/span[1]")[1].text
        except:
            rating=""
        try:
            image_url=driver.find_element(By.XPATH,"//img[@class='jsx-2929697302 profile-img']").get_attribute("src")
        except:
            image_url=""
        try:
            #if driver.find_element(By.XPATH,"//*[@id='agent-description']/div/span/span[1]/span[11]/span/span[2]/a/p/button").text=="Continue reading":
            driver.find_element(By.XPATH,"//*[@id='agent-description']/div/span/span[1]/span[11]/span/span["
                                         "2]/a/p/button").click()
            about=driver.find_element(By.XPATH,"//*[@id='agent-description']/div/span[1]/span[1]/p").text
        except:
            about=driver.find_element(By.XPATH,"//*[@id='agent-description']").text
        try:
            l = about.split("BRE")[1]
            L = [s for s in l.split() if s.isdigit()]
            if len(L[0])>=6:
                lic = L[0]
        except:
            lic=""
        try:
            experience=driver.find_element(By.XPATH,"//*[@class='jsx-2966494122 preview-profile-subtitle title-down-space']").text
        except:
            experience=""
        try:
            price_range=driver.find_element(By.XPATH,"//*[@class='jsx-2966494122 preview-profile-sub-subtitle title-down-space']").text
        except:
            price_range=""
        html_list = driver.find_element(By.XPATH,"//*[@id='datalist1']")
        items = html_list.find_elements(By.TAG_NAME,"li")
        areas_served=[]
        try:
            if driver.find_element(By.XPATH,"//*[@id='served']/p").text=="Show more areas served":
                driver.find_element(By.XPATH,"//*[@id='served']/p").click()
            for item in items:
                text = item.text
                areas_served.append(text)
        except:
            for item in items:
                text = item.text
                areas_served.append(text)

        specializations=[]
        try:
            if driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                            "1]/div/div/div/div/div[1]/div[3]/div[3]/h3").text=="Specializations":
                html_list = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                                         "1]/div/div/div/div/div[1]/div[3]/div[3]/div/ul")
                items = html_list.find_elements(By.TAG_NAME,"li")
                for item in items:
                    spec = item.text
                    specializations.append(spec)
            elif driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                              "1]/div/div/div/div/div[1]/div[3]/div[4]/h3").text=="Specializations":
                html_list = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                                         "1]/div/div/div/div/div[1]/div[3]/div[4]/div/ul")
                items = html_list.find_elements(By.TAG_NAME,"li")
                for item in items:
                    spec = item.text
                    specializations.append(spec)
        except:
            specializations.append("")
        languages=[]
        try:
            html_list = driver.find_element(By.XPATH,"//div[@class='jsx-2966494122 languages-content']/ul")
            items = html_list.find_elements(By.TAG_NAME,"li")
            for item in items:
                lang = item.text
                languages.append(lang)
        except:
            languages.append("")
        try:
            video = driver.find_element(By.XPATH,"//div[@class='jsx-962941538 preview-vedio-preview']/iframe").get_attribute("src")
        except:
            video = ""
        contact=[]
        mbl=[]
        fx=[]
        ofc=[]
        othr=[]
        try:
            html_list = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                                     "1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]")
            items = html_list.find_elements(By.TAG_NAME,"div")
            for item in items:
                html_list = driver.find_element(By.XPATH,"//*[@id='contact-details']/div[1]/div/div[2]/div[1]/p/a").text
                contact_number = item.text
                contact.append(contact_number)
        except:
            contact.append("")
        mbl,ofc,fx,othr,hm=[a for a in contact if "Mobile" in a],[a for a in contact if "Office" in a],[a for a in contact if "Fax" in a],[a for a in contact if "Other" in a],[a for a in contact if "Home" in a]
        try:
            mobile=mbl[0][:14]
        except:
            mobile=""
        try:
            office=ofc[0][:14]
        except:
            office=""
        try:
            fax=fx[0][:14]
        except:
            fax=""
        othr.extend(mbl[1:])
        othr.extend(ofc[1:])
        othr.extend(fx[1:])
        othr.extend(hm[0:])
        try:
            agent_website = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                                         "1]/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/p["
                                                         "1]/a").get_attribute("href")
        except:
            agent_website = ""
        try:
            company_website = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                                           "1]/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/p["
                                                           "2]/a").get_attribute("href")
        except:
            company_website = ""
        address=[]
        try:
            html_list = driver.find_element(By.XPATH,"//*[@id='contact-details']/div[3]/div[2]")
            items = html_list.find_elements(By.TAG_NAME,"p")
            for item in items:
                address.append(item.text)
        except:
            address.append("")
        try:
            zip1 = [int(s) for s in address[-1].split() if s.isdigit()][-1]
        except:
            zip1=""
        try:
            state = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                                 "1]/div/div/div/div/div[2]/div[1]/div[3]/div[2]/p[2]/span[3]").text
        except:
            state="NH"
        social_media=[]
        try:
            html_list = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                                     "1]/div/div/div/div/div[2]/div[1]/div[2]/div")
            items = html_list.find_elements(By.TAG_NAME,"a")
            for item in items:
                if item.text=="facebook":
                    S1 = item.get_attribute("href")
                    social_media.append(S1)
                if item.text=="Twitter":
                    S2 = item.get_attribute("href")
                    social_media.append(S2)
        except:
            social_media.append("")
        twitter=[]
        facebook=[]
        linkedin=[]
        try:
            twitter=[a for a in social_media if "twitter" in a]
        except:
            twitter.append("")
        try:
            facebook=[a for a in social_media if "facebook" in a]
        except:
            facebook.append("")
        try:
            linkedin=[a for a in social_media if "linkedin" in a]
        except:
            linkedin.append("")
        Listings=[]
        try:
            listings = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div[2]/div["
                                                    "1]/div[2]/div/div/div/div[1]/div/div[2]").text
            Listings = [str(s) for s in listings.split() if s.isdigit()]
        except:
            Listings.append('')
        Reviews = []
        try:
            ratings = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div[2]/div["
                                                   "1]/div[3]/div/div/div[1]/div/div[2]").text
            Reviews = [str(s) for s in ratings.split() if s.isdigit()]
        except:
            Reviews.append('')
        Recommendations = []
        try:
            recom = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div[2]/div[1]/div["
                                                 "4]/div/div/div[1]/div/div[2]").text
            Recommendations = [str(s) for s in recom.split() if s.isdigit()]
        except:
            Recommendations.append('')
        Certification=[]
        try:
            html_list = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/section/div/div/div["
                                                     "1]/div/div/div/div/div[1]/div[3]/div[1]/ul")
            cert = html_list.find_elements(By.TAG_NAME,"i")
            for i in cert:
                certification = i.get_attribute("class")
                Certification.append(certification.split("icon-",1)[1])
        except:
            Certification.append("")
        data_dict = {"agent_url":rest_url,"agent_dp":image_url,"agent_name":name,"agent_phone":mobile,"agent_bio":about,"agent_role":"broker",
                    "agent_license":lic,"agent_areaserved":",".join(areas_served),"agent_specialization":",".join(specializations),
                    "agent_facebook":",".join(facebook),"agent_linkedin":",".join(linkedin),"agent_twitter":",".join(twitter),
                    "agent_video":video,"agent_credentials":",".join(Certification),
                    "agent_site":agent_website,"agent_rating":rating,"agent_price_range":price_range,
                    "agent_experience":experience,"agent_listing":"|".join(Listings),'agent_reviews':",".join(Reviews),
                    "agent_spoken_languages":",".join(languages),"agent_recommendations":",".join(Recommendations),
                    "office_name":company,"office_address":",".join(address),"office_zip":zip1,"office_site":company_website,
                    "office_phone":office,"office_fax":fax, "other_numbers": ",".join(othr), "state":state
                    }
        data_df = pd.DataFrame(data_dict,index=[0], columns= ['agent_url','agent_dp','agent_name','agent_phone','agent_bio','agent_role','agent_license','agent_areaserved','agent_specialization','agent_facebook','agent_linkedin','agent_twitter','agent_video','agent_credentials','agent_site','agent_rating','agent_price_range','agent_experience','agent_listing','agent_reviews','agent_spoken_languages','agent_recommendations','office_name','office_address','office_zip', 'office_site','office_phone','office_fax','other_numbers','state'])
        # engine = create_engine('postgresql://postgres:smartsetter@ss-db-data-dev.cpeist8s9qou.us-west-2.rds.amazonaws.com:5432/postgres')
        # data_df.to_sql('realtor', con=engine, index=False, if_exists='append')
        with open("realtor1.csv",'a',newline='',encoding='utf-8') as f:
           data_df.to_csv(f, mode='a',header=f.tell()==0)
        count +=1
    except:
        count+=1
