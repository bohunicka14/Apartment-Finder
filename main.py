from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from collections import namedtuple
import os
from os.path import isfile
import csv

WEB_PAGE = 'https://www.byty.sk/bratislava/'
TEST = 'https://www.byty.sk/bratislava-ii-ruzinov/2-izbove-byty/predaj/?p[param1][to]=150000&p[foto]=1&p[limit]=60'

AppartmentAd = namedtuple('AppartmentAd', [
	'title', 
	'location',
	'condition_info', 
	'url',
	'price', 
	'date'  
])

class AppartmentDownloader():
	def __init__(self, csvpath=None):
		self.db_path = csvpath
		self.db = []

		opts = Options()
		opts.set_headless()

		assert opts.headless

		self.browser = Firefox(options=opts)
		
		self.browser.get(TEST) 

		self.curr_page = 1

		# self.set_parameters()
		# self.browser.implicitly_wait(5)
		self.total_pages()

		self.load_ads()
		while self.next_page():
			self.load_ads()

		self.save_ads_to_db()

		self.browser.quit()

	def total_pages(self):
		pages = self.browser.find_element_by_class_name('vpravo')
		all_buttons = pages.find_elements_by_css_selector('#nastranu ul.vpravo li a')
		self.total_number_of_pages = len(all_buttons)

	def next_page(self):
		if self.curr_page + 1 > self.total_number_of_pages:
			return False
		self.curr_page += 1
		pages = self.browser.find_element_by_class_name('vpravo')
		all_buttons = pages.find_elements_by_css_selector('#nastranu ul.vpravo li a')
		for button in all_buttons:
			if button.text == str(self.curr_page):
				self.browser.execute_script("arguments[0].click();", button)
				# button.click()
				return True




	def load_ads(self):
		all_ads = self.browser.find_elements_by_class_name('inzerat')

		for ad in all_ads:
			_title = ad.find_element_by_class_name('advertisement-head').text
			content = ad.find_element_by_class_name('inzerat-content')
			_location = content.find_element_by_css_selector('.inzerat .inzerat-content .locationText').text
			# _condition_info = content.find_element_by_class_name('condition-info').text
			_condition_info = ''
			_url = ad.find_element_by_css_selector('div.advertisement-head a').get_attribute('href')
			_price = ad.find_element_by_css_selector('.inzerat .price span').text
			_date = ad.find_element_by_class_name('date').text
			self.db.append(AppartmentAd(_title, _location, _condition_info, _url, _price, _date))


	def save_ads_to_db(self):
		with open(self.db_path,'w',newline='') as dbfile:
			dbwriter = csv.writer(dbfile, delimiter=';')
			dbwriter.writerow(list(AppartmentAd._fields))
			for entry in self.db:
				dbwriter.writerow(list(entry))

	def set_parameters(self):

		## typ
		select_type = self.browser.find_element_by_id('param3')
		select_type.click()
		
		type_value = select_type.find_element_by_name('24|predaj')
		type_value.click()

		## druh
		select_category = self.browser.find_element_by_id('hlavne_kategorie')
		select_category.click()
		
		category_value = select_category.find_element_by_name('10002') ## dvojizbovy
		category_value.click()

		## lokalita
		region = self.browser.find_element_by_id('region')
		# region.click()
		region_input = region.find_element_by_id('region')
		region_input.send_keys('Bratislava II - Ružinov')

		## cena do
		# max_price = self.browser.find_element_by_name('p[param1][to]')
		# max_price.click()
		# max_price.send_keys('150000')

		## browse button
		button = self.browser.find_element_by_css_selector('span.button.red')
		# button.click()
		self.browser.execute_script("arguments[0].click();", button)

		## number of results displaying on one page
		number_of_results = self.browser.find_element_by_id('limitSelect')
		number_of_results.click()

		number_of_results_value = number_of_results.find_element_by_class_name('limit_60')
		number_of_results_value.click()

		

	
	
if __name__ == "__main__":
	#path = os.path.dirname(os.path.abspath(__file__))
	run = AppartmentDownloader('results.csv')
	# with open('test.csv','w',newline='') as dbfile:
	# 		dbwriter = csv.writer(dbfile, delimiter=',')
	# 		dbwriter.writerow(['a', 'ž'])
	
		
