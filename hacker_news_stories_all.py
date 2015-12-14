import urllib2
import json
import datetime
import time
import pytz
import hacker_news

# Set up database connection settings and other parameters
ts = str(int(time.time()))
hitsPerPage = 1000

schema = "CREATE TABLE hn_submissions (objectID INTEGER PRIMARY KEY, title varchar, url varchar, num_points int, num_comments int, author varchar, created_at DATETIME);"

db = init_db('hn.sqlite3', schema)
db.text_factory = str

cur = db.cursor()

num_processed = 0

while True:
	try:
		# Retrieve HN submissions from the Algolia API; finds all submissions before timestamp of last known submission time
		url = 'https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=%s&numericFilters=created_at_i<%s' % (hitsPerPage, ts)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)

		data = json.loads(response.read())
		submissions = data['hits']
		ts = submissions[-1 + len(submissions)]['created_at_i']

		for submission in submissions:

			# make sure we remove smartquotes/other unicode from title
			title = submission['title'].translate(dict.fromkeys([0x201c, 0x201d, 0x2011, 0x2013, 0x2014, 0x2018, 0x2019, 0x2026, 0x2032])).encode('utf-8')

			# EST timestamp since USA activity reflects majority of HN activity
			created_at = datetime.datetime.fromtimestamp(int(submission['created_at_i']), tz=pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S')


			SQL = "INSERT INTO hn_submissions (objectID, title, url, num_points, num_comments, author, created_at) VALUES (?,?,?,?,?,?,?)"
			insert_data = (int(submission['objectID']), title, submission['url'], submission['points'], submission['num_comments'], submission['author'], created_at)

			try:
				cur.execute(SQL, insert_data)
				db.commit()

			except Exception, e:
				print insert_data
				print e

		# If there are no more HN stories, we're done!
		if (data["nbHits"] < hitsPerPage):
			break

		num_processed += hitsPerPage

		if num_processed % 100000 == 0:
			# write to console periodically to make sure everything's working
			print "%s HN Posts Processed: %s" % (num_processed, datetime.datetime.now())

		# make sure we stay within API limits
		time.sleep(3600/10000)

	except Exception, e:
		print e

db.close()
