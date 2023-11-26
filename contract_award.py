import pandas as pd
from fake_useragent import UserAgent
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import json, requests
import datetime
import fileLocations
from datetime import datetime
import createNdjsonFile, downloadDocumentFilesUsingSelenium, createS3FilesForHtmlAndMetadat
import time
import re
from lxml import etree
from unidecode import unidecode
import os, codecs


def saveHTML(soup, nog, CATEGORY):
    # get file path to save page
    nog = str(nog).replace("/", "_").replace(" ", "_") + ".html"
    n = os.path.join(fileLocations.CACHE_FOLDER_PATH + CATEGORY, nog)
    # open file in write mode with encoding
    f = codecs.open(n, "w", "utf−8")
    # obtain page source
    h = str(soup)
    # write page source content to file
    f.write(h)
    print("HTML SAVED")
    f.close()
    return


def fake_agent():
    ua = UserAgent()
    print(ua.chrome)
    header = {'User-Agent': str(ua.chrome)}
    return header


def get_pagination():
    res0 = requests.get(
        'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0'
        '%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on'
        '&contractStageList_0=on&contractStageList_1=on&contractStageList_2=on&contractStageList_3=on'
        '&contractStageList=0%2C1%2C2%2C3&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&sortBy'
        '=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false',
        headers=header)
    soup0 = BeautifulSoup(res0.text, 'html.parser')
    pages = soup0.select('.link-text')
    page_count = []
    for page in pages:
        page_count.append(page.text)
    last_page = page_count[-1]
    return last_page


