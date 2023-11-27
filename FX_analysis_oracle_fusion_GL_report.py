import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import time
import os
import warnings
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys


def my_work():
    global user_name, password, max_rows
    # prompt the user to select the download directory
    warnings.filterwarnings("ignore")
    my_canvas.itemconfigure(status_now, text="Waiting for directory to select", font=("Verdana", 10))
    start = time.time()
    messagebox.showinfo("Select directory", "Please select the directory to save all the files")
    selected_directory = filedialog.askdirectory()
    # print(selected_directory)
    selected_directory = os.path.abspath(selected_directory)
    messagebox.showinfo("Select directory", "Please select the directory of the chrome driver")
    chromedriver_path = filedialog.askdirectory()
    chromedriver_path = chromedriver_path+'/chromedriver.exe'
    service = Service(chromedriver_path)
    option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    prefs = {"download.default_directory": selected_directory}
    my_canvas.itemconfigure(status_now, text="Directory Selected. Waiting for the user to select the input file", font=("Verdana", 8))
    option.add_experimental_option("prefs", prefs)
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    # # start the ChromeDriver with the specified options
    driver = webdriver.Chrome(service=service, options=option)
    driver.get("https://ecjm.fa.us2.oraclecloud.com/")
    driver.maximize_window()
    user_name = A_entry.get()
    password = B_entry.get()
    # enter username
    username_element = driver.find_element(By.ID, 'userid')
    username_element.send_keys(user_name)
    time.sleep(2)

    # enter password
    password_element = driver.find_element(By.ID, 'password')
    password_element.send_keys(password)
    time.sleep(2)

    # logging into oracle page
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnActive"]'))).click()
    time.sleep(5)

    # going to oracle homepage
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:commandLink1"]'))).click()
    time.sleep(5)

    # clicking on tools
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="groupNode_tools"]'))).click()
    time.sleep(5)
    warnings.simplefilter(action='ignore', category=FutureWarning)
    messagebox.showinfo("Select Files", "Please select the required input files")
    file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
    columns_with_leading_zeros = ['Period', 'LE FROM', 'LE TO', 'BU FROM', 'BU TO', 'LOC FROM', 'LOC TO',
                                  'CC FROM', 'CC TO', 'Acct From', 'Acct To', 'IC FROM', 'IC TO',
                                  'Res From', 'Res To']
    columns_with_leading_zeros_1 = ['CC', 'LE', 'LOC', 'BU', 'Acct', 'IC', 'Res']
    if 'GLR Report' in file_path:
        df = pd.read_excel(file_path, dtype={col: str for col in columns_with_leading_zeros})
        subset_cols = df.columns
        df = df.drop_duplicates(subset=subset_cols, keep='last')
        max_rows = len(df)
        my_canvas.itemconfigure(status_now, text="Input Selected: GLR Report. Waiting for the browser to download the files", font=("Verdana", 7))
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="itemNode_tools_reports_and_analytics_0"]'))).click()
        time.sleep(10)
        for index, rows in df.iterrows():
            period = rows[0]
            le_from = str(rows[1])
            le_to = str(rows[2])
            bu_from = str(rows[3])
            bu_to = str(rows[4])
            loc_from = str(rows[5])
            loc_to = str(rows[6])
            cc_from = str(rows[7])
            cc_to = str(rows[8])
            acct_from = str(rows[9])
            acct_to = str(rows[10])
            ic_from = str(rows[11])
            ic_to = str(rows[12])
            res_from = str(rows[13])
            res_to = str(rows[14])
            # if le_from or le_to == '':
            file_name = 'GLR001 - ' + le_from + '.' + le_to + '.' + bu_from + '.' + bu_to + '.' + loc_from + '.' + loc_to + '.' + cc_from + '.' + cc_to + '.' + acct_from + '.' + acct_to + '.' + ic_from + '.' + ic_to + '.' + \
                        res_from + '.' + res_to + '-' + period + '.xlsx'
            file_name = file_name.replace('nan.', '').strip()
            print(file_name)
            progress_bar_status = str(index+1)+'/'+str(max_rows)
            driver.get(
                'https://ecjm.fa.us2.oraclecloud.com/analytics/saw.dll?bipublisherEntry&Action=open&itemType=.xdo&bipPath=%2FCustom%2FReports%2FGL%20Reports%2FGL-R-001%20JE%20at%20Line%20Level%20Report.xdo&path=%2Fshared%2FCustom%2FReports%2FGL%20Reports%2FGL-R-001%20JE%20at%20Line%20Level%20Report.xdo')
            time.sleep(10)
            # all the required elements are in iframe. so, we need to switch the content to iframe
            inside_iframe = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ContentIFrame')))
            driver.switch_to.frame(inside_iframe)
            time.sleep(5)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="xdo:_paramsp_period_div"]/a/span'))).click()
            time.sleep(3)
            # passing all the input's
            input_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//input[@value='{period}']")))
            # input_element = driver.find_element(By.XPATH, f"//input[@value='{period}']")
            input_element.click()
            time.sleep(5)
            if le_from != 'nan':
                legal_entity_from = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT1"]')
                legal_entity_from.clear()
                legal_entity_from.send_keys(le_from)
                time.sleep(2)
                legal_entity_to = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT1_TO"]')
                legal_entity_to.clear()
                legal_entity_to.send_keys(le_to)
                time.sleep(2)
            if bu_from != 'nan':
                banner_unit_from = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT2"]')
                banner_unit_from.clear()
                banner_unit_from.send_keys(bu_from)
                time.sleep(2)
                banner_unit_to = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT2_TO"]')
                banner_unit_to.clear()
                banner_unit_to.send_keys(bu_to)
                time.sleep(2)
            if loc_from != 'nan':
                location_from = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT3"]')
                location_from.clear()
                location_from.send_keys(loc_from)
                time.sleep(2)
                location_to = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT3_TO"]')
                location_to.clear()
                location_to.send_keys(loc_to)
                time.sleep(2)
            if cc_from != 'nan':
                cost_center_from = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT4"]')
                cost_center_from.clear()
                cost_center_from.send_keys(cc_from)
                time.sleep(2)
                cost_center_to = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT4_TO"]')
                cost_center_to.clear()
                cost_center_to.send_keys(cc_to)
                time.sleep(2)
            if acct_from != 'nan':
                account_from = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT5"]')
                account_from.clear()
                account_from.send_keys(acct_from)
                time.sleep(2)
                account_to = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT5_TO"]')
                account_to.clear()
                account_to.send_keys(acct_to)
                time.sleep(2)
            if ic_from != 'nan':
                inter_company_from = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT6"]')
                inter_company_from.clear()
                inter_company_from.send_keys(ic_from)
                time.sleep(2)
                inter_company_to = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT6_TO"]')
                inter_company_to.clear()
                inter_company_to.send_keys(ic_to)
                time.sleep(2)
            if res_from != 'nan':
                reserved_from = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT7"]')
                reserved_from.clear()
                reserved_from.send_keys(res_from)
                time.sleep(2)
                reserved_to = driver.find_element(By.XPATH, '//*[@id="_paramsSEGMENT7_TO"]')
                reserved_to.clear()
                reserved_to.send_keys(res_to)
                time.sleep(2)
            # clicking on the apply button after sending all the values
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reportViewApply"]'))).click()
            my_canvas.itemconfigure(status_now, text=f"Files are downloading...({progress_bar_status})", font=("Verdana", 10))
            time.sleep(30)
            driver.switch_to.default_content()
            original_file = os.path.join(selected_directory, 'GL-R-001 JE at Line Level Report_XXHBC GL-R-001 XSL Template.xlsx')
            new_file_name = os.path.join(selected_directory, file_name)
            os.rename(original_file, new_file_name)
            val_to_update = 1
            update_p_b(val_to_update)
            time.sleep(0.01)
        my_canvas.itemconfigure(status_now, text="GLR Reports have downloaded successfully", font=("Verdana", 10))
        driver.quit()
        time.sleep(2)
        root.quit()
        sys.exit()
    elif 'General Ledger Report' in file_path:
        df = pd.read_excel(file_path, dtype={col: str for col in columns_with_leading_zeros_1})
        subset_cols = df.columns
        df = df.drop_duplicates(subset=subset_cols, keep='last')
        max_rows = len(df)
        my_canvas.itemconfigure(status_now, text="Input Selected: General Ledger Report. Waiting for the browser to download the files", font=("Verdana", 6))
        # clicking on scheduled process
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="itemNode_tools_scheduled_processes_fuse_plus_0"]'))).click()
        time.sleep(10)
        for index, row in df.iterrows():
            from_accounting = row[0]
            to_accounting = row[1]
            le = row[2]
            bu = row[3]
            loc = row[4]
            cc = row[5]
            acct = row[6]
            ic = row[7]
            res = row[8]
            file_name = 'General Ledger Account Details Report - ' + le + '.' + bu + '.' + loc + '.' + cc + '.' + acct + '.' + ic + '.' + res + '-' + from_accounting + '.xlsx'
            # progress_bar_status = ((index + 1) / max_rows) * 100
            progress_bar_status = str(index+1)+'/'+str(max_rows)
            # clicking on Schedule new process
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:panel:scheduleProcess"]/a'))).click()
            time.sleep(5)
            # my_canvas.itemconfigure(status_now, text="Directory Selected. Waiting for browser to download the files", font=("Verdana", 10))
            name = 'General Ledger Account Details Report'
            name_element = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:selectOneChoice2::content"]')
            name_element.clear()
            name_element.send_keys(name)
            name_element.send_keys(Keys.ENTER)
            time.sleep(5)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:snpokbtnid"]'))).click()
            time.sleep(5)
            from_accounting_period = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:aTTRIBUTE6Id::content"]')
            from_accounting_period.clear()
            from_accounting_period.send_keys(from_accounting)
            time.sleep(2)
            to_accounting_period = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:aTTRIBUTE7Id::content"]')
            to_accounting_period.clear()
            to_accounting_period.send_keys(to_accounting)
            time.sleep(2)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:kff1_ACKFF_KFFButconImage1"]'))).click()
            time.sleep(2)
            # adding filed for Account
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFields"]/table/tbody/tr/td[1]/a/span'))).click()
            time.sleep(2)
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFieldsIter:0:adFldMenuItem"]/td[2]'))).click()
            time.sleep(2)
            # adding field for Business Unit
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFields"]/table/tbody/tr/td[1]/a/span'))).click()
            time.sleep(2)
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFieldsIter:1:adFldMenuItem"]/td[2]'))).click()
            time.sleep(2)
            # adding filed for Cost Center
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFields"]/table/tbody/tr/td[1]/a/span'))).click()
            time.sleep(2)
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFieldsIter:2:adFldMenuItem"]/td[2]'))).click()
            time.sleep(2)
            # adding filed for Inter company
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFields"]/table/tbody/tr/td[1]/a/span'))).click()
            time.sleep(2)
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFieldsIter:3:adFldMenuItem"]/td[2]'))).click()
            time.sleep(2)
            # # adding field for Legal Entity
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFields"]/table/tbody/tr/td[1]/a/span'))).click()
            time.sleep(2)
            WebDriverWait(driver, 60).until(
                (EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFieldsIter:4:adFldMenuItem"]/td[2]')))).click()
            time.sleep(2)
            # adding field for location
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFields"]/table/tbody/tr/td[1]/a/span'))).click()
            time.sleep(2)
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFieldsIter:5:adFldMenuItem"]/td[2]'))).click()
            time.sleep(2)
            # adding field for reserved
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFields"]/table/tbody/tr/td[1]/a/span'))).click()
            time.sleep(2)
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:addFieldsIter:6:adFldMenuItem"]/td[2]'))).click()
            time.sleep(2)
            # passing the values to the fields
            legal_entity = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:value00::content"]')
            legal_entity.send_keys(le)
            time.sleep(2)
            business_unit = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:value10::content"]')
            business_unit.send_keys(bu)
            time.sleep(2)
            location = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:value20::content"]')
            location.send_keys(loc)
            time.sleep(2)
            cost_center = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:value30::content"]')
            cost_center.send_keys(cc)
            time.sleep(2)
            account = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:value40::content"]')
            account.send_keys(acct)
            time.sleep(2)
            inter_company = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:value50::content"]')
            inter_company.send_keys(ic)
            time.sleep(2)
            reserved = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:KFFFILTERFilterCriteria:value60::content"]')
            reserved.send_keys(res)
            time.sleep(2)
            # clicking OK button after filling all the fields
            ok_button = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:kff1_kffSearchDialog::_fcc"]').find_element(By.CLASS_NAME, "x1a")
            ok_button.click()
            time.sleep(5)
            # WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:basicReqBody:dynam1:0:j_id83"]'))).click()
            # time.sleep(5)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:requestBtns:submitButton"]'))).click()
            time.sleep(5)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:r1:0:r1:requestBtns:confirmationPopup:confirmSubmitDialog::ok"]'))).click()
            time.sleep(5)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:panel:processRefreshId"]/a'))).click()
            time.sleep(5)
            while True:
                refresh_button = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:panel:result::db"]/table/tbody/tr[1]/td[2]/div/table/tbody/tr/td[3]/span').text
                # refresh_button = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:panel:result::db"]/table/tbody/tr[1]/td[2]/div/table/tbody/tr/td[3]/span').text
                if refresh_button == 'Running':
                    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:panel:processRefreshId"]/a'))).click()
                    time.sleep(3)
                else:
                    break
            buttons = driver.find_elements(By.CLASS_NAME, 'xen')
            buttons[0].click()
            time.sleep(5)
            # republished = driver.getText()
            inside_iframe = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt1:processDetails:processDetails:r61:0:if1')))
            driver.switch_to.frame(inside_iframe)
            time.sleep(5)
            republish_id = driver.find_element(By.CLASS_NAME, 'icon_cell').find_element(By.TAG_NAME, 'img').get_attribute('onclick')
            republish_id = republish_id.split("('")[1].replace("');", '').strip()
            republish_url = 'https://ecjm.fa.us2.oraclecloud.com' + republish_id
            # print(republish_url)
            driver.switch_to.default_content()
            # driver.execute_script(f"window.open({republish_url}, '_blank');")
            # driver.get(republish_url)
            driver.execute_script("window.open('', '_blank');")
            # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))
            driver.switch_to.window(driver.window_handles[1])
            driver.get(republish_url)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reportViewMenu"]'))).click()
            time.sleep(5)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'floatMenuSubMenuAdjust'))).click()
            time.sleep(5)
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="_xdoFMenu01"]/div/div/ul/li[7]/div/a'))).click()
            my_canvas.itemconfigure(status_now, text=f"Files are downloading...({progress_bar_status})", font=("Verdana", 10))
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[2])
            while True:
                load_button = driver.find_element(By.XPATH, '//*[@id="message"]').text
                if load_button == 'Loading':
                    WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="message"]'), 'Report Completed'))
                    time.sleep(3)
                else:
                    break
            driver.close()
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            warnings.simplefilter(action='ignore', category=FutureWarning)
            original_file = os.path.join(selected_directory, 'GeneralLedger_General Ledger Report.xlsx')
            new_file_name = os.path.join(selected_directory, file_name)
            os.rename(original_file, new_file_name)
            val_to_update = 1
            update_p_b(val_to_update)
            time.sleep(0.01)
        my_canvas.itemconfigure(status_now, text="General Ledger Account Details Reports have downloaded successfully", font=("Verdana", 10))
        driver.quit()
        time.sleep(2)
        # my_canvas.itemconfigure(status_now, text="Status: Files are downloaded", font=("Verdana", 10))
        root.quit()
        sys.exit()


