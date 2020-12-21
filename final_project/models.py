from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Group(models.Model):
    """Создание модели группы"""
    name = models.CharField(max_length=10)
    course = models.IntegerField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Создание модели пользователя"""
    middle_name = models.CharField(max_length=150, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.username + ' ' + self.last_name + ' ' + self.first_name


class Subject(models.Model):
    """Создание модели предмета"""
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Exam(models.Model):
    """Создание модели экзамена"""
    datetime = models.DateTimeField()
    classroom = models.CharField(max_length=10)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.__str__() + ' ' + self.group.name


class Mark(models.Model):
    """Создание модели отметки"""
    mark = models.IntegerField()
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam.__str__() + ' ' + self.student.__str__()


class GroupSubjectTeacher(models.Model):
    """Создание модели соответствия предметов, групп и преподавателей"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
