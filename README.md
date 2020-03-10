# Hargreaves Lansdown Tracker

## Install the requirements

Install Python 3+

Install the requirements:

```bash
pip3 install -r requirements.txt
```

## Usage

```python
from hl import HargreavesLansdown

api = HargreavesLansdown("your username", "your password", "your secure number", "your date of birth (in DDMMYY format)")
api.login()

portfolio_values = list(api.get_values())
```
