from requests import Response, Session
from bs4 import BeautifulSoup as bs
from .constants import URL_EDUCATION, URL_NEWS, URL_SCHEDULE, URLS_LANGUAGES, URL_NOTIFY,\
     URL_NOTIFY_ARCHIVE, URL_MESSAGES_UNREAD, URL, URL_JOURNAL
from .exceptions import PageNotExist


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

    @staticmethod
    def get_amount_messages_from_soup(soup: bs, language: str) -> int:
        """Returns amount messages from soup

        :param soup: Soup
        :param language: Language

        :type soup: bs4.BeautifulSoup
        :param language: Language

        :return: Amount messages from soup
        :rtype: int
        """

        titles: dict = {
            "ru": "Личные сообщения",
            "en": "Private messages",
        }

        amount_messages: str = soup.find("a", title=titles[language])

        if amount_messages is None:
            return 0

        return int(clean_data.remove_many_spaces(amount_messages.text))

    @staticmethod
    def get_amount_notify_from_soup(soup: bs, language: str) -> int:
        """Returns amount notifications from soup

        :param soup: Soup
        :param language: Language

        :type soup: bs4.BeautifulSoup
        :param language: Language

        :return: Amount notifications from soup
        :rtype: int
        """

        titles: dict = {
            "ru": "Уведомления",
            "en": "Notifications",
        }

        amount_notifications: str = soup.find("a", title=titles[language])

        if amount_notifications is None:
            return 0

        return int(clean_data.remove_many_spaces(amount_notifications.text))

    @staticmethod
    def get_soup_messages_unread(session: Session, language: str, cookies: dict, proxies: dict, page: int = 1) -> bs:
        """Return soup unread messages

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict

        :return: Soup unread messages
        :rtype: bs4.BeautifulSoup
        """

        if page < 1:
            raise PageNotExist("Page does not exist: %s/page/%d" % (URL_MESSAGES_UNREAD, page))

        session.get(URLS_LANGUAGES[language], cookies=cookies, proxies=proxies)

        response: Response = session.get(
            "%s/page/%d" % (URL_MESSAGES_UNREAD, page),
            cookies=cookies,
            proxies=proxies
        )

        return bs(response.text, "html.parser")

    @classmethod
    def get_amount_pages_messages_unread(cls, session: Session, language: str, cookies: dict, proxies: dict) -> int:
        """Returns amount pages unread messages

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict

        :return: Amount pages unread messages
        :rtype: int
        """

        soup: bs = cls.get_soup_messages_unread(
            session, language, cookies, proxies
        )

        amount_msg: int = cls.get_amount_messages_from_soup(
            soup, language
        )

        if amount_msg < 1:
            return 0

        amount_pages: int = 1

        paginator_links: bs = soup.select('.paginator a')

        if not paginator_links:
            return 1

        next_link: str = "%s%s" % (URL, paginator_links[-1]["href"])
        end_link: str = "%sjavascript:void(0);" % URL

        while (next_link != end_link):
            amount_pages += 1

            response: Response = session.get(
                "%s%s" % (URL, paginator_links[-1]["href"]),
                cookies=cookies,
                proxies=proxies
            )
            soup = bs(response.content, 'html.parser')
            paginator_links: bs = soup.select('.paginator a')
            next_link = "%s%s" % (URL, paginator_links[-1]["href"])

        return amount_pages
    
    @staticmethod
    def get_soup_journal(session: Session, language: str, cookies: dict, proxies: dict) -> bs:
        """ Returns journal

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict

        :return: Journal page
        :rtype: bs4.BeautifulSoup
        """
        session.get(URLS_LANGUAGES[language], cookies=cookies, proxies=proxies)

        response: Response = session.get(URL_JOURNAL, cookies=cookies, proxies=proxies)

        return bs(response.text, "html.parser")
    
    @staticmethod
    def get_soup_events(session: Session, language: str, cookies: dict, proxies: dict, url: str) -> bs:
        """ Returns soup events

        :param session: Session
        :param language: Language
        :param cookies: Cookies
        :param proxies: Proxies
        :param url: Url

        :type session: Session
        :type language: str
        :type cookies: dict
        :type proxies: dict
        :type url: str

        :return: Soup events
        :rtype: bs4.BeautifulSoup
        """
        
        session.get(URLS_LANGUAGES[language], cookies=cookies, proxies=proxies)

        response: Response = session.get(url, cookies=cookies, proxies=proxies)

        return bs(response.text, "html.parser")
