from django.db import models


class Job(models.Model):
    title = models.TextField()
    url = models.TextField()
    company_name = models.TextField()
    city = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    employment = models.TextField()
    prog_lang = models.TextField()
    skills = models.TextField()
    data_bases = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title