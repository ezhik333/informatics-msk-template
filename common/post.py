import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder
import brotli # required
import time
import os.path
import json
from collections import OrderedDict


RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

if(os.path.exists("post.json") == False):
    print(f"{RED}Not found 'post.json' file.{NC} Creating template. Please provide correct data there.")
    pj = "{\n    \"login\": \"\",\n    \"password\": \"\",\n    \"user_id\":\"\",\n    \"task_no\": \"\"\n}"

    with open('post.json', 'w') as outfile:
        outfile.write(pj)
    exit()

with open('post.json') as json_file:
    pdata = json.load(json_file)

pfail = 0
pj = pdata
if("login" in pj):
    if(pj['login'] == ""):
        print(f"{RED}login not found in 'post.json'{NC}")
        pfail = pfail + 1

if("password" in pj):
    if(pj['password'] == ""):
        print(f"{RED}password not found in 'post.json'{NC}")
        pfail = pfail + 1

if("user_id" in pj):
    if(pj['user_id'] == ""):
        print(f"{RED}user_id not found in 'post.json'{NC}")
        print(f"{BLUE}\tGo to site and open your \"about user\" page.{NC}")
        print(f"{BLUE}\tYou will see a link like this: {GREEN}https://informatics.msk.ru/user/profile.php?id=<YOUR_USER_ID>{NC}")
        pfail = pfail + 1

if("task_no" in pj):
    if(pj['task_no'] == ""):
        print(f"{RED}task_no not found in 'post.json'{NC}")
        print(f"{BLUE}\tYou can find task number on website{NC}")
        print(f"{BLUE}\tAlso check task page link: {GREEN}https://informatics.msk.ru/mod/statements/view.php?chapterid=<TASK_NO>#1{NC}")
        pfail = pfail + 1

if(pfail > 0):
    exit();

user_id = pj['user_id']
task_no = pj['task_no']
login = pj['login']
password = pj['password'];


s = requests.Session();
s.headers.update(
    {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "informatics.msk.ru",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"})
r = s.get("https://informatics.msk.ru/");

if(r.status_code != 200):
    print(f"{RED}Error while opening start page{NC}")
    exit();

logintoken_field = BeautifulSoup(r.content, features="html.parser").findAll(attrs={'name' : 'logintoken', 'type' : 'hidden'})
logintoken = str(logintoken_field[0]['value'])


post_data = {
    "username" : login,
    "password" : password,
    "rememberusername" : "1",
    "logintoken" : logintoken    
}

# print(post_data);

r = s.post("https://informatics.msk.ru/login/index.php", data=post_data)
print("Post login info: ", r.status_code)
if(r.status_code != 200):
    print(f"{RED}Error while trying to login{NC}")
    exit();

# TODO check if login success

mp_encoder = MultipartEncoder(
    fields={
        'lang_id': '3',
        'file': ('main.cpp', open('main_no_comments.cpp', 'rb'), 'text/x-c++src'),
    }
)

url = f"https://informatics.msk.ru/py/problem/{task_no}/submit";
print(url)
r = s.post(url, data=mp_encoder, headers={'Content-Type': mp_encoder.content_type})
print("Posting file :", r.status_code)
if(r.status_code != 200):
    print(f"{RED}Error while trying to post code{NC}")
    exit();

print("-----")
print(r.json())

j = r.json()
if(j['status'] == "error"):
    print(f"{RED}{j['error']}{RED}")
    print("Fail. Exit...")
    exit();

runid = j['data']['run_id']
#runid = "32348698"
url = f"https://informatics.msk.ru/py/protocol/get/{runid}"

success = 0;
for i in range(0, 10):
    r = s.get(url)
    print("Protocol get: ", r.status_code)
    j = r.json()
    if("status" not in j):
        print("No error!")
        success = 1
        break
    print(r.json())
    print("Not ready. Waiting 5 seconds more...")
    time.sleep(5)

if(success == 0):
    print("{RED}No success after 10 attempts... Check manually on site :({NC}")
    exit();

if("tests" not in j):
    print("{RED}Not found any test data. Exit...{NC}")
    exit()

my_tests = j

if("compiler_output" in my_tests):
    if(my_tests['compiler_output'] != ""):
        print(f"{RED}COMPILER ERROR!{NC}")
        print(my_tests['compiler_output'])
        exit();


my_tests_sorted = sorted(my_tests['tests']);

print(my_tests['tests'])

print(f"\n\n\n")

fail_counter = 0;
for test in my_tests_sorted:
    #print(my_tests_sorted[test])
    test_info = my_tests['tests'][test]
    mem = test_info['max_memory_used']
    ntime = test_info['time']
    rtime = test_info['time']
    s_status = test_info['string_status']
    if(s_status == "OK"):
        s_status = f"{GREEN}{s_status}{NC}"
    else:
        s_status = f"{RED}{s_status}{NC}"
        fail_counter = fail_counter + 1

    print(f"{test}:\t{s_status}\t{rtime}\t{mem}")

if(fail_counter == 0):
    print(f"\n{GREEN}SUCCESS!{NC}")
else:
    print(f"\n{RED}FAILS: {fail_counter}{NC}")
