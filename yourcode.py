import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
#用户输入
user_input = sys.argv[1:]
if(len(user_input) != 2):
    print("需两个输入，日期和货币代码")
    exit(0)
if(len(user_input[0]) != 8 or len(user_input[1])!= 3):
    print("日期或货币代码格式错误")
    exit(0)
#转换用户输入格式与网页输入格式相同
input_1 = user_input[0]
input_1 = input_1[:4]+"-"+input_1[4:6]+"-"+input_1[6:]
input_2 = user_input[1]
#打开中文与货币代码转换网页
web = webdriver.Chrome()
name_url = "https://www.11meigui.com/tools/currency"
web.get(name_url)

# 定位td表格
td_element = web.find_element(By.XPATH, "/html/body/main/div/table/tbody/tr[2]/td")

# 定位tr，tr代表每一行的数值
tr_elements = td_element.find_elements(By.TAG_NAME, "tr")

# 将每一行tr数值放入pandas表格以便后续操作
data = []
for tr_element in tr_elements:
    td_data = []
    td_elements = tr_element.find_elements(By.TAG_NAME, "td")
    for td_element in td_elements:
        td_data.append(td_element.text)
    data.append(td_data)

df = pd.DataFrame(data)

output_file = "output_table.cvs"

df.to_csv(output_file)
#将表格导入cvs表格以便后续操作

web.quit()
matching_input_df = pd.read_csv("output_table.cvs",skiprows= 1, header = 1)
matching_input_df = matching_input_df[['英文','Unnamed: 5']]

filtered_input = matching_input_df.loc[matching_input_df['Unnamed: 5'] == user_input[1], '英文']


web = webdriver.Chrome()

url = "https://www.boc.cn/sourcedb/whpj/"
web.get(url)

#输入第一日期
input_field1 = web.find_element(By.XPATH, "/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[2]/div/input")
input_field1.send_keys(input_1)
#输入第二日期
input_field2 = web.find_element(By.XPATH, "/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[4]/div/input")
input_field2.send_keys(input_1)
#选择货币代号所代表中文
select_element = Select(web.find_element(By.XPATH, "/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[6]/select"))
select_element.select_by_visible_text(filtered_input.iloc[0]) 
#跳转至所需网页
element = web.find_element(By.XPATH, "/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[7]")
element.click()
#等待加载
web.implicitly_wait(10)
#抓取所需输出
final_out_put_element = web.find_element(By.XPATH,'/html/body/div/div[4]/table/tbody/tr[2]/td[4]')
print(final_out_put_element.text)

web.quit()



    


