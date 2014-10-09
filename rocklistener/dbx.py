from models import DropboxUser
from social_auth.models import UserSocialAuth
from dropbox import client, session
from django.conf import settings


# class for managing dropbox operations: 
class Dbx:
	def __init__(self, uid):
		self.dropbox_user = DropboxUser.objects.get_or_create(uid = uid)
		
		social_user = UserSocialAuth.objects.get(uid=uid, provider = 'dropbox')
		secret = social_user.tokens['access_token'].split('&')[0].split('=')[1]
		token = social_user.tokens['access_token'].split('&')[1].split('=')[1]

		sess = session.DropboxSession(settings.DROPBOX_APP_ID, settings.DROPBOX_API_SECRET, 'dropbox')
		sess.set_token(token,secret)

		self.client = client.DropboxClient(sess)
	# manage webhook requests from dropbox
	def listen(self):
		return True
	# check updates (files and folders) for a specific user
	def checkUpdates(self):
		has_more = True
		while has_more:
			result = self.client.delta(self.dropbox_user.cursor)
			for path, metadata in result['entries']:
				# Ignore deleted files, folders, and non-markdown files
				if (metadata is None or metadata['is_dir'] or not path.endswith('.jpg')):
					continue

				# Convert to Markdown and store as <basename>.html
				html = markdown(client.get_file(path).read())
				client.put_file(path[:-3] + '.html', html, overwrite=True)
			# Update cursor
			self.dropbox_user.cursor = result['cursor']
			self.dropbox_user.save()
			# Repeat only if there's more to do
			has_more = result['has_more']

	# upload a new file to a specific folder
	def uploadFile(self, file):
		return True
	# rename folder
	def renameFolder(self, path, name):
		return True