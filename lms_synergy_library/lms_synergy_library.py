from requests import Session
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from .utils import clean_data, SoupLms
from .exceptions import LanguageNotFoundError, UserIsNotTeacherError, UserIsNotStudentError
from .constants import URL_LOGIN, URLS_LANGUAGES, URL
from typing import Dict, List


class LMS:
    session: Session = None
    type_user: str = None

    def __init__(
        self,
        login: str = "demo",
        password: str = "demo",
        proxy: dict = None,
        headers: dict = None,
        language: str = "en",
    ) -> None:
        """Init LMS

        :param login: Login
        :param password: Login
        :param proxy: Proxy
        :param headers: Headers
        :param language: Language

        :type login: str
        :type password: str
        :type proxy: dict
        :type headers: dict
        :type language: str

        :return: None
        :rtype: None

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms.get_name()
        'Student Demonstratsionnyiy'
        """

        self.login = login
        self.password = password
        self.proxy = proxy
        self.headers = headers

        if language not in URLS_LANGUAGES:
            raise LanguageNotFoundError("No such language %s" % language)
        self.language = language

        self.__sign()

    def __del__(self) -> None:
        """Close session

        :return: None
        :rtype: None

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> del lms
        """

        if self.session:
            self.session.close()

    def __sign(self) -> None:
        """Auth

        :return: None
        :rtype: None

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms._LMS__sign()
        """

        headers: dict = (
            self.headers if self.headers else {"User-Agent": UserAgent().random}
        )
        proxies: dict = self.proxy if self.proxy else {}

        data: dict = {"popupUsername": self.login, "popupPassword": self.password}

        self.session = Session()
        self.session.headers.update(headers)
        self.session.post(URL_LOGIN, data=data, proxies=proxies)
        self.session.get(URLS_LANGUAGES[self.language], proxies=proxies)
        self.type_user = self.get_type_user()

    def get_type_user(self) -> str:
        """Returns type user

        :return: Type user
        :rtype: str

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms.get_type_user()
        'student'
        """

        if not self.type_user:
            soup: bs = SoupLms.get_soup_schedule(
                session=self.session,
                language=self.language,
                cookies=self.cookies,
                proxies=self.proxy
            )

            all_roles: bs = soup.find("div", {"class": "drop-menu drop-select small"}).find("ul")
            
            drop_menu_label: bs = soup.find("div", {"id": "switch-accounts"}).find("div", {"class": "drop-menu-label"})
            current_type_user: str = drop_menu_label.find("span", {"class": "title"}).text

            roles: List[Dict[str, str]] = []

            for li in all_roles.find_all("li"):
                if li.find("b"):
                    roles.append({"name": li.find("b").text.lower()})
                elif li.find("a"):
                    roles[-1]["type"] = li.find("a").text.lower()

            for role in roles:
                if role["name"] == current_type_user:
                    self.type_user = role["type"]
                    break

            if not self.type_user:
                self.type_user = roles[0]["name"]

        return self.type_user

    @property
    def cookies(self) -> dict:
        """Returns cookies

        :return: Cookies
        :rtype: dict

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> cookies = lms.cookies
        """

        return self.session.cookies.get_dict()

    @cookies.setter
    def cookies(self, cookies: dict) -> None:
        """Set cookies

        :param cookies: Cookies
        :type cookies: dict

        :return: None
        :rtype: None

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms.cookies = {"PHPSESSID": "demo"}
        """

        self.session.cookies.update(cookies)

    def verify(self) -> bool:
        """Verify auth

        :return: True or False
        :rtype: bool

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms.verify()
        True
        """

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        return soup.find("div", {"class": "user-name"}) is not None

    def get_name(self) -> str:
        """Returns name

        :return: Name
        :rtype: str

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms.get_name()
        'Student Demonstratsionnyiy'
        """

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        name: str = soup.find("div", {"class": "user-name"}).text

        return clean_data.remove_many_spaces(name)

    def get_amount_messages(self) -> int:
        """Returns amount messages

        :return: Amount messages
        :rtype: int

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms.get_amount_messages()
        0
        """

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        return SoupLms.get_amount_messages_from_soup(
            soup, self.language
        )

    def get_amount_notifications(self) -> int:
        """Returns amount notifications

        :return: Amount notifications
        :rtype: int

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms.get_amount_notifications()
        0
        """

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        return SoupLms.get_amount_notify_from_soup(
            soup, self.language
        )

    def get_amount_unverified_work(self) -> int:
        """Returns amount unverified work

        :return: Amount unverified work
        :rtype: int

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> # lms.get_amount_unverified_work()
        >>> # error - if user is not teacher
        >>> # 0 - if user is teacher and amount unverified work is 0
        """

        if self.type_user not in ["teacher", "преподаватель"]:
            raise UserIsNotTeacherError("User is not teacher")

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        titles: dict = {
            "ru": "Требуют проверки",
            "en": "Require verification",
        }

        amount_unverified_work: str = soup.find("a", title=titles[self.language])

        if amount_unverified_work is None:
            return 0

        return int(clean_data.remove_many_spaces(amount_unverified_work.text))

    def get_info(self) -> dict:
        """Returns information about user

        :return: Information about user
        :rtype: dict

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> lms.get_info()
        {'name': 'Student Demonstratsionnyiy', 'amount_messages': 0, 'amount_notifications': 0}
        """

        return {
            "name": self.get_name(),
            "amount_messages": self.get_amount_messages(),
            "amount_notifications": self.get_amount_notifications(),
        }

    def get_schedule(self) -> dict:
        """Returns schedule

        :return: Schedule
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> schedule = lms.get_schedule()
        >>> # schedule # schedule for student
        >>> # {
        >>> #   "31.01.23, Tue": {
        >>> #       "09:55 - 11:40": {
        >>> #           "name": "Mathematics",
        >>> #           "classroom": "D-101"
        >>> #           "type": "lecture"
        >>> #           "teacher": "Teacher Demonstratsionnyiy"
        >>> #       },
        >>> #   },
        >>> # }
        >>> # schedule # schedule for teacher
        >>> # {
        >>> #   "31.01.23, Tue": {
        >>> #       "09:55 - 11:40": {
        >>> #           "name": "Mathematics",
        >>> #           "Group": "it-21"
        >>> #           "classroom": "D-101"
        >>> #           "type_lesson": "lecture"
        >>> #       },
        >>> #   },
        >>> # }
        """
        types: dict = {
            "студент": "student",
            "преподаватель": "teacher",
            "student": "student",
            "teacher": "teacher"
        }

        return eval("self._get_%s_schedule" % types[self.type_user])()

    def _get_student_schedule(self) -> dict:
        """Returns schedule for student

        :return: Schedule
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> schedule = lms._get_student_schedule()
        >>> # schedule
        >>> # {
        >>> #   "31.01.23, Tue": {
        >>> #       "09:55 - 11:40": {
        >>> #           "name": "Mathematics",
        >>> #           "classroom": "D-101"
        >>> #           "type": "lecture"
        >>> #           "teacher": "Teacher Demonstratsionnyiy"
        >>> #       },
        >>> #   },
        >>> # }
        """

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        table: bs = soup.find("table", {"class": "table-list v-scrollable"})
        shedule: dict = {}

        for tr in table.find("tbody").find_all("tr"):
            if len(tr.find_all("td")) == 1:
                return shedule
            if tr.find("th"):
                date: str = clean_data.remove_many_spaces(tr.find("th").text)
                shedule[date] = {}
            else:
                time: str = clean_data.remove_many_spaces(tr.find_all("td")[0].text)
                name: str = clean_data.remove_many_spaces(tr.find_all("td")[1].text)
                classroom: str = clean_data.remove_many_spaces(
                    tr.find_all("td")[2].text
                )
                type_: str = clean_data.remove_many_spaces(tr.find_all("td")[3].text)
                teacher: str = clean_data.remove_many_spaces(tr.find_all("td")[4].text)

                shedule[date][time] = {
                    "name": name,
                    "classroom": classroom,
                    "type": type_,
                    "teacher": teacher,
                }

        return shedule

    def _get_teacher_schedule(self) -> dict:
        """Returns schedule for student

        :return: Schedule
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> schedule = lms._get_teacher_schedule()
        >>> # schedule
        >>> # {
        >>> #   "31.01.23, Tue": {
        >>> #       "09:55 - 11:40": {
        >>> #           "name": "Mathematics",
        >>> #           "Group": "it-21"
        >>> #           "classroom": "D-101"
        >>> #           "type_lesson": "lecture"
        >>> #       },
        >>> #   },
        >>> # }
        """

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        table: bs = soup.find("table", {"class": "table-list v-scrollable"})
        shedule: dict = {}

        for tr in table.find("tbody").find_all("tr"):
            if len(tr.find_all("td")) == 1:
                return shedule
            if tr.find("th"):
                date: str = clean_data.remove_many_spaces(tr.find("th").text)
                shedule[date] = {}
            else:
                time: str = clean_data.remove_many_spaces(tr.find_all("td")[0].text)
                name: str = clean_data.remove_many_spaces(tr.find_all("td")[1].text)
                group: str = clean_data.remove_many_spaces(tr.find_all("td")[2].text)
                classroom: str = clean_data.remove_many_spaces(
                    tr.find_all("td")[3].text
                )
                type_lesson: str = clean_data.remove_many_spaces(
                    tr.find_all("td")[4].text
                )

                shedule[date][time] = {
                    "name": name,
                    "group": group,
                    "classroom": classroom,
                    "type_lesson": type_lesson,
                }

        return shedule

    def get_news(self) -> list:
        """Returns news

        :return: News
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> news = lms.get_news()
        >>> # news
        >>> # [
        >>> #   {
        >>> #       "title": "Title",
        >>> #       "description": "Description",
        >>> #       "date": "Date",
        >>> #       "link": "Link",
        >>> #   },
        >>> # ]
        """

        soup: bs = SoupLms.get_soup_news(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        events_anons: bs = soup.find("div", {"class": "events-list rssNews"})

        news: list = []

        for event_anons in events_anons.find_all("div", {"class": "item"}):
            title: str = clean_data.remove_many_spaces(
                event_anons.find("h3").text
            )
            description: str = clean_data.remove_many_spaces(
                event_anons.find("div", {"class": "awrap"}).text
            )
            date: str = clean_data.remove_many_spaces(
                event_anons.find("div", {"class": "meta"}).text
            )
            link: str = event_anons.find("a", {"class": "more"})["href"]

            news.append(
                {
                    "title": title,
                    "description": description,
                    "date": date,
                    "link": link,
                }
            )

        return news

    def get_disciplines(self) -> list:
        """Returns disciplines

        :return: Disciplines
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> disciplines = lms.get_disciplines()
        >>> # disciplines
        >>> # [
        >>> #   {
        >>> #       "title": "Title",
        >>> #       "typeOfControl": "TypeOfControl",
        >>> #       "currentScore": "CurrentScore",
        >>> #       "finalGrade": "FinalGrade"
        >>> #   },
        >>> # ]
        """

        soup: bs = SoupLms.get_soup_disciplines(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        disciplines: list = []

        table = soup.find("tbody", {"class": "expanded"})

        for tr in table.find_all("tr"):
            if len(tr.find_all("td")) != 5:
                continue
            title: str = clean_data.remove_many_spaces(tr.find_all("td")[1].text)
            typeOfControl: str = clean_data.remove_many_spaces(
                tr.find_all("td")[2].text
            )
            currentScore: str = clean_data.remove_many_spaces(
                tr.find_all("td")[3].text
            )
            if currentScore == "": currentScore = "-"

            finalGrade: str = clean_data.remove_many_spaces(
                tr.find_all("td")[4].text
            )
            if finalGrade == "": finalGrade = "-"
            
            url: str = tr.find_all("td")[1].find("a")
            if url: url = "%s%s" % (URL, url["href"])
            else: url = "-"

            disciplines.append(
                {
                    "title": title,
                    "typeOfControl": typeOfControl,
                    "currentScore": currentScore,
                    "finalGrade": finalGrade,
                    "url": url
                }
            )
        
        return disciplines

    def get_pesonal_curators(self) -> list:
        """Returns personal curators

        :return: Personal curators
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> pesonal_curators = lms.get_pesonal_curators()
        >>> # pesonal_curators
        >>> # [
        >>> #   {
        >>> #       "name": "",
        >>> #       "phones": [],
        >>> #       "emails": []
        >>> #   },
        >>> # ]
        """

        if self.type_user not in ["student", "студент"]:
            raise UserIsNotStudentError("User is not student")

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        curator_main: bs = soup.find("div", {"id": "curatorMain"})
        curator_list: bs = curator_main.find("ul", {"class": "curatorList"})
        personal_curators: list = []

        if curator_list is None: return []

        for li in curator_list.find_all("li"):
            name: str = li.find("span", {"class": "curatorName"}).text
            phones: list = []
            emails: list = []

            phone_icons = li.find_all('i', {'class': ['icon-helpdesk']})
            email_icon = li.find('i', {'class': ['icon-mail']})

            for icon in phone_icons:
                phone = icon.find_next_sibling(string=True).strip()
                phones.append(phone)

            if email_icon:
                email_link = email_icon.find_next_sibling('a')
                email = email_link.get('href').replace('mailto:', '').strip()
                emails.append(email)

            personal_curators.append(
                {
                    "name": name,
                    "phones": phones,
                    "emails": emails
                }
            )

        return personal_curators

    def get_tutors(self) -> list:
        """Returns tutors

        :return: Tutors
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> tutors = lms.get_tutors()
        >>> # tutors
        >>> # [
        >>> #   {
        >>> #       "name": "",
        >>> #       "phones": [],
        >>> #       "emails": []
        >>> #   },
        >>> # ]
        """

        if self.type_user not in ["student", "студент"]:
            raise UserIsNotStudentError("User is not student")

        soup: bs = SoupLms.get_soup_schedule(
            session=self.session,
            language=self.language,
            cookies=self.cookies,
            proxies=self.proxy
        )

        curator_main: bs = soup.find("div", {"id": "curators"})
        curator_list: bs = curator_main.find("ul", {"class": "curatorList"})
        tutors: list = []

        if curator_list is None: return []

        for li in curator_list.find_all("li"):
            name: str = li.find("span", {"class": "curatorName"}).text
            phones: list = []
            emails: list = []

            phone_icons = li.find_all('i', {'class': ['icon-helpdesk']})
            email_icon = li.find('i', {'class': ['icon-mail']})

            for icon in phone_icons:
                phone = icon.find_next_sibling(string=True).strip()
                phones.append(phone)

            if email_icon:
                email_link = email_icon.find_next_sibling('a')
                email = email_link.get('href').replace('mailto:', '').strip()
                emails.append(email)

            tutors.append(
                {
                    "name": name,
                    "phones": phones,
                    "emails": emails
                }
            )

        return tutors

    def get_notify(self) -> list:
        """Returns notifications

        :return: Notifications
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> notify = lms.get_notify()
        >>> # notify
        >>> # [
        >>> #   {
        >>> #       "discipline": "Discipline",
        >>> #       "teacher": "Teacher",
        >>> #       "event": "Event",
        >>> #       "current_score": "Current_score",
        >>> #       "message": "Message"
        >>> #   },
        >>> # ]
        """

        amount_pages: int = SoupLms.get_amount_pages_notify(
            self.session, self.language, self.cookies, self.proxy
        )
        notify: list = []

        for page in range(1, amount_pages):
            soup: bs = SoupLms.get_soup_notify(
                session=self.session,
                language=self.language,
                cookies=self.cookies,
                proxies=self.proxy,
                page=page
            )

            table: bs = soup.find("table", {"class": "table-list dataTable"})

            for tr in table.find("tbody").find_all("tr"):
                if len(tr.find_all("td")) == 1:
                    return notify
                if tr.find_all("td")[4].text[-1] == "0":
                    continue
                discipline: str = tr.find_all("td")[0].text
                teacher: str = tr.find_all("td")[1].text
                event: str = tr.find_all("td")[2].text
                current_score: str = tr.find_all("td")[3].text
                message: str = tr.find_all("td")[4].text

                notify.append(
                    {
                        "discipline": discipline,
                        "teacher": teacher,
                        "event": event,
                        "current_score": current_score,
                        "message": message
                    }
                )

        return notify

    def get_notify_archive(self) -> list:
        """Returns notifications archive

        :return: Notifications archive
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> notify_archive = lms.get_notify_archive()
        >>> # notify_archive
        >>> # [
        >>> #   {
        >>> #       "discipline": "Discipline",
        >>> #       "teacher": "Teacher",
        >>> #       "event": "Event",
        >>> #       "current_score": "Current_score",
        >>> #       "message": "Message"
        >>> #   },
        >>> # ]
        """

        amount_pages: int = SoupLms.get_amount_pages_notify_archive(
            self.session, self.language, self.cookies, self.proxy
        )
        notify_archive: list = []

        for page in range(1, amount_pages):
            soup: bs = SoupLms.get_soup_notify_archive(
                session=self.session,
                language=self.language,
                cookies=self.cookies,
                proxies=self.proxy,
                page=page
            )

            table: bs = soup.find("table", {"class": "table-list dataTable"})

            for tr in table.find("tbody").find_all("tr"):
                if len(tr.find_all("td")) == 1:
                    return notify_archive
                if tr.find_all("td")[4].text[-1] == "0":
                    continue
                discipline: str = tr.find_all("td")[0].text
                teacher: str = tr.find_all("td")[1].text
                event: str = tr.find_all("td")[2].text
                current_score: str = tr.find_all("td")[3].text
                message: str = tr.find_all("td")[4].text

                notify_archive.append(
                    {
                        "discipline": discipline,
                        "teacher": teacher,
                        "event": event,
                        "current_score": current_score,
                        "message": message
                    }
                )

        return notify_archive

    def get_unread_messages(self) -> list:
        """Returns unread messages

        :return: unread messages
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> unread_messages = lms.get_unread_messages()
        >>> # unread_messages
        >>> # [
        >>> #   {
        >>> #       "sender_name": "Sender_name",
        >>> #       "subject": "Subject",
        >>> #       "date": "Date",
        >>> #       "url": "Url"
        >>> #   },
        >>> # ]
        """

        messages: list = []

        amount_pages: int = SoupLms.get_amount_pages_messages_unread(
            self.session, self.language, self.cookies, self.proxy
        )

        if amount_pages < 1:
            return messages

        for page in range(1, amount_pages):
            soup: bs = SoupLms.get_soup_messages_unread(
                session=self.session,
                language=self.language,
                cookies=self.cookies,
                proxies=self.proxy,
                page=page
            )

            table: bs = soup.find("table", {"class", "dataTable decorateTable table-list"})

            for tr in table.find("tbody").find_all("tr"):
                sender_name: str = clean_data.remove_many_spaces(
                    tr.find_all("td")[1].text
                )
                subject: str = clean_data.remove_many_spaces(
                    tr.find_all("td")[2].text
                )
                url: str = "%s%s" % (URL, tr.find_all("td")[2].find("a")["href"])
                date: str = clean_data.remove_many_spaces(
                    tr.find_all("td")[4].text
                )

                messages.append(
                    {
                        "sender_name": sender_name,
                        "subject": subject,
                        "date": date,
                        "url": url
                    }
                )

        return messages
    
    def get_marks(self) -> list:
        """Returns marks

        :return: marks
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> marks = lms.get_marks()
        >>> # marks
        >>> # [
        >>> #   {
        >>> #       "discipline": "Discipline",
        >>> #       "type_discipline": "Type_discipline",
        >>> #       "teacher": "Teacher",
        >>> #       "date_discipline": "Date_discipline",
        >>> #       "time_discipline": "Time_discipline",
        >>> #       "mark": "Mark",
        >>> #       "hours": "Hours"
        >>> #   },
        >>> # ]
        """

        soup: bs = SoupLms.get_soup_journal(
                session=self.session,
                language=self.language,
                cookies=self.cookies,
                proxies=self.proxy,
        )
        
        table: bs = soup.find("table", {"class": "table-list dataTable"})
        marks: list = []

        for tr in table.find_all("tr", {"id": "entryId"}):
            if len(tr.find_all("td")) == 1:
                return marks
            else:
                discipline: str = clean_data.remove_many_spaces(tr.find_all("td")[0].text)
                type_discipline: str = clean_data.remove_many_spaces(tr.find_all("td")[1].text)
                teacher: str = clean_data.remove_many_spaces(tr.find_all("td")[2].text)
                date_discipline: str = clean_data.remove_many_spaces(tr.find_all("td")[3].text)
                time_discipline: str = clean_data.remove_many_spaces(tr.find_all("td")[4].text)
                mark: str = clean_data.remove_many_spaces(tr.find_all("td")[5].text)
                hours: str = clean_data.remove_many_spaces(tr.find_all("td")[6].text)

                marks.append(
                    {
                        "discipline": discipline,
                        "type_discipline": type_discipline,
                        "teacher": teacher,
                        "date_discipline": date_discipline,
                        "time_discipline": time_discipline,
                        "mark": mark,
                        "hours": hours
                    }
                )

        return marks
    
    def get_events(self):
        """Returns event

        :return: event
        :rtype: list

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> events = lms.get_events()
        >>> # events
        >>> # [
        >>> #   {
        >>> #       "discipline": {
        >>> #               "current_grade": "Current_grade",
        >>> #               "events": [
        >>> #                           {
        >>> #                               "name": "Name",
        >>> #                               "access": "Access",
        >>> #                               "max_grade": "Max_grade",
        >>> #                               "result": "Result",
        >>> #                               "url": "Url"
        >>> #                           },
        >>> #               ]
        >>> #       },
        >>> #   },       
        >>> # ]
        """

        disciplines = self.get_disciplines()
        info_disciplines = []

        for discipline in disciplines:
            if discipline["url"] == "-":
                continue
            soup: bs = SoupLms.get_soup_events(
                session=self.session,
                language=self.language,
                cookies=self.cookies,
                proxies=self.proxy,
                url=discipline["url"]
            )

            table: bs = soup.find("table", {"class": "table-list"})
            events: list = []

            for tr in table.find("tbody").find_all("tr"):
                if len(tr.find_all("td")) == 1:
                    continue
                name: str = clean_data.remove_many_spaces(tr.find_all("td")[0].text)
                access: str = clean_data.remove_many_spaces(tr.find_all("td")[1].text)
                max_grade: str = clean_data.remove_many_spaces(tr.find_all("td")[2].text)
                result: str = clean_data.remove_many_spaces(tr.find_all("td")[3].text)
                if result == "": result = "-"
                url: str = tr.find_all("td")[0].find("a")
                if url: url = "%s%s" % (URL, url["href"])
                else: url = "-"

                events.append(
                    {
                        "name": name,
                        "access": access,
                        "max_grade": max_grade,
                        "result": result,
                        "url": url
                    }
                )
            
            current_grade = table.find("tfoot").find_all("td")

            info_disciplines.append(
                {
                    discipline["title"]: {
                        "current_grade": clean_data.remove_many_spaces(current_grade[-1].text), 
                        "events": events
                    },
                }
            )
        return info_disciplines
