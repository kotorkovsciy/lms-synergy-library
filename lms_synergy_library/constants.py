from typing import Final


URL: Final[str] = "https://lms.synergy.ru"
URL_LOGIN: Final[str] = "%s/user/login" % URL
URL_SCHEDULE: Final[str] = "%s/schedule/academ" % URL
URL_NEWS: Final[str] = "%s/announce" % URL
URL_EDUCATION: Final[str] = "%s/student/up" % URL
URL_NOTIFY: Final[str] = "%s/student/notifications" % URL
URL_NOTIFY_ARCHIVE: Final[str] = "%s/archive" % URL_NOTIFY
URLS_LANGUAGES: Final[dict] = {
        "ru": "%s/user/lng/1" % URL,
        "en": "%s/user/lng/2" % URL,
}
