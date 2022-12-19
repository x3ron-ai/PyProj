class ProjectExceptions:
	class AuthError:
		class InvalidLogin(Exception):
			def __init__(self, text):
				self.txt = text
		class InvalidPassword(Exception):
			def __init__(self, text):
				self.txt = text