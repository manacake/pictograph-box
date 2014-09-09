#!/usr/bin/env python
from fabric.api import local

def deploy():
	'''Deploys the latest version to Heroku'''

	# Push changes to master
	local('git push origin master')

	# Push changes to Heroku
	local('git push heroku master')

	# Run migrations on Heroku
	local('heroku run python manage.py migrate')