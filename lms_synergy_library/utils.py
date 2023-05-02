from requests import Response, Session
from bs4 import BeautifulSoup as bs
from constants import URL_EDUCATION, URL_LOGIN, URL_NEWS, URL_SCHEDULE, URLS_LANGUAGES


class clean_data:
    @staticmethod
    def remove_many_spaces(string):
        return " ".join(string.split())

class SoupLms:
    @staticmethod
    def get_soup_schedule(session, language, cookies) -> bs:
        """Returns soup schedule

        :param session: Session
        :param language: Language
        :param cookies: Cookies

        :type session: Session
        :type language: str
        :type cookies: dict

        :return: Soup schedule
        :rtype: bs4.BeautifulSoup
        """

        session.get(URLS_LANGUAGES[language], cookies=cookies)

        response: Response = session.get(URL_SCHEDULE, cookies=cookies)

        return bs(response.text, "html.parser")

    @staticmethod
    def get_soup_news(session, language, cookies) -> bs:
        """Returns soup news

        :param session: Session
        :param language: Language
        :param cookies: Cookies

        :type session: Session
        :type language: str
        :type cookies: dict

        :return: Soup news
        :rtype: bs4.BeautifulSoup
        """

        session.get(URLS_LANGUAGES[language], cookies=cookies)

        response: Response = session.get(URL_NEWS, cookies=cookies)

        return bs(response.text, "html.parser")

    @staticmethod
    def get_soup_disciplines(session, language, cookies) -> bs:
        """Returns soup discipline

        :param session: Session
        :param language: Language
        :param cookies: Cookies

        :type session: Session
        :type language: str
        :type cookies: dict

        :return: Soup discipline
        :rtype: bs4.BeautifulSoup
        """

        session.get(URLS_LANGUAGES[language], cookies=cookies)

        response: Response = session.get(URL_EDUCATION, cookies=cookies)

        return bs(response.text, "html.parser")
