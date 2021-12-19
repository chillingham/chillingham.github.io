from decouple import Config


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aagroupspw@gmail.com'
EMAIL_HOST_PASSWORD = Config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
