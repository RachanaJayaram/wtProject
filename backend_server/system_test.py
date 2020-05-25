import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Setting up the webdriver.
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(
    executable_path="C:\chromedriver_win32\chromedriver.exe", chrome_options=chrome_options)


# Testing inputs.
baseUrl = "http://127.0.0.1:4200/{}"
test_input = '''4 5\n0 1 5\n0 2 2\n0 3 1\n3 1 3\n2 3 2\n0 3\n'''

'''
Testing home page content.
The entirety of the home page is rendered dynamically.
The front end JS sends requests to the backend server to fetch content,
this way the author can change article data in the backend without having to change the html file.
The list of elements in the front page is a rss feed.
Initially we have manually published 3 articles
1.  Dijkstras Algorithm
2.  Bellman Ford Algorithm
3.  Floyd Warshall Algorithm
The first 3 tests ensure, the rss feed reflects this.
The 4th test checks if the publishing link is properly rendered.
'''
print("**Testing Home page content**")

# Get all links in the page.
driver.get(baseUrl.format("home"))
time.sleep(2)
a_tags = driver.find_elements_by_tag_name('a')
rendered_hrefs = [link.get_attribute("href") for link in a_tags]


'''Test 1'''
print("Test 1 - Check if Dijkstras Algorithm article is linked")
assert baseUrl.format(
    "algorithm-description/dijkstra") in rendered_hrefs
print("Passed")


'''Test 2'''
print("Test 2 - Check if Bellman Ford article is linked")
assert baseUrl.format(
    "algorithm-description/bellman-ford") in rendered_hrefs
print("Passed")


''' Test 3'''
print("Test 3 - Check if Floyd Warshall article is linked")
assert baseUrl.format(
    "algorithm-description/floyd-warshall") in rendered_hrefs
print("Passed")


'''Test 4'''
print("Test 4 - Check if link to publish new article exists")
assert baseUrl.format("publish") in rendered_hrefs
print("Passed")


'''
Testing algorithm description page.
The algorithm description page is completely dynamically rendered.
The html page is the same regardless of which algorithm was previously clicked by the user.

Test 5 - By using Jinja2 data injection and by sending XHR requestes to the backend server,
we get the article content dynamically.  (Including this heading)
The backend stores xml file containing content details for each algorithm.

Test 6 - The author link is also dynamically added based on the contents of the xml file of the algorithm 

Test 7 - The intelligent functionality of the project is that -
youtube video tutorials related to the article content are embedded.

Test 8 - The example and demo section is only rendered for those algorithms for which visualization is implemented,
this is signalled by a field in the xml file.
'''

print("**Testing Algorithm Description Page**")


driver.get(baseUrl.format("algorithm-description/dijkstra"))
time.sleep(6)
heading = "Dijkstras"


'''Test 5'''
print("Test 5 - Check if heading is properly injected.")
assert "{} Algorithm".format(heading) == driver.find_elements_by_class_name(
    "post-heading")[0].get_attribute("innerText")
print("Passed")


'''Test 6'''
print("Test 6 - Check if author bio is linked.")
assert driver.find_element_by_id(
    "author").get_attribute("innerText").strip() == "Rachana Jayaram"
print("Passed")


'''Test 7'''
print("Test 7 - Check if related video recommendations are embedded.")
video_count = 0
div_children = driver.find_element_by_id("youtube").find_elements_by_xpath(".//*")
for element in div_children:
    if element.get_attribute("tagName") == "IFRAME":
        video_count += 1
assert video_count > 0
print("Passed")


'''Test 8'''
print("Test 8 - Check if demo section is rendered for Dijkstras.")
try:
    driver.find_element_by_id("example")
    assert True
except:
    assert False
print("Passed")


'''
Testing Dijkstras Visualization page.
Graph in the vizualization page is rendered based on input submitted in the previous page,
only if input is valid.

Test 9 - Automatically enter input, and submit form - subsequently check if graph is rendered.

Test 10 - Check if graph doesnt glitch/still exists when next button is clicked.
'''

print("**Testing Visualization Page**")


'''Test 9'''
print("Test 9 - Check if graph is rendered for correct input.")
input_element = driver.find_element_by_name("input")
input_element.clear()
input_element.send_keys(test_input)
time.sleep(6)
driver.find_element_by_class_name("btn").click()
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
time.sleep(6)
try:
    driver.find_element_by_id("graph-container")
    assert True
except:
    assert False
print("Passed")


''' Test 10'''
print("Test 10 - Check if graph is remains-rendered for on clicking next.")
driver.find_element_by_id("next").click()
time.sleep(3)
try:
    driver.find_element_by_class_name("sigma-mouse")
    assert True
except:
    assert False
print("Passed")

driver.find_element_by_id("next").click()
time.sleep(2)
driver.find_element_by_id("next").click()
time.sleep(2)
driver.find_element_by_id("next").click()
time.sleep(2)
driver.find_element_by_id("next").click()
time.sleep(2)
driver.find_element_by_id("next").click()
time.sleep(2)
driver.find_element_by_id("next").click()
time.sleep(2)
driver.find_element_by_id("next").click()
time.sleep(2)

driver.close()
