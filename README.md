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

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- [@kotorkovsciy](https://www.github.com/kotorkovsciy)
