#sett	# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mkm+covmxb8_qvn^lc5jo0t5s#bj8!r=sy#v+cpmy*ol+pdl8w'

'''
CROWDCAFE = {
'app_token' : "bf4df1710484a930055ccfbbae5b06b4ff69845e",
'user_token' : "f77b9b34f55f02b5c21069c22cb611707e10d9b7",
'base_url' : "http://localhost/",
'api_url' : "http://localhost/api/"
}
'''

CROWDCAFE = {
'app_token' : "e54d11315bad440c31b38d489fdee9be45ac84cf",
'user_token' : "5b046e5b931031dd613f8f0cdf20bbf4cd4004ed",
'base_url' : "http://crowdcafe.io/",
'api_url' : "http://crowdcafe.io/api/",
'job_id' : 8
}

DROPBOX_APP_ID = 'jntt60e8dkk2zez'
DROPBOX_API_SECRET = '5uzov1jvxg44hro'

DROPBOX_USER_SECRET = 'u1nyc1a1jh0omei'
DROPBOX_USER_TOKEN = 'p6630w0yihdkih30'
#DROPBOX_FOLDER_NAME = 'ROCKPEARL_CROWDCAFE_JUDGEMENTS'
DROPBOX_FOLDER_NAME = 'ROCKPEARL_CROWDCAFE_JUDGEMENTS_TEST'

# AMAZON AWS CREDENTIALS------------------------------------------------------
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = 'AKIAJOHNS6D3IQDWRBGA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'https://s3-eu-west-1.amazonaws.com/'
AWS_STORAGE_BUCKET_NAME = 'crowdcrop'
# -----------------------------------------------------------------------------

# EMAILS
# -----------------------------------------------------------------------------
# TODO: fix the key when in production with one that can be used only by the ip of the server
MANDRILL_API_KEY = 'tp33mCmGNGgbfq8Se6oJtw'
EMAIL_HOST_PASSWORD = MANDRILL_API_KEY
EMAIL_HOST_USER = 'pavel@crowdcafe.io'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
SERVER_EMAIL = 'Rockpearl Error <error@crowdcafe.io>'
