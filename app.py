from Crawler import TwitterCrawler

account = {'username': 'YOUR_USERNAME',
           'password': 'YOUR_PASSWORD', 'email': 'YOUR_EMAIL'}

crawler = TwitterCrawler(account)

df = crawler.get_followers('IvePetThatDog')
df.to_csv('crawled data/IvePetThatDog.csv', index=False)
