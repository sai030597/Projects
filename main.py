import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import pandas as pd

import warnings

warnings.filterwarnings("ignore")

import undetected_chromedriver as uc

# for sample o/p
driver = uc.Chrome()
urls = [
    'https://www.redfin.com/city/30794/TX/Dallas/filter/viewport=33.15095:32.4665:-96.2551:-97.21228,'
    'no-outline/page-4']
dataDf = pd.DataFrame()
for url in urls:
    driver.get(url)
    driver.maximize_window()
    links = driver.find_elements(By.CSS_SELECTOR, 'a.slider-item')
    e = []
    for q in links:
        e.append(q.get_attribute('href'))
    for i in e:
        driver.get(i)
        # driver.get('https://www.redfin.com/TX/Coppell/100-Mockingbird-Ln-75019/home/31279063#property-history')
        print(i)
        time.sleep(5)
        try:
            address = driver.find_element(By.XPATH, "//h1[@class='full-address']").text
            address = address.replace('\n', '')
        except:
            address = ''
        try:
            about_this_home = driver.find_element(By.XPATH, "//p[@class='text-base']/span").text
            new_about = driver.find_elements(By.CSS_SELECTOR, ".keyDetail.font-weight-roman.font-size-base")
            for i in new_about:
                j = i.text
        except:
            about_this_home = ''
        try:
            agent_information = driver.find_element(By.CLASS_NAME,"agent-info-section").text
        except:
            agent_information = ''
        try:
            main_group = driver.find_element(By.CSS_SELECTOR, '.amenities-container')
            heading = [P.text for P in driver.find_elements(By.CSS_SELECTOR, '.super-group-title')]
            sub_group = main_group.find_elements(By.CSS_SELECTOR, '.super-group-content')

            property_details = []
            for j, i in enumerate(sub_group):
                main_heading = heading[j] + ' - '
                group = i.find_elements(By.CSS_SELECTOR, '.amenity-group')

                #     print(group)
                for t in group:
                    a_key = main_heading + t.find_element(By.CSS_SELECTOR, '.title').text
                    a_value = [o.text for o in t.find_elements(By.CSS_SELECTOR, 'li.entryItem')]
                    #     print(a_key,a_value)
                    data_dict = {a_key: a_value}
                    property_details.append(data_dict)
        except:
            property_details = ''

        try:
            about_key = driver.find_elements(By.CSS_SELECTOR, ".header.font-color-gray-light.inline-block")
            about_value = driver.find_elements(By.CSS_SELECTOR, ".content.text-right , .text-right .clickabl")
            Home_facts_and_price_insights = []
            for i, j in zip(about_key, about_value):
                about_table = {i.text: j.text}
                Home_facts_and_price_insights.append(about_table)
        except:
            Home_facts_and_price_insights = ''

        try:
            lat_long = driver.find_element(By.XPATH,
                                           "//div[@class='Section AddressBannerSectionV2 white-bg not-omdp']/script")
            lat1 = lat_long.get_attribute('innerHTML')
            lat2 = json.loads(lat1)
            latitude = lat2['geo']['latitude']
            longitude = lat2['geo']['longitude']
        except:
            latitude = ''
            longitude = ''

        current_url = driver.current_url
        try:
            sale_History_button = driver.find_element(By.XPATH,
                                                      "//span[@class=' bottomLink font-color-link "
                                                      "bottom-link-propertyHistory']").click()
        except:
            pass
        time.sleep(2)
        date_headers = driver.find_elements(By.CLASS_NAME, "timeline-content")
        final_list = []
        l = []
        k = []
        for date_header in date_headers:
            main_date = date_header.find_element(By.TAG_NAME, 'h4')
            k.append(main_date.text)
            key_values = date_header.find_elements(By.CSS_SELECTOR, '.row.PropertyHistoryEventRow')
            l = []
            for key_value in key_values:
                a = key_value.text.replace('\n', '|')
                splitted = a.split('|')
                internal_dict = {}
                for index in range(1, len(splitted), 2):
                    internal_dict[splitted[index]] = splitted[index - 1]
                l.append(internal_dict)

            final_list.append(l)

        temp_dict = {}
        for i, j in zip(k, final_list):
            j = ','.join(map(str, j))
            temp_dict[i] = j

        try:

            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-content='Tax History']"))).click()


            # kona = driver.find_element(By.CSS_SELECTOR, "li[data-content='Tax History']")
            # # b = driver.find_element_by_xpath("//input[starts-with(@class,'gsc')]")
            # driver.execute_script("arguments[0].click();", kona)
        except:
            time.sleep(3)
            # kona = driver.find_element(By.CSS_SELECTOR, "li[data-content='Tax History']")
            # # b = driver.find_element_by_xpath("//input[starts-with(@class,'gsc')]")
            # driver.execute_script("arguments[0].click();", kona)
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Tax History']"))).click()
            # driver.find_element(By.XPATH, "//span[@aria-label='Tax History']").click()

        try:
            tenderInformationTable = driver.find_element(By.CLASS_NAME, "TaxHistoryTable")
            columnList = tenderInformationTable.find_element(By.TAG_NAME, "tr")
            columnList = [i.text.replace('\n=', '').replace('\n+', '') for i in
                          columnList.find_elements(By.TAG_NAME, "th")]
            trTags = tenderInformationTable.find_elements(By.TAG_NAME, "tr")[1:]
            allDataDict = []
            correctList = []
            for trCount in range(len(trTags)):
                valueList = [i.text for i in trTags[trCount].find_elements(By.TAG_NAME, "td")]
                dataDict = dict(zip(columnList, valueList))
                allDataDict.append(dataDict)
        except:
            allDataDict = ''


        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.facts-table')))
        facts_table = driver.find_element(By.CSS_SELECTOR, ".facts-table")
        trTags = facts_table.find_elements(By.CLASS_NAME, "table-row")
        allDataDict1 = []
        for trCount in range(len(trTags)):
            keylist = [i.text for i in trTags[trCount].find_elements(By.CLASS_NAME, "table-label")]
            valueList = [i.text for i in trTags[trCount].find_elements(By.CLASS_NAME, "table-value")]
            dataDict = dict(zip(keylist, valueList))
            allDataDict1.append(dataDict)
        time.sleep(2)

    ###########zoning###########################
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-content='Zoning']")))
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "li[data-content='Zoning']").click()
            table = driver.find_element(By.CSS_SELECTOR, "table[aria-label='Zoning name, type, and code']")
            valuesList = table.find_elements(By.CSS_SELECTOR, 'tr.ZoningRow')
            columnList = [i.find_element(By.TAG_NAME, 'th').text for i in valuesList]
            trTags = [i.find_element(By.TAG_NAME, 'td').text.strip() for i in valuesList]
            zone = dict(zip(columnList, trTags))
        except:
            zone = {}

    #############################################

        # driver.find_element(By.XPATH, "//a[@aria-label='Sale & Tax History']").click()

        # allDataDict

        school_containers = driver.find_elements(By.CLASS_NAME, 'school-card-component')
        try:
            school_list = []

            for school_container in school_containers:
                rating = school_container.find_element(By.CSS_SELECTOR, ".gs-rating-text span").text + '/10'
                school_name = [i.text.replace('\n', '') for i in
                               school_container.find_elements(By.CSS_SELECTOR, ".school-info-box.desktop")]
                students = school_container.find_element(By.CSS_SELECTOR, '.subsection-number').text
                distance1 = school_container.find_elements(By.CSS_SELECTOR, '.subsection-number')
                distance = distance1[1].text
                review = school_container.find_element(By.CSS_SELECTOR,
                                                       '.parent-review-section+ .font-size-smaller').text
                school_Dict = {'school_name': school_name[0], 'distance': distance, 'students': students,
                               'rating': rating,
                               'review': review}
                school_list.append(school_Dict)
        except:
            school_list = ''

        around_this_home = driver.find_elements(By.CSS_SELECTOR, '.percentage .value')
        try:
            Car_depedent = around_this_home[0].text + '/10'
        except:
            Car_depedent = ''
        try:
            Minimal_transit = around_this_home[1].text + '/10'
        except:
            Minimal_transit = ''
        try:
            Somewhat_Bikeable = around_this_home[2].text + '/10'
        except:
            Somewhat_Bikeable = ''
        around_dict = {'Car_depedent': Car_depedent, 'Minimal_transit': Minimal_transit,
                       'Somewhat_Bikeable': Somewhat_Bikeable}
        try:
            About_climate_risk = driver.find_element(By.CSS_SELECTOR, 'p.padding-bottom-medium').text
        except:
            About_climate_risk = ''
        try:
            risk_factors = driver.find_elements(By.CSS_SELECTOR, '#ExpandableCard-expandable-segment p')
            Flood_Factor = risk_factors[0].text
            Fire_Factor = risk_factors[1].text
            Heat_Factor = risk_factors[2].text
            Storm_Risk = risk_factors[3].text
            Drought_Risk = risk_factors[4].text
        except:
            Flood_Factor = ''
            Fire_Factor = ''
            Heat_Factor = ''
            Storm_Risk = ''
            Drought_Risk = ''
        try:
            script_list = driver.find_elements(By.XPATH, '//script')
            for i in script_list:
                try:
                    json_file = i.get_attribute('innerHTML')
                    #         print(json_file)
                    json_data = json.loads(json_file.split('root.__reactServerState.InitialContext = ')[1].split(
                        'root.__reactServerState.Config = ')[0].replace(';', '', -1))
                    new = json.dumps((json_data['ReactServerAgent.cache']['dataCache'][
                                          '/stingray/api/home/details/marketInsightsInfo']['res']['text'].replace('{}&&',
                                                                                                                  '')))
                    new2 = json.loads(new.replace('"{', '{', ).replace('}"', '}').replace('\\', ''))
                    aggregate_data = new2['payload']['housingMarketInfo']['housingMarketGraphs']['metrics'][0][
                        'aggregateData']
                    for i in aggregate_data:
                        i['estimate'] = i.pop('value')
                        del i['yoy']
                    estimates = aggregate_data
                except:
                    estimates = []
        except:
            estimates = []
        about_climate_dict = {'About_climate_risk': About_climate_risk, 'Flood_Factor': Flood_Factor,
                              'Fire_Factor': Fire_Factor, 'Heat_Factor': Heat_Factor, 'Storm_Risk': Storm_Risk,
                              'Drought_Risk': Drought_Risk}

        dataDict = {"Location Url": driver.current_url,"Agent_information":agent_information,'Redfin_Estimates(5Years)':estimates, "address": address, "about_this_home": about_this_home
            , "Home_facts_and_price_insights": Home_facts_and_price_insights,
                    "property_details": property_details, "Sale_History": [temp_dict], "public Facts": allDataDict1,'zoning':zone,
                    "Tax_history": allDataDict,
                    "school": school_list, "around": around_dict,
                    "about climate risk": about_climate_dict, "latitude": latitude, "longitude": longitude}

        dataDf = dataDf.append(dataDict, ignore_index=True)
        with open("redfin_today.csv", 'a', newline='', encoding='utf-8-sig') as f:
            dataDf.to_csv(f, mode='a', header=f.tell() == 0)

