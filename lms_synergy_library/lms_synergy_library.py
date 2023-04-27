from requests import Response, Session
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from utils import clean_data
import typing


class LMS:
    _URL: typing.Final[str] = "https://lms.synergy.ru"
    _URL_LOGIN: typing.Final[str] = "%s/user/login" % _URL
    _URL_SCHEDULE: typing.Final[str] = "%s/schedule/academ" % _URL
    _URL_NEWS: typing.Final[str] = "%s/announce" % _URL
    _URL_EDUCATION: typing.Final[str] = "%s/student/up" % _URL
    _URLS_LANGUAGES: typing.Final[dict] = {
        "ru": "%s/user/lng/1" % _URL,
        "en": "%s/user/lng/2" % _URL,
    }

    session: Session = None

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

        if language not in self._URLS_LANGUAGES:
            raise ValueError("language not found")
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
        self.session.post(self._URL_LOGIN, data=data, proxies=proxies)
        self.session.get(self._URLS_LANGUAGES[self.language], proxies=proxies)

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

    def _get_soup_schedule(self) -> bs:
        """Returns soup schedule

        :return: Soup schedule
        :rtype: bs4.BeautifulSoup

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> soup = lms._get_soup_schedule()
        >>> clean_data.remove_many_spaces(soup.find("div", {"class": "user-name"}).text)
        'Student Demonstratsionnyiy'
        """

        self.session.get(self._URLS_LANGUAGES[self.language], cookies=self.cookies)

        response: Response = self.session.get(self._URL_SCHEDULE, cookies=self.cookies)

        return bs(response.text, "html.parser")

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

        soup: bs = self._get_soup_schedule()

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

        soup: bs = self._get_soup_schedule()

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

        titles: dict = {
            "ru": "Личные сообщения",
            "en": "Private messages",
        }

        soup: bs = self._get_soup_schedule()

        amount_messages: str = soup.find("a", title=titles[self.language])

        if amount_messages is None:
            return 0

        return int(clean_data.remove_many_spaces(amount_messages.text))

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

        titles: dict = {
            "ru": "Уведомления",
            "en": "Notifications",
        }

        soup: bs = self._get_soup_schedule()

        amount_notifications: str = soup.find("a", title=titles[self.language])

        if amount_notifications is None:
            return 0

        return int(clean_data.remove_many_spaces(amount_notifications.text))

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

        soup: bs = self._get_soup_schedule()

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

    def _get_soup_news(self) -> bs:
        """Returns soup news

        :return: Soup news
        :rtype: bs4.BeautifulSoup

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> soup = lms._get_soup_news()
        >>> clean_data.remove_many_spaces(soup.find("div", {"class": "user-name"}).text)
        'Student Demonstratsionnyiy'
        """

        self.session.get(self._URLS_LANGUAGES[self.language], cookies=self.cookies)

        response: Response = self.session.get(self._URL_NEWS, cookies=self.cookies)

        return bs(response.text, "html.parser")

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

        soup: bs = self._get_soup_news()

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

    def get_soup_disciplines(self) -> bs:
        """Returns soup discipline

        :return: Soup discipline
        :rtype: bs4.BeautifulSoup

        :Example:

        >>> from lms_synergy_library import LMS
        >>> lms = LMS(login="demo", password="demo")
        >>> soup = lms.get_soup_disciplines()
        >>> clean_data.remove_many_spaces(soup.find("div", {"class": "user-name"}).text)
        'Student Demonstratsionnyiy'
        """

        self.session.get(self._URLS_LANGUAGES[self.language], cookies=self.cookies)

        response: Response = self.session.get(self._URL_EDUCATION, cookies=self.cookies)

        return bs(response.text, "html.parser")

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

        soup: bs = self.get_soup_disciplines()

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

            disciplines.append(
                {
                    "title": title,
                    "typeOfControl": typeOfControl,
                    "currentScore": currentScore,
                    "finalGrade": finalGrade
                }
            )
        
        return disciplines


if __name__ == "__main__":
    import doctest

    doctest.testmod()
