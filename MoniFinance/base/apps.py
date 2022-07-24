from django.apps import AppConfig
import os

class BaseConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'base'

	def ready(self):
		#Código para as tarefas não executarem duas vezes
		run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE') 
		if run_once is not None:
			return
		os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True' 

		#Setando tarefas periodicas
		from . import tasks
		tasks.start()