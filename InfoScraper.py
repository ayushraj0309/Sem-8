class InfoScraper:
    def __init__(self, profile_url, logged_in_browser):
        self.profile_id = Helper.get_profile_id_from_linkedin_url(profile_url)
        self.profile_url = profile_url
        self.browser = logged_in_browser
        self.bs = self.setBroswerAndGetSoup()
        self.basicProfileInfo = self.getBasicProfileInfo()
        self.all_experiences = self.getAllExperieceInfo()
        self.all_educations = self.getAllEducationInfo()
        self.is_faculty = Helper.is_from_IIITA(self.all_experiences)
        self.is_student = Helper.is_from_IIITA(self.all_educations)
        self.profile_status = self.connectionStatus()

    def setBroswerAndGetSoup(self):
        self.browser.get(self.profile_url)
        Helper.scroll(self.browser)
        src = self.browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        return soup

    def connectionStatus(self):
        bs = self.bs
        actions_div = bs.find('div', {'class': 'pvs-profile-actions'})
        if actions_div is None:
            return "Error"
        actions = actions_div.findAll('div', {'class': 'entry-point'})
        if ' to connect' in str(actions_div):
            return "Not Connected"
        if 'Pending' in str(actions_div):
            return "Request Pending"
        if actions is None or len(actions) == 0:
            return "Unknown"
        return "Connected"

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
        info['Name'] = self.getProfileName(bs)
        info['Location'] = self.getProfileLocation(bs)
        return info
    
    def getExpURLID(self, bs):
        ids = []
        href_classes = bs.findAll('a', {'data-field': 'experience_company_logo'})
        for href_class in href_classes:
            if href_class is None:
                continue
            exp_url = href_class.attrs.get('href', None)
            if exp_url is None:
                continue
            ids.append(exp_url)
        return ids

    def getExpTitle(self, all_exp_spans):
        if len(all_exp_spans) < 2:
            return 'None'
        job_title = all_exp_spans[1].get_text().strip()
        return str(job_title)

    def getExpCompany(self, all_exp_spans):
        if len(all_exp_spans) < 4:
            return 'None'
        double_text = str(all_exp_spans[3].get_text().strip())
        strip_index = len(double_text)//2
        company = double_text[0:strip_index].split(' · ')[0]
        return str(company)

    def getExpTimePeriod(self, all_exp_spans):
        if len(all_exp_spans) < 7:
            return 'None'
        time_period = all_exp_spans[6].get_text().strip().split(' · ')[0]
        return str(time_period)

    def getExpInfo(self, exp):
        info = {}
        all_exp_spans = exp.find_all('span')
        job_title = self.getExpTitle(all_exp_spans)
        company = self.getExpCompany(all_exp_spans)
        time_period = self.getExpTimePeriod(all_exp_spans)
        
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
        company_ids = self.getExpURLID(bs)
        exp_sections = self.getExperienceSetions(bs)
        for exp in exp_sections:
            all_experiences.append(self.getExpInfo(exp))
        for i in range(len(all_experiences)):
            if i >= len(company_ids):
                all_experiences[i]['URL ID'] = 'None'
                continue
            all_experiences[i]['URL ID'] = str(company_ids[i])
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
        school_url_id = self.getEduSchoolID(edu)
        school = self.getEduSchool(all_edu_spans)
        course = self.getEduCourse(all_edu_spans)
        discipline = self.getEduDiscipline(all_edu_spans)
        time_period = self.getEduTimePeriod(all_edu_spans)
        info['URL ID'] = school_url_id
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
        edu_sections = self.getEducationSetions(bs)
        for edu in edu_sections:
            all_educations.append(self.getEduInfo(edu))
        return all_educations