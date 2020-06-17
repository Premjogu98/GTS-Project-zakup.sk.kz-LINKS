import dateparser
from datetime import datetime
Due_date = dateparser.parse('12.апреля.2020')
date_time = Due_date.strftime("%Y-%m-%d")
print("date and time:",date_time)