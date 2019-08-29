from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Classroom(models.Model):
	teacher = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.PositiveSmallIntegerField()

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})

	def __str__(self):
		return self.name

class Student(models.Model):
	MALE = 'M'
	FEMALE = 'F'
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	date_of_birth = models.DateField()
	GENDER_CHOICES = [
		(MALE,'Male'),
		(FEMALE, 'Female')
	]
	gender = models.CharField(
		max_length=1,
		choices=GENDER_CHOICES,
		default=MALE,
	)
	exam_grade = models.PositiveSmallIntegerField()
	classroom = models.ForeignKey(Classroom, default=1, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'student_id':self.id})