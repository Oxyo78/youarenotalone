import csv
from website.models import City

with open('website/laposte_city.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    print(spamreader.count())
    for row in spamreader:
        # try:
        #     a = City.objects.create(cityName=row[0], postalCode=row[1], coordinateLng=row[2], coordinateLat=row[3])
        #     a.save()
        # except:
        #     continue
        pass