def get_container():
    header = fake_agent()
    print(header)
    # res = requests.get('https://zakupki.gov.ru/epz/order/extendedsearch/results.html', headers=header)
    res = requests.get(f'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94'
                       f'%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on'
                       f'&contractStageList_0=on&contractStageList_1=on&contractStageList_2=on&contractStageList_3=on'
                       f'&contractStageList=0%2C1%2C2%2C3&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D'
                       f'&sortBy=UPDATE_DATE&pageNumber='
                       f'{i}&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false',
                       headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    container = soup.select('.search-registry-entry-block')
    return header, container


def get_soup(detail):
    link = detail.select_one('.registry-entry__header-mid__number a').get_attribute_list('href')[0]
    complete_link = 'https://zakupki.gov.ru' + link
    # # complete_link = 'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html?reestrNumber=2245100011022000111&contractInfoId=77395790'
    # complete_link = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber=3234201335923000003'
    res1 = requests.get(complete_link, headers=header)
    soup = BeautifulSoup(res1.text, 'html.parser')
    return complete_link, soup


def first_tab(CATEGORY, soup1):
    changeDocumentsDetails = ''
    ktrOkpdPosition2 = ''
    procurementType2 = ''
    lotVolume2 = ''
    pricePerUnit2 = ''
    deliveryLocation = ''
    lotNo = ''
    try:
        entityIdAtSource = soup1.find(text='Реестровый номер контракта').next.next.text.strip().replace(' ', '')

    except:
        entityIdAtSource = ''

    try:
        status = soup1.find(text='Статус контракта').next.next.text.strip()
    except:
        status = ''
    try:
        purchasingId = soup1.find(text='Идентификационный код закупки (ИКЗ)').next.next.text.strip()
    except:
        purchasingId = ''
    try:
        itemNumber = soup1.find(text='Уникальный номер позиции плана-графика').next.next.text.strip()
    except:
        itemNumber = ''
    try:
        procurementMethod = soup1.find(
            text='Способ определения поставщика (подрядчика, исполнителя)').next.next.text.strip()
    except:
        try:
            procurementMethod = soup1.find(text='Способ определения поставщика').next.next.text.strip()
        except:
            procurementMethod = ''
    try:
        openDate1 = soup1.find(text='Дата размещения (по местному времени)').next.next.text.strip()
    except:
        openDate1 = ''
    try:
        periodOfExecution = soup1.find(text='Срок исполнения').next.next.text.strip()
    except:
        periodOfExecution = ''
    try:
        theContractIsPlacedInTheRegisterOfContracts = soup1.find(
            text='Размещен контракт в реестре контрактов').next.next.text.strip()
    except:
        theContractIsPlacedInTheRegisterOfContracts = ''

    try:
        updatedContractInTheRegisterOfContracts = soup1.find(
            text='Обновлен контракт в реестре контрактов').next.next.text.strip()
    except:
        updatedContractInTheRegisterOfContracts = ''
    try:
        groundsForAgreement = soup1.find(
            text='Основание заключения контракта с единственным поставщиком').next.next.text.strip()
    except:
        groundsForAgreement = ''
    try:
        bankingInfo = soup1.find(
            text='Информация о банковском и (или) казначейском сопровождении контракта').next.next.text.strip()
    except:
        bankingInfo = ''
    try:
        changeReason = soup1.find(text='Причина изменения условий контракта').next.next.text.strip()
    except:
        changeReason = ''
    try:
        for index in range(len(soup1.find_all('span', 'section__title'))):
            if soup1.find_all('span', 'section__title')[index].text.strip().replace('\n', '').replace('  ',
                                                                                                      '') == 'Реквизиты документа, являющегося основаниемизменения условий контракта':
                changeDocumentsDetails = soup1.find_all('span', 'section__title')[
                    index].next.next.next.text.strip().replace('\n', '').replace(' ', '')
        # changeDocumentsDetails = soup1.find(
        #     text='Реквизиты документа, являющегося основанием изменения условий контракта').next.next.text.strip()
    except:
        changeDocumentsDetails = ''
    try:
        buyerName = soup1.find(text='Полное наименование заказчика').next.next.text.strip()
    except:
        buyerName = ''
    try:
        buyerNameAbbreviated = soup1.find(text='Сокращенное наименование заказчика').next.next.text.strip()
    except:
        buyerNameAbbreviated = ''
    try:
        customerId = soup1.find(text='Идентификационный код заказчика').next.next.text.strip()
    except:
        customerId = ''
    try:
        buyerTin = soup1.find(text='ИНН').next.next.text.strip()
    except:
        buyerTin = ''
    try:
        buyerCheckpoint = soup1.find(text='КПП').next.next.text.strip()
    except:
        buyerCheckpoint = ''
    try:
        buyerFormCode = soup1.find(text='Код организационно-правовой формы').next.next.text.strip()
    except:
        buyerFormCode = ''
    try:
        buyerOkpoCode = soup1.find(text='Код ОКПО').next.next.text.strip()
    except:
        buyerOkpoCode = ''
    try:
        buyerMunicipalityCode = soup1.find(text='Код территории муниципального образования').next.next.text.strip()
    except:
        buyerMunicipalityCode = ''
    try:
        buyerBudgetName = soup1.find(text='Наименование бюджета').next.next.text.strip()
    except:
        buyerBudgetName = ''
    try:
        buyerBudgetLevel = soup1.find(text='Уровень бюджета').next.next.text.strip()
        buyerBudgetLevel = buyerBudgetLevel.replace('\xa0', '')

    except:
        buyerBudgetLevel = ''
    try:
        contractConclusionDate = soup1.find(text='Дата заключения контракта').next.next.text.strip()
    except:
        contractConclusionDate = ''
    try:
        contractId = soup1.find(text='Номер контракта').next.next.text.strip()
    except:
        contractId = ''
    try:
        title = soup1.find(text='Предмет контракта').next.next.text.strip()
    except:
        title = ''
    try:
        shortDescription = title
    except:
        shortDescription = ''
    try:
        totalContractNoVat = soup1.find(text='Цена контракта').next.next.text.strip()
        totalContractNoVat = totalContractNoVat.replace('\xa0', '')
    except:
        totalContractNoVat = ''
    try:
        totalContractValue = soup1.find(text='В том числе НДС').next.next.text.strip()
    except:
        totalContractValue = ''
    try:
        contractValueCurrency = soup1.find(text='Валюта контракта').next.next.text.strip()
    except:
        contractValueCurrency = ''
    try:
        openDate = soup1.find(text='Дата начала исполнения контракта').next.next.text.strip()
    except:
        openDate = ''
    try:
        closeDate = soup1.find(text='Дата окончания исполнения контракта').next.next.text.strip().replace(' ', '')
    except:
        closeDate = ''
    try:
        stageId = soup1.find(text='Идентификатор этапа контракта').next.next.text.strip()
    except:
        stageId = ''
    try:
        advancePayment = soup1.find(text='Размер аванса').next.next.text.strip()
        advancePayment = advancePayment.replace('\xa0', '').replace('\n', '')
    except:
        advancePayment = ''
    try:
        for index1 in range(len(soup1.find_all('span', 'section__title'))):
            if soup1.find_all('span', 'section__title')[
                index1].text.strip() == 'Место поставки товара, выполнения работы или оказания услуги':
                deliveryLocation = soup1.find_all('span', 'section__title')[index1].next.next.next.text.strip()
    except:
        deliveryLocation = ''
    try:
        supplierName = soup1.select_one('.tableBlock__col_first.text-break').text.strip().split('\n')[0].replace("'",
                                                                                                                 '`').replace(
            '"', '`')
    except:
        supplierName = ''
    try:
        supplierTin = soup1.select_one('.section .grey-main-light+ span').text
    except:
        supplierTin = ''
    try:
        supplierCheckpoint = soup1.select_one('.blockInfo__section+ section .grey-main-light+ span').text
    except:
        supplierCheckpoint = ''
    try:
        supplierCountryCode = soup1.select_one('.text-break+ .tableBlock__col').text.strip()
    except:
        supplierCountryCode = ''
    try:
        supplierAddress = soup1.select_one('.tableBlock__body .tableBlock__col:nth-child(3)').text.strip()
    except:
        supplierAddress = ''

    try:
        if soup1.find_all(text='Почтовый адрес'):
            supplierEmailTelephone = soup1.select_one(
                '.tableBlock__body .tableBlock__col:nth-child(5)').text.strip().replace('\n', '').replace('   ', '')
        else:
            supplierEmailTelephone = soup1.select_one(
                '.tableBlock__body .tableBlock__col:nth-child(4)').text.strip().replace('\n', '').replace('   ', '')
    except:
        supplierEmailTelephone = ''
    try:
        new_documents = soup1.select_one('.mb-2:nth-child(6) a').get_attribute_list('href')[0]
        header = fake_agent()
        new_link = 'https://zakupki.gov.ru' + new_documents
        res_99 = requests.get(new_link, headers=header)
        soup_99 = BeautifulSoup(res_99.text, 'html.parser')
        links = soup_99.select('.margRight5 a')
        final_list2 = []
        for link in links:
            href = link.get_attribute_list('href')[0]
            name = link.text
            type = 'file'
            dict1 = {'name': name, 'file': href, 'type': type}
            final_list2.append(dict1)
    except:
        final_list2 = []

    return final_list2, bankingInfo, changeReason, changeDocumentsDetails, ktrOkpdPosition2, procurementType2, \
        lotVolume2, pricePerUnit2, deliveryLocation, entityIdAtSource, status, \
        purchasingId, itemNumber, procurementMethod, openDate1, groundsForAgreement, buyerName, buyerNameAbbreviated, \
        customerId, buyerTin, buyerCheckpoint, buyerFormCode, buyerOkpoCode, buyerMunicipalityCode, buyerBudgetName, \
        buyerBudgetLevel, contractConclusionDate, contractId, title, totalContractNoVat, totalContractValue, \
        contractValueCurrency, openDate, closeDate, stageId, advancePayment, supplierName, supplierTin, \
        supplierCheckpoint, supplierCountryCode, supplierAddress, supplierEmailTelephone, shortDescription, periodOfExecution, theContractIsPlacedInTheRegisterOfContracts, updatedContractInTheRegisterOfContracts


lots = []


def second_tab(next_tab):
    driver = webdriver.Chrome()
    driver.get('https://zakupki.gov.ru' + next_tab)
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '.btn-close.closePopUp').click()
    columnsList = ["lotTitle", "ktrOkpdPosition", "procurementType", "lotVolume", "pricePerUnit", "totalLotVlaue"]
    allTdList = []
    for i in range(0, 9999):
        soup00 = BeautifulSoup(driver.page_source, 'html.parser')
        saveHTML(soup00, entityIdAtSource + '_' + str(i + 1), CATEGORY)
        # htmlfiles = entityIdAtSource + '_' + str(i + 1)
        trTags = driver.find_elements(By.XPATH,
                                      '//table[@id = "contract_subjects"]/tbody[@class = "tableBlock__body"]/tr['
                                      '@class="tableBlock__row "]')
        for trCount in range(len(trTags)):
            tdTags = [i.text.replace('\n', '').replace("'", '`').replace('"', '`') for i in
                      trTags[trCount].find_elements(By.TAG_NAME, "td")[1:]]
            allTdList.append(tdTags)
        try:
            driver.find_element(By.CSS_SELECTOR, '.next').click()
            time.sleep(3)
        except:
            break

    lotDf = pd.DataFrame(allTdList, columns=columnsList)
    lotDf['lotTitle'] = lotDf['lotTitle'].str.split('.', n=1, expand=True)[1]
    lotDf['lotTitle'] = lotDf['lotTitle'].str.replace('Страна происхождения: РОССИЯ (643)', '')
    print(lotDf['lotTitle'])
    lotDf['lotTitle'] = lotDf['lotTitle'].str.strip()

    lotDf['lotNumber'] = range(1, 1 + len(lotDf))
    lotDf = lotDf[
        ['lotNumber', 'lotTitle', 'totalLotVlaue', 'ktrOkpdPosition', 'procurementType', 'lotVolume', 'pricePerUnit']]
    lots = lotDf.to_dict(orient="records")
    return lots


