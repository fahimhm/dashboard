# module/library
import os
import time
import datetime as dt
from os.path import join
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

def set_dataset(url, aList):
    # delete old file
    for name in aList:
        if os.path.isfile(join(os.getcwd(), 'datasets', name + '.csv')):
            os.remove(join(os.getcwd(), 'datasets', name + '.csv'))

    # driver setting
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2) # not to choose default download setting directory
    fp.set_preference("browser.download.manager.ShowWhenStarting", False)
    fp.set_preference("browser.download.dir", join(os.getcwd(), 'datasets'))
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # get the url and navigating
    driver = webdriver.Firefox(executable_path = join(os.getcwd(), 'driver', 'geckodriver.exe'), firefox_profile = fp)
    for name in aList:
        driver.get(url)
        driver.find_element_by_link_text(name).click()
        if name != 'Data_Mentah':
            # range_start column
            driver.find_element_by_id('ctl32_ctl04_ctl03_txtValue').send_keys('10/1/2018')
            # range_finish column
            driver.find_element_by_id('ctl32_ctl04_ctl05_txtValue').send_keys(dt.date.today().strftime("%m/%d/%Y"))
            if (name == 'Performance_Teknisi_Tracker') or (name == 'Data_Mentah_Maintenance'):
                # plant column
                driver.find_element_by_id('ctl32_ctl04_ctl07_txtValue').send_keys('ciawi')
                # workcenter column
                driver.find_element_by_id('ctl32_ctl04_ctl09_txtValue').click() # dropdown first
                driver.find_element_by_id('ctl32_ctl04_ctl09_divDropDown_ctl05').click() # utility
                driver.find_element_by_id('ctl32_ctl04_ctl09_divDropDown_ctl03').click() # fillpack B
                driver.find_element_by_id('ctl32_ctl04_ctl09_divDropDown_ctl02').click() # fillpack A
                driver.find_element_by_id('ctl32_ctl04_ctl09_divDropDown_ctl04').click() # processing
                # category1 column
                driver.find_element_by_id('ctl32_ctl04_ctl11_txtValue').click() # dropdown first
                driver.find_element_by_id('ctl32_ctl04_ctl11_divDropDown_ctl00').click() # all category
                if name == 'Data_Mentah_Maintenance':
                    driver.find_element_by_id('ctl32_ctl04_ctl13_txtValue').click() # dropdown
                    driver.find_element_by_id('ctl32_ctl04_ctl13_divDropDown_ctl00').click() # click all category
            elif name == 'Performance_WO_Tracker':
                # plant column
                driver.find_element_by_id('ctl32_ctl04_ctl09_txtValue').send_keys('ciawi')
                # workcenter column
                driver.find_element_by_id('ctl32_ctl04_ctl11_txtValue').click() # click dropdown first
                driver.find_element_by_id('ctl32_ctl04_ctl11_divDropDown_ctl05').click() # click utility
                driver.find_element_by_id('ctl32_ctl04_ctl11_divDropDown_ctl03').click() # fillpack B
                driver.find_element_by_id('ctl32_ctl04_ctl11_divDropDown_ctl02').click() # fillpack A
                driver.find_element_by_id('ctl32_ctl04_ctl11_divDropDown_ctl04').click() # processing
                # category1 column
                driver.find_element_by_id('ctl32_ctl04_ctl07_txtValue').click() # dropdown
                driver.find_element_by_id('ctl32_ctl04_ctl07_divDropDown_ctl00').click() # click all category
        else:
            # range_start column
            driver.find_element_by_id('ctl32_ctl04_ctl07_txtValue').send_keys('10/1/2018')
            # range_finish column
            driver.find_element_by_id('ctl32_ctl04_ctl09_txtValue').send_keys(dt.date.today().strftime("%m/%d/%Y"))
            # plant column
            driver.find_element_by_id('ctl32_ctl04_ctl11_txtValue').send_keys('ciawi')
            # workcenter column
            driver.find_element_by_id('ctl32_ctl04_ctl03_txtValue').click() # click dropdown first
            driver.find_element_by_id('ctl32_ctl04_ctl03_divDropDown_ctl05').click() # click utility
            driver.find_element_by_id('ctl32_ctl04_ctl03_divDropDown_ctl03').click() # fillpack B
            driver.find_element_by_id('ctl32_ctl04_ctl03_divDropDown_ctl02').click() # fillpack A
            driver.find_element_by_id('ctl32_ctl04_ctl03_divDropDown_ctl04').click() # processing
            # category1 column
            driver.find_element_by_id('ctl32_ctl04_ctl05_txtValue').click() # dropdown
            driver.find_element_by_id('ctl32_ctl04_ctl05_divDropDown_ctl00').click() # click all category
        # submit button
        driver.find_element_by_id('ctl32_ctl04_ctl00').click() # click submit

        # give delay for process
        time.sleep(1)
        try:
            while driver.find_element_by_link_text('Cancel'):
                time.sleep(1)
        except NoSuchElementException:
            pass

        # navigating download menu
        action = ActionChains(driver)
        dropdownmenu = driver.find_element_by_css_selector("#ctl32_ctl05_ctl04_ctl00_ButtonLink > span")
        action.move_to_element(dropdownmenu).perform()
        dropdownmenu.click()
        csvtoclick = driver.find_element_by_link_text("CSV (comma delimited)")
        action.move_to_element(csvtoclick).perform()
        csvtoclick.click()

        # give delay for download process
        time.sleep(1)
        name = name.replace("_", "%5F")
        while os.path.isfile(join(os.getcwd(), 'datasets', name + '.csv')) == False:
            time.sleep(1)
        else:
            while int(os.path.getsize(join(os.getcwd(), 'datasets', name + '.csv'))) == 0:
                time.sleep(1)



    # close driver
    driver.quit()

    # the file has been downloaded, rename it
    counter = 0
    path = join(os.getcwd(), 'datasets')
    for file in os.listdir(path):
        if file.endswith('.csv'):
            if file.find("%5F") > 0:
                counter = counter + 1
                os.rename(join(path, file), path + "\\" + file.replace("%5F", "_"))
            elif counter == 0:
                break
