# lms-synergy-library

This unofficial library is a collection of useful functions for the LMS Synergy platform.

## Installation

```bash
pip install lms-synergy-library
```

## Usage

```python
from lms_synergy_library import LMS

lms = LMS(login="demo", password="demo")

# verify
lms.verify()

# get amount messages
lms.get_amount_messages()

# get amount notifications
lms.get_amount_notifications()

# get information about user
lms.get_info()

# get shedule
lms.get_schedule()

# get news
lms.get_news()

# get disciplines
lms.get_disciplines()

# get amount unverified work
lms.get_amount_unverified_work()

# get pesonal curators
lms.get_pesonal_curators()

# get tutors
lms.get_tutors()

# get notifications
lms.get_notify()

# get notifications archive
lms.get_notify_archive()

# get unread messages
lms.get_unread_messages()

# get marks
lms.get_marks()

# get events
lms.get_events()

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- [@kotorkovsciy](https://www.github.com/kotorkovsciy)
