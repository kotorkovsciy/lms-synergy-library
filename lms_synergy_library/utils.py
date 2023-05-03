from requests import Response, Session
from bs4 import BeautifulSoup as bs
from constants import URL_EDUCATION, URL_NEWS, URL_SCHEDULE, URLS_LANGUAGES, URL_NOTIFY,\
     URL_NOTIFY_ARCHIVE
from exceptions import PageNotExist


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

    @staticmethod
    def get_soup_notify(session: Session, language: str, cookies: dict, proxies: dict, page: int = 1) -> bs:
        """Returns soup notifications

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies
        :param page: Page

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict
        :type page: int

        :return: Soup notifications
        :rtype: bs4.BeautifulSoup
        """

        if page < 1:
            raise PageNotExist("Page does not exist: %s?page=%d&pageSize=10" % (URL_NOTIFY, page))

        session.get(URLS_LANGUAGES[language], cookies=cookies, proxies=proxies)

        response: Response = session.get(
            "%s?page=%d&pageSize=10" % (URL_NOTIFY, page),
            cookies=cookies,
            proxies=proxies
        )

        return bs(response.text, "html.parser")

    @classmethod
    def get_amount_pages_notify(cls, session: Session, language: str, cookies: dict, proxies: dict) -> int:
        """Returns amount pages notify

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict

        :return: Amount pages notify
        :rtype: int
        """

        soup: bs = cls.get_soup_notify(
            session, language, cookies, proxies
        )

        paginator_links: bs = soup.select('.paginator a')

        if paginator_links:
            amount_pages: int = int(paginator_links[-2].text)
        else:
            amount_pages: int = 1

        return amount_pages

    @staticmethod
    def get_soup_notify_archive(session: Session, language: str, cookies: dict, proxies: dict, page: int = 1) -> bs:
        """Returns soup notifications archive

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies
        :param page: Page

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict
        :type page: int

        :return: Soup notifications archive
        :rtype: bs4.BeautifulSoup
        """
        if page < 1:
            raise PageNotExist("Page does not exist: %s?page=%d&pageSize=10" % (URL_NOTIFY_ARCHIVE, page))

        session.get(URLS_LANGUAGES[language], cookies=cookies, proxies=proxies)

        response: Response = session.get(
            "%s?page=%d&pageSize=10" % (URL_NOTIFY_ARCHIVE, page),
            cookies=cookies,
            proxies=proxies
        )

        return bs(response.text, "html.parser")

    @classmethod
    def get_amount_pages_notify_archive(cls, session: Session, language: str, cookies: dict, proxies: dict) -> int:
        """Returns amount pages notify archive

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict

        :return: Amount pages notify archive
        :rtype: int
        """

        soup: bs = cls.get_soup_notify_archive(
            session, language, cookies, proxies
        )

        paginator_links: bs = soup.select('.paginator a')

        if paginator_links:
            amount_pages: int = int(paginator_links[-2].text)
        else:
            amount_pages: int = 1

        return amount_pages
