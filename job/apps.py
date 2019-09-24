from django.apps import AppConfig


class JobConfig(AppConfig):
    name = 'job'

    def ready(self):
        print('Job App Ready')
        import job.signals