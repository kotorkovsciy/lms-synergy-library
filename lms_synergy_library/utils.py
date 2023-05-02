from requests import Response, Session
from bs4 import BeautifulSoup as bs
from constants import URL_EDUCATION, URL_NEWS, URL_SCHEDULE, URLS_LANGUAGES


class clean_data:
    @staticmethod
    def remove_many_spaces(string):
        return " ".join(string.split())

class SoupLms:
    @staticmethod
    def get_soup_schedule(session: Session, language: str, cookies: dict, proxies: dict) -> bs:
        """Returns soup schedule

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict

        :return: Soup schedule
        :rtype: bs4.BeautifulSoup
        """

        session.get(URLS_LANGUAGES[language], cookies=cookies, proxies=proxies)

        response: Response = session.get(URL_SCHEDULE, cookies=cookies, proxies=proxies)

        return bs(response.text, "html.parser")

    @staticmethod
    def get_soup_news(session: Session, language: str, cookies: dict, proxies: dict) -> bs:
        """Returns soup news

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict

        :return: Soup news
        :rtype: bs4.BeautifulSoup
        """

        session.get(URLS_LANGUAGES[language], cookies=cookies, proxies=proxies)

        response: Response = session.get(URL_NEWS, cookies=cookies, proxies=proxies)

        return bs(response.text, "html.parser")

    @staticmethod
    def get_soup_disciplines(session: Session, language: str, cookies: dict, proxies: dict) -> bs:
        """Returns soup discipline

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict

        :return: Soup discipline
        :rtype: bs4.BeautifulSoup
        """

        session.get(URLS_LANGUAGES[language], cookies=cookies, proxies=proxies)

        response: Response = session.get(URL_EDUCATION, cookies=cookies, proxies=proxies)

        return bs(response.text, "html.parser")
