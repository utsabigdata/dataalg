''' 
Program written by Brandon Lwowski
Purpose: Collect data on product reviews from various 
websites included  in the retail dict object
'''
from amazon import Amazon_Selenium
from walmart import Walmart_Selenium
from target import Target_Selenium
import sys

### Main Program Flow
print ("(A) - AMAZON")
print ("(T) - TARGET")
print ("(W) - WALMART")
print ("(Q) - QUIT")
retailer = input("Select Retailer: ")

### Get User Input For Retailer
while True:
    if retailer.upper() == "A" or  retailer.upper() == "(A)" or  retailer.upper() == "AMAZON":
        retailer = "AMAZON"
        search_retailer = Amazon_Selenium()
        break
    elif retailer.upper() == "T" or  retailer.upper() == "(T)" or  retailer.upper() == "TARGET":
        retailer = "TARGET"
        search_retailer = Target_Selenium()
        break
    elif retailer.upper() == "W" or  retailer.upper() == "(W)" or  retailer.upper() == "WALMART":
        retailer = "WALMART"
        search_retailer = Walmart_Selenium()
        break
    elif retailer.upper() == "Q" or  retailer.upper() == "(Q)" or  retailer.upper() == "QUIT":
        sys.exit()
    else:
        retailer = input("Incorrect Option Try Again: ")

### Get User Input For Product Name
product = input("\nName of Product to Search at {}: ".format(retailer))
product = product.title()


### Get Search Option
print ("\n(S) - PRODUCT SEARCH")
print ("(R) - PRODUCT REVIEWS")
print ("(B) - PRODUCT SEARCH AND REVIEW")
print ('(U) - SCRAPE BY URL')
print ("(Q) - QUIT")

search_options = input("Select Search Option: ")

### Get User Input For Search Options
while True:
    if search_options.upper() == "S" or  search_options.upper() == "(S)" or  search_options.upper() == "PRODUCT SEARCH":
        search_retailer.option = "S"
        search_retailer.open_page()
        search_retailer.collect_data(search_word=product)
        break
    elif search_options.upper() == "R" or  search_options.upper() == "(R)" or  search_options.upper() == "PRODUCT REVIEWS":
        search_retailer.option = "R"
        break
    elif search_options.upper() == "B" or  search_options.upper() == "(B)" or  search_options.upper() == "PRODUCT SEARCH AND REVIEW":
        search_retailer.options = "B"
        break
    elif search_options.upper() == "U" or  search_options.upper() == "(U)" or  search_options.upper() == "SCRAPE BY URL":
        search_retailer.option = "U"
        break
    elif search_options.upper() == "Q" or  search_options.upper() == "(Q)" or  search_options.upper() == "QUIT":
        sys.exit()
    else:
        search_options = input("Incorrect Option Try Again: ")


search_retailer.close_page()