def close_window():  # optional! I use it clear my remnant data
    root.quit()
    sys.exit(1)


def update_p_b(progress):
    global inv_progress, add_them_here, max_rows
    add_them_here += progress
    inv_progress['value'] = (add_them_here / max_rows) * 100
    root.update_idletasks()


def get_greeting():
    current_time_g = time.localtime()
    hour = current_time_g.tm_hour
    if 6 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def login_page():
    my_canvas.itemconfigure(greeting, text="")
    next_button.destroy()
    my_canvas.create_text(180, 200, text="USER NAME")
    my_canvas.create_text(180, 250, text="PASSWORD")

    global A_entry
    A_entry = tk.Entry(root, width=30)
    # my_canvas.create_window(320, 200, window=username_entry)
    my_canvas.create_window(320, 200, window=A_entry)

    global B_entry
    B_entry = tk.Entry(root, show='*', width=30)
    # my_canvas.create_window(320, 250, window=password_entry)
    my_canvas.create_window(320, 250, window=B_entry)

    global login_button
    login_button = tk.Button(root, text="Login", command=lambda: threading.
                             Thread(target=my_work).start())
    my_canvas.create_window(275, 300, window=login_button)
    my_canvas.itemconfigure(status_now, text="Waiting for login and password", font=("Verdana", 10))

    global inv_progress
    inv_progress = ttk.Progressbar(root, orient=tk.HORIZONTAL,
                                   length=565, mode="determinate")
    my_canvas.create_window(10, 390, window=inv_progress, anchor='sw')

    global close_button
    close_button = tk.Button(root, text="Close", command=close_window)
    my_canvas.create_window(530, 30, window=close_button)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    inv_progress = ""
    current_version = ""
    A_entry = ""
    B_entry = ""
    login_button = ""
    close_button = ""
    user_name = ""
    password = ""
    max_rows = 0
    add_them_here = 0
    # Initialize progress variables
    root = tk.Tk()
    root.title("Showcase")
    script_file_path_logo = os.path.abspath(__file__)
    current_directory_logo = os.path.dirname(script_file_path_logo)
    current_file_logo = "Logo"
    current_logo_name = "HB_BG.png"
    current_bg_name = os.path.join(current_directory_logo, current_file_logo, "HB_BG.png")
    bg_image = PhotoImage(file=current_bg_name)
    file_path_logo = os.path.join(current_directory_logo, current_file_logo, current_logo_name)
    print(file_path_logo)
    root.iconbitmap(file_path_logo)
    my_canvas = Canvas(root, width=580, height=400, )
    my_canvas.pack(fill="both", expand=True)
    my_canvas.create_image(285, 60, image=bg_image, anchor='n')
    banner_path = os.path.join(current_directory_logo, current_file_logo, "Banner.png")
    banner = tk.PhotoImage(file=banner_path)
    my_canvas.create_image(290, 10, image=banner, anchor="n")
    close_button1 = tk.Button(root, text="Close", command=close_window)
    my_canvas.create_window(530, 30, window=close_button1)
    greeting = my_canvas.create_text(300, 345, text=get_greeting(), font=("Verdana", 20))
    status_now = my_canvas.create_text(275, 350, text="", font=("Verdana", 10))
    # Create a button to go to the next page
    next_button = tk.Button(root, text="Let's begin", command=login_page)
    my_canvas.create_window(290, 380, window=next_button)
    root.mainloop()
