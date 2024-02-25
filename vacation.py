import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from tools import *
from constants import *
from config import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', type = str, help = 'myworkday url', default="")

args = parser.parse_args()
print(args.url)

class YourWorkDayApply(Hand):
    def __init__(self, url: str, email: str, password: str):
        super().__init__(webdriver.Chrome())
        if url and url[-1] == '/':
            url = url[:-1]
        self.url_jd = url
        self.url_apply = url + '/apply'
        self.url_apply_manually = url + '/apply/applyManually'
        self.email = email
        self.pwd = password

    def valid(self):
        """Validate the job is a workday post by examing the URL."""
        return True

    def action(self, new_application = False):
        """Apply for a workday job posting."""

        try:
            if new_application:
                self.navigate_create_account()
                time.sleep(10)
                
            self.driver.get(self.url_apply)
            if not yes_or_not("log-in"):
                return
            try:
                self.log_in() # might be already logged in
            except NoSuchElementException:
                input("Probably already logged in, verify or login manually then enter")
            time.sleep(2)
        except Exception as e:
            # sometimes it does not require login
            print("Login failed. \n\t1. It might not be necessary.(not very likely) \n\t2. You might have an account already using the same email and another password (very likely), manully login and enter. \n\t 3.Wrong URL")
        
        self.driver.get(self.url_apply_manually) # might not be necessary
        time.sleep(5)

        try:
            self.my_information()
        except Exception as e:
            print(e)
        input("make sure my information is correct and enter")
        self.save_and_continue("experience")
        
        time.sleep(2)
        try:
            self.add_work_experience()
        except Exception as e:
            print(e)

        time.sleep(2)
        try:
            self.add_education()
        except Exception as e:
            print(e)

        #self.upload_resume()
        input("Manually answer application questions")
        try:
            self.save_and_continue("disclosure")
        except:
            input("make sure we are on the next page and enter")

        time.sleep(3)
        try:
            self.disclosure_questions()
        except Exception as e:
            print(e)
        input("Confirm disclosure questions are answerred corrected and enter")
        self.save_and_continue("self identify")

        try:
            self.self_identify()
        except Exception as e:
            print(e)
        input("End of Automation! Confirm disability questions are answerred corrected and enter and manual submit")

        time.sleep(10000)

    def self_identify(self):
        try:
            self.fill_by_xpath('//*[@data-automation-id="name"]', f"{FNAME} {LNAME}")
        except:
            pass
        time.sleep(1)
        try:
            self.find_by_xpath('//*[@text()="I do not want to answer"]').click() # not working
        except:
            pass
        time.sleep(1)
        try:
            self.find_by_xpath('//*[@data-automation-id="dateIcon"]').click()
            #? self.find_by_xpath( '//*[@data-automation-id="dateIcon"]').click().submit()
            #? self.find_by_xpath( '//*[@data-automation-id="dateIcon"]').click().send_keys(webdriver.common.keys.ENTER)
            input("type enter on the browser to confirm the date")
        except:
            pass

    def disclosure_questions(self):
        try:
            self.click_and_select('veteranStatus', 'I DO NOT WISH TO SELF-IDENTIFY')
        except:
            pass
        try:
            self.click_and_select('gender', 'Male')
        except:
            pass
        try:
            self.click_and_select('hispanicOrLatino', 'No')
        except:
            pass
        try:
            self.click_and_select('ethnicDropdown', 'Not Specified')
        except:
            pass
        try:
            self.find_by_xpath('//*[@data-automation-id="agreementCheckbox"]').click()
        except:
            pass

    def my_information(self):
        # select country
        if True:
            try:
                self.find_by_xpath('//*[@data-automation-id="sourceDropdown"]').click()
                time.sleep(1)  # ElementClickInterceptedException
                try:
                    self.find_by_xpath('//*[text()="LinkedIn"]').click() # select linkedIn as source

                    # click_radio() # possibly check the box if necessary
                    
                except NoSuchElementException:
                    try:
                        self.find_by_xpath('//*[text()="Indeed"]').click() # select linkedIn as source
                    except NoSuchElementException:
                        input("Manual input required for job source, enter after manual input is completed")
            except ElementClickInterceptedException:
                print("source already selected")
            except AttributeError:
                print("source might already be selected")
            except Exception as e:
                input("source selection failed, manually select and enter")
        
        if False: # doesn't seem to be necessary
            try:
                self.find_by_xpath('//*[@data-automation-id="countryDropdown"]').click()
                time.sleep(1)
                self.find_by_xpath( '//*[text()="United States of America"]').click() # select US as country
            except ElementClickInterceptedException:
                print("country alread selected")
            except AttributeError:
                print("source might already be selected")
 
        input("make sure that the source is corrected enterred")
        try:
            self.fill_by_xpath('//*[@data-automation-id="legalNameSection_firstName"]', FNAME)
            self.fill_by_xpath('//*[@data-automation-id="legalNameSection_lastName"]', LNAME) # ???
        except Exception as e:
            print(e)
            input("make sure name is correct then continue")
        #phone type
        self.fill_by_xpath('//*[@data-automation-id="phone-number"]', F) # ???

        try:
            self.fill_by_xpath('//*[@data-automation-id="email"]', E)
        except Exception as e:
            pass # occasionally it require email on this page, when no login is required

        #<button aria-haspopup="listbox" type="button" value="bfc1aaf99d474ef496653b223dbcf47f" data-automation-id="phone-device-type" id="input-12" aria-label="Phone Device Type Mobile required" class="css-o82vv0">Mobile</button>
        #mobile
        try:
            self.find_by_xpath( '//*[@data-automation-id="phone-device-type"]').click()
            time.sleep(1)
            self.find_by_xpath( '//*[text()="Mobile"]').click()
        except ElementClickInterceptedException:
            input("phone selected exception, inspect and enter")
        except AttributeError:
            input("phone selected exception, inspect and enter")


    def click_and_select(self, xpath: str, select_str: str) -> bool:
        try:
            self.find_by_xpath( '//*[@data-automation-id="' + xpath + '"]').click()
            #<div>I DO NOT WISH TO SELF-IDENTIFY</div>
            self.find_by_xpath( '//*[text()="' + select_str + '"]').click() 
            return True
        except ElementClickInterceptedException:
            print(f"{xpath} already selected")
            return False
        except AttributeError:
            print(f"{xpath} already selected")
            return False
        except Exception as e:
            return False

    def upload_resume(self):
        #file_input = self.driver.find_element(webdriver.common.by.By.CSS_SELECTOR, "input[type='file']")
        #file_input.send_keys(upload_file)
        #driver.find_element(By.ID, "file-submit").click()
        #<input data-automation-id="file-upload-input-ref" type="file" multiple="" class="css-1hyfx7x">
        self.fill_by_xpath( xpath='//*[@data-automation-id="file-upload-input-ref"]', value='/home/yellow/Downloads/Resume.pdf')

    def add_education(self):
        try:
            #<button aria-label="Add Education" data-automation-id="Add" font-size="14" height="40" class="css-6719aw">Add</button>
            self.find_by_xpath( '//button[@aria-label="Add Education"]').click() # Mon 22 Jan 2024 11:03:23 PM EST
        except Exception as e:
            print(e)
            input("make sure education is added/opened")
        
        time.sleep(1)
        education, count = csv_to_dictionary('education.csv')
        for i in range(count): # index out of range error?
            #enter_and_select(self.driver, '')
            self.fill_by_xpath_at_index('//*[@data-automation-id="school"]', education['School or University'][i], i)
            try:
                self.find_by_xpath_at_index('//*[@data-automation-id="degree"]', i).click()
                #self.find_by_xpath_at_index('//*[text()="' + education['Degree'][i] + '"]', i).click()
                #self.find_by_xpath_at_index('//*[text()="80-Master"]', i).click()
                self.find_by_xpath( '//li[contains(text(), "' + education['Degree'][i] + '")]').click()
            except Exception as e:
                print(e)
                input("make sure degree is enterred correctly and enter")

            try:
                # not working
                self.fill_by_xpath_at_index('//*[@data-automation-id="dataSectionYear-input"]', education['From'][i], int(i * 2)) 
                self.fill_by_xpath_at_index('//*[@data-automation-id="dataSectionYear-input"]', education['To'][i], int(i * 2 + 1))
            except:
                input("make sure year are added")

            if i != count - 1:
                try:
                    self.find_by_xpath( '//button[@aria-label="Add Another Education"]').click()
                except ElementClickInterceptedException:
                    input("manual action requried: click add another education and enter")

    def add_work_experience(self):
        try:
            self.find_by_xpath( '//button[@aria-label="Add Work Experience"]').click()
            time.sleep(1)
        except NoSuchElementException:
            pass
        #stale element not found error?
        work_experience, count = csv_to_dictionary('work_experience.csv')
        time_box_index = 0
        for i in range(count):
            self.fill_by_xpath_at_index('//*[@data-automation-id="jobTitle"]', work_experience['Job Title'][i], i)
            self.fill_by_xpath_at_index('//*[@data-automation-id="company"]', work_experience['Company'][i], i)

            time.sleep(1)
            
            if work_experience['I currently work here'][i] == 'Yes':
                self.driver.find_elements(by = webdriver.common.by.By.XPATH, value = '//*[@data-automation-id="currentlyWorkHere"]')[i].send_keys(webdriver.Keys.SPACE)

                year, month = int(work_experience['From'][i].split('/')[0]), int(work_experience['From'][i].split('/')[1])
                self.data_selector(time_box_index, year, month)
                time_box_index += 1
            elif work_experience['I currently work here'][i] == 'No':
                year, month = int(work_experience['From'][i].split('/')[0]), int(work_experience['From'][i].split('/')[1])
                self.data_selector(time_box_index, year, month)
                time_box_index += 1
                year, month = int(work_experience['To'][i].split('/')[0]), int(work_experience['To'][i].split('/')[1])
                self.data_selector(time_box_index, year, month)
                time_box_index += 1
            else:
                raise ValueError

            self.fill_by_xpath_at_index('//*[@data-automation-id="description"]', work_experience['Role Description'][i], i)
            if i != count - 1:
                try:
                    self.find_by_xpath( '//button[@aria-label="Add Another Work Experience"]').click()
                    time.sleep(1)
                except Exception as e:
                    print(e)
                    input("manual action requried: click add another work experience and enter")
             
    def save_and_continue(self, page_name: str = None):
        #<button data-automation-id="bottom-navigation-next-button" font-size="14" height="40" class="css-a9u6na">Save and Continue</button>
        try:
            self.find_by_xpath( '//*[text()="Save and Continue"]').click()
        except NoSuchElementException:
            self.find_by_xpath( '//*[@data-automation-id="bottom-navigation-next-button"]').click()
        except Exception:
            pass 
        input(f"Now we should be on the next page '{page_name}', if not, manually fill table and continue")

    def navigate_create_account(self):
        self.driver.get(self.url_jd)
        if not yes_or_not("create-account"):
            return
        self.driver.get(self.url_apply)

        sleep()
        self.find_by_xpath(CREATE_ACCOUNT_PAGE_XPATH).click()
        sleep()
        self.create_account()
        time.sleep(5)

        if not yes_or_not("verify account in the email and then continue"):
            return
        self.driver.get(self.url_jd)
 
    def create_account(self):
        """Creat account with password and save it into a file"""
        self.fill_by_id("input-6", self.email)
        sleep()
        self.fill_by_id("input-7", self.pwd)
        sleep()
        self.fill_by_id("input-8", self.pwd)
        input("check if there is a checkbox before creating account")
        # might be a checkbox here need intervantion
        # might need to use a div tag
        self.find_by_xpath( CREATE_ACCOUNT_SUB_XPATH).click()
    
    def log_in(self):
        """Sign in"""
        self.fill_by_id("input-4", self.email)
        self.fill_by_id("input-5", self.pwd)
        sleep()
        self.login()
        time.sleep(2)
        

def example():
    """A simple test to validate set up is correct."""
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    driver.find_element(by = webdriver.common.by.By.NAME, value = "q").send_keys("selenium")
    driver.find_element(by = webdriver.common.by.By.NAME, value = "q").submit()
    time.sleep(10)
    driver.close()

if __name__ == "__main__":
    apply_url = args.url
    if apply_url == "":
        apply_url = input("enter application url: ")
    operation = YourWorkDayApply(url = apply_url, email = E, password = P)
    operation.action(new_application = True)

    print(csv_to_dictionary(file_path = "work_experience.csv"))
 
