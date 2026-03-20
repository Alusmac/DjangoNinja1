from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """Student model
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    """Course model
    """
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Enrollment(models.Model):
    """Enrollment model
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")

    class Meta:
        unique_together = ("student", "course")


class Grade(models.Model):
    """Grade model
    """
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name="grade")
    score = models.FloatField()
