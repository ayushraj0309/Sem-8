class InfoScraper:
	def __init__(self, profile_url):
		self.profile_url = profile_url
		self.browser = webdriver.Chrome('driver/chromedriver.exe')
		self.bs = self.setBroswerAndGetSoup()
		self.basicProfileInfo = self.getBasicProfileInfo()
		self.all_experiences = self.getAllExperieceInfo()
		self.all_educations = self.getAllEducationInfo()

	def setBroswerAndGetSoup(self):
		self.browser.get(self.browser)
		src = browser.page_source
		soup = BeautifulSoup(src, 'lxml')
		return soup

	def getProfileName(self, bs):
		name_div = bs.find('div', {'class': 'mt2 relative'})
		name_loc = name_div.find_all('div')
		name = name_loc[0].find('h1').get_text().strip()
		return str(name)

	def getProfileLocation(self, bs):
		name_div = bs.find('div', {'class': 'mt2 relative'})
		name_loc = name_div.find_all('div')
		if len(name_loc) == 0:
			return 'None'
		loc = name_loc[-1].find('span').get_text().strip()
		return str(loc)

	def getBasicProfileInfo(self):
		bs = self.bs
		info = {}
		info['Name'] = getProfileName(bs)
		info['Location'] = getProfileLocation(bs)
		return info
	
	def getExpTitle(self, all_exp_spans):
		if len(all_exp_spans) < 2:
			return 'None'
		job_title = all_exp_spans[1].get_text().strip()
		return str(job_title)

	def getExpCompany(self, all_exp_spans):
		if len(all_exp_spans) < 4:
			return 'None'
		company = all_exp_spans[3].get_text().strip().split(' · ')[0]
		return str(company)

	def getExpTimePeriod(self, all_exp_spans):
		if len(all_exp_spans) < 7:
			return 'None'
		time_period = all_exp_spans[6].get_text().strip().split(' · ')[0]
		return str(time_period)

	def getExpInfo(self, exp):
		info = {}
		all_exp_spans = exp.find_all('span')
		job_title = getExpTitle(all_exp_spans)
		company = getExpCompany(all_exp_spans)
		time_period = getExpTimePeriod(all_exp_spans)
		
		info['Job Title'] = job_title
		info['Company'] = company
		info['Time Period'] = time_period
		return info
		
	def getExperienceSetions(self, bs):
		profile_sections = bs.findAll('section')
		exp_profile_section = None
		for profile_section in profile_sections:
			x = profile_section.find('div', {'id': 'experience'})
			if x is not None:
				exp_profile_section = profile_section
				break
		if exp_profile_section is None:
			return {}
		exp_sections = exp_profile_section.find_all('div', {'class': 'display-flex flex-column full-width align-self-center'})
		return exp_sections

	def getAllExperieceInfo(self):
		bs = self.bs
		all_experiences = []
		exp_sections = getExperienceSetions(bs)
		for exp in exp_sections:
			all_experiences.append(getExpInfo(exp))
		return all_experiences

	def getEduSchoolID(self, edu):
		href_class = edu.findAll('a')
		if href_class is None or len(href_class) == 0:
			return 'None'
		school_url = href_class[0].attrs.get('href', None)
		if school_url is None:
			return 'None'
		return str(school_url)

	def getEduSchool(self, all_edu_spans):
		if len(all_edu_spans) < 2:
			return 'None'
		job_title = all_edu_spans[1].get_text().strip()
		return str(job_title)

	def getEduCourse(self, all_edu_spans):
		if len(all_edu_spans) < 4:
			return 'None'
		course_and_discipline = all_edu_spans[4].get_text().strip().split(',')
		if len(course_and_discipline) < 1:
			return 'None'
		course = course_and_discipline[0]
		return str(course)

	def getEduDiscipline(self, all_edu_spans):
		if len(all_edu_spans) < 4:
			return 'None'
		line_text = all_edu_spans[4].get_text()
		course_and_discipline = line_text.strip().split(',')
		if len(course_and_discipline) < 2:
			return 'None'
		ind = line_text.find(', ')
		discipline = line_text[ind+1:]
		return str(discipline)

	def getEduTimePeriod(self, all_edu_spans):
		if len(all_edu_spans) < 8:
			return 'None'
		time_period = all_edu_spans[7].get_text().strip()
		return str(time_period)

	def getEduInfo(self, edu):
		info = {}
		# print(edu)
		all_edu_spans = edu.find_all('span')
		school_url_id = getEduSchoolID(edu)
		school = getEduSchool(all_edu_spans)
		course = getEduCourse(all_edu_spans)
		discipline = getEduDiscipline(all_edu_spans)
		time_period = getEduTimePeriod(all_edu_spans)
		info['Insititution ID'] = school_url_id
		info['Insititution'] = school
		info['Course'] = course
		info['Discipline'] = discipline
		info['Time Period'] = time_period
		return info
		
	def getEducationSetions(self, bs):
		profile_sections = bs.findAll('section')
		edu_profile_section = None
		for profile_section in profile_sections:
			x = profile_section.find('div', {'id': 'education'})
			if x is not None:
				edu_profile_section = profile_section
				break
		if edu_profile_section is None:
			return {}
		edu_sections = edu_profile_section.find_all('div', {'class': 'display-flex flex-column full-width align-self-center'})
		return edu_sections

	def getAllEducationInfo(self):
		bs = self.bs
		all_educations = []
		edu_sections = getEducationSetions(bs)
		for edu in edu_sections:
			all_educations.append(getEduInfo(edu))
		return all_educations