# lots = second_tab()


def third_tab(final_list2):
    final_list = []

    try:
        links = soup3.select('.section__value a')
        for link in links:
            href = link.get_attribute_list('href')[0]
            name = link.text
            name = name.replace('\n', '').replace(' ', '').strip()
            type = 'file'
            temp_dict = {'name': name, 'file': href, 'type': type}
            final_list.append(temp_dict)

        # types = soup3.select('img.vAlignMiddle')
        # href = []
        # name = []
        # type1 = []
        # # final_list = []
        # for link in links:
        #     a = link.get_attribute_list('href')[0]
        #     href.append(a)
        #     b = link.get_attribute_list('title')[0]
        #     try:
        #         b = b.split('(')[0]
        #     except:
        #         b = b
        #
        #     b = b.replace('\n', '')
        #     name.append(b)
        # for type in types:
        #     c = type.get_attribute_list('alt')[0]
        #     if c:
        #         type1.append('file')
        #     # type1.append(c)
        #     else:
        #         type1.append('page')
        # for name, type, file in zip(name, type1, href):
        #     tempdict = {'name': str(name).strip(), 'file': file, 'type': type, }
        #     final_list.append(tempdict)

    except:
        pass
    final_list.extend(final_list2)
    return final_list


def store_in_csv(data, df_columns, CATEGORY):
    df = pd.DataFrame(data=data, columns=df_columns)
    with open(fileLocations.CSV_FOLDER_PATH + CATEGORY + "/" + CATEGORY + ".csv", 'a', newline='',
              encoding='utf-8') as f:
        df.to_csv(f, mode='a', header=f.tell() == 0)


if __name__ == '__main__':
    header = fake_agent()
    todaysDate = str(datetime.now().date()).replace("-", "/")
    noticeType = "award"
    CATEGORY = "zakupki_" + noticeType
    [fileLocations.createFolder(parent_dir, CATEGORY) for parent_dir in fileLocations.createFolderList]
    last_page = get_pagination()
    print(last_page)
    count = 1
    # for i in range(count, int(last_page) + 1):
    for i in range(count, 2):
        count += i - 1
        print(count)
        print('page no: ', i)
        header, container = get_container()
        for detail in container[:2]:
            complete_link, soup1 = get_soup(detail)
            final_list2,bankingInfo, changeReason, changeDocumentsDetails, ktrOkpdPosition2, procurementType2, \
                lotVolume2, pricePerUnit2, deliveryLocation, entityIdAtSource, status, \
                purchasingId, itemNumber, procurementMethod, openDate1, groundsForAgreement, buyerName, buyerNameAbbreviated, \
                customerId, buyerTin, buyerCheckpoint, buyerFormCode, buyerOkpoCode, buyerMunicipalityCode, buyerBudgetName, \
                buyerBudgetLevel, contractConclusionDate, contractId, title, totalContractNoVat, totalContractValue, \
                contractValueCurrency, openDate, closeDate, stageId, advancePayment, supplierName, supplierTin, \
                supplierCheckpoint, supplierCountryCode, supplierAddress, supplierEmailTelephone, shortDescription, periodOfExecution, theContractIsPlacedInTheRegisterOfContracts, updatedContractInTheRegisterOfContracts = first_tab(
                CATEGORY, soup1)

            try:
                for i in range(len(soup1.find_all('a', "tabsNav__item"))):
                    if soup1.find_all('a', "tabsNav__item")[i].text.strip() == 'Платежи и объекты закупки' or \
                            soup1.find_all('a', "tabsNav__item")[i].text.strip() == 'ПЛАТЕЖИ И ОБЪЕКТЫ ЗАКУПКИ':
                        next_tab = soup1.find_all('a', "tabsNav__item")[i].attrs['href']
                        res2 = requests.get('https://zakupki.gov.ru' + next_tab, headers=header)
                        soup2 = BeautifulSoup(res2.text, 'html.parser')
                        lots = second_tab(next_tab)
            except:
                pass

            try:
                for i in range(len(soup1.find_all('a', "tabsNav__item"))):
                    if soup1.find_all('a', "tabsNav__item")[i].text.strip() == 'ВЛОЖЕНИЯ' or \
                            soup1.find_all('a', "tabsNav__item")[i].text.strip() == 'Вложения':
                        next_tab1 = soup1.find_all('a', "tabsNav__item")[i].attrs['href']
                        res3 = requests.get('https://zakupki.gov.ru' + next_tab1, headers=header)
                        soup3 = BeautifulSoup(res3.text, 'html.parser')
                        final_list = third_tab(final_list2)
            except:
                pass
            other_value = {
                'openDate1': openDate1,
                'purchasingId': purchasingId.replace('\xa0', ''), 'itemNumber': itemNumber.replace('\xa0', ''),
                'procurementMethod': procurementMethod.replace('\xa0', ''),
                'groundsForAgreement': groundsForAgreement.replace('\xa0', ''),
                'supplierName': supplierName.replace('\xa0', '').replace('\n', ''),
                'supplierCheckpoint': supplierCheckpoint.replace('\xa0', '').replace('\n', ''),
                'supplierTin': supplierTin.replace('\xa0', '').replace('\n', ''),
                'supplierAddress': supplierAddress.replace('\xa0', '').replace('\n', '').replace("'", '`').replace(
                    '"', '`'),
                'contractStartDate': openDate,
                'contractEndDate': closeDate.split(' ')[0],
                'supplierCountryCode': supplierCountryCode.replace('\xa0', '').replace('\n', '').replace(' ', ''),
                'supplierEmailTelephone': supplierEmailTelephone.replace('\xa0', '').replace('\n', ''),
                'bankingInfo': bankingInfo, 'changeReason': changeReason.replace('\xa0', ''),
                'changeDocumentsDetails': changeDocumentsDetails.replace('\xa0', '').replace("'", '`').replace('"',
                                                                                                               '`'),
                'buyerNameAbbreviated': buyerNameAbbreviated.replace('\xa0', '').replace("'", '`').replace('"', '`'),
                'periodOfExecution': periodOfExecution,
                'theContractIsPlacedInTheRegisterOfContracts': theContractIsPlacedInTheRegisterOfContracts,
                'updatedContractInTheRegisterOfContracts': updatedContractInTheRegisterOfContracts,
                'customerId': customerId.replace('\xa0', ''), 'buyerTin': buyerTin.replace('\xa0', ''),
                'buyerCheckpoint': buyerCheckpoint.replace('\xa0', '').replace("'", '`').replace('"', '`'),
                'buyerFormCode': buyerFormCode.replace('\xa0', ''),
                'buyerOkpoCode': buyerOkpoCode.replace('\xa0', '').replace("'", '`').replace('"', '`'),
                'buyerMunicipalityCode': buyerMunicipalityCode.replace('\xa0', '').replace("'", '`').replace('"', '`'),
                'buyerBudgetName': buyerBudgetName.replace('\xa0', '').replace("'", '`').replace('"', '`'),
                'buyerBudgetLevel': buyerBudgetLevel.replace('\xa0', '').replace("'", '`').replace('"', '`'),
                'contractConclusionDate': contractConclusionDate.replace("'", '`').replace('"', '`'),
                'contractId': contractId.replace('\xa0', '').replace('\n', '').replace("'", '`').replace('"', '`'),
                'totalContractNoVat': totalContractNoVat.replace('\xa0', '').replace("'", '`').replace('"', '`'),
                'stageId': stageId.replace("'", '`').replace('"', '`'),
                'advancePayment': advancePayment.replace('\n', '').replace('\xa0', '').replace(' ', ''),
                'deliveryLocation': deliveryLocation.replace('\xa0', '').replace('\n', '').replace("'", '`').replace(
                    '"', '`')
            }
            open_date_a = ''
            open_date_b = ''
            temp_list = [[complete_link, entityIdAtSource, status, buyerName, title, totalContractValue,
                          contractValueCurrency, open_date_a, open_date_b, shortDescription,
                          supplierName, other_value, final_list, lots]]
            columns = ['originalUrl', 'entityIdAtSource', 'status', 'buyerName', 'title',
                       'totalContractValue',
                       'contractValueCurrency', 'openDate', 'closeDate', 'shortDescription', 'supplierName',
                       'otherValues', 'documentLinks','lots']
            store_in_csv(temp_list, columns, CATEGORY)
            print('done!')
    downloadDocumentUrls = createNdjsonFile.CreateNDJSONFileandReturnDownloadUrls(CATEGORY)
    createS3FilesForHtmlAndMetadat.createS3Files(todaysDate, CATEGORY)
    downloadDocumentFilesUsingSelenium.downloadFiles(CATEGORY, downloadDocumentUrls, todaysDate, entityIdAtSource)
