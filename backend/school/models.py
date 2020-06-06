from django.db import models
from django.db.models import Sum


# Create your models here.

class OutSchoolPeople(models.Model):
    name = models.CharField(max_length=50,
                            null=False,
                            blank=False,
                            verbose_name='姓名')
    age = models.PositiveSmallIntegerField(null=False,
                                           blank=False,
                                           verbose_name='年齡')

    def __str__(self):
        return self.name


class InSchoolPeople(models.Model):
    name = models.CharField(max_length=50,
                            null=False,
                            blank=False,
                            verbose_name='姓名')
    height = models.PositiveSmallIntegerField(null=False,
                                              blank=False,
                                              verbose_name='身高')

    def total_credits(self):
        return self.learn.all().aggregate(Sum('credit'))['credit__sum']

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50,
                            null=False,
                            blank=False,
                            verbose_name='名稱')
    credit = models.PositiveSmallIntegerField(null=False,
                                              blank=False,
                                              default=0,
                                              verbose_name='學分')
    instructor = models.ForeignKey(InSchoolPeople,
                                   null=False,
                                   blank=False,
                                   on_delete=models.CASCADE,
                                   related_name='teach',
                                   verbose_name='講師')
    student = models.ManyToManyField(InSchoolPeople,
                                     blank=False,
                                     related_name='learn',
                                     verbose_name='學生')

    def student_number(self):
        return self.student.all().count()

    def __str__(self):
        return '{} (講師: {})'.format(self.name, self.instructor.name)


class Award(models.Model):
    name = models.CharField(max_length=50,
                            null=False,
                            blank=False,
                            verbose_name='名稱')
    prize = models.PositiveIntegerField(null=False,
                                        blank=False,
                                        verbose_name='獎金')

    owner = models.ForeignKey(InSchoolPeople,
                              null=False,
                              blank=False,
                              on_delete=models.CASCADE,
                              related_name='reward',
                              verbose_name='得獎者')

    def __str__(self):
        return '{} (獎金: {})}'.format(self.name, self.prize)


class Section(models.Model):
    course = models.ForeignKey(Course,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE,
                               related_name='have',
                               verbose_name='課程')
    date = models.DateField(null=False,
                            blank=False,
                            auto_now=False,
                            auto_now_add=False,
                            verbose_name='日期')
    memo = models.CharField(max_length=255,
                            null=False,
                            blank=True,
                            verbose_name='備註')

    def __str__(self):
        return '{} (日期: {})'.format(self.course.name, str(self.date))


class SectionAttending(models.Model):
    section = models.ForeignKey(Section,
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                related_name='record',
                                verbose_name='課堂')
    inSchool = models.ManyToManyField(InSchoolPeople,
                                      blank=True,
                                      related_name='attend',
                                      verbose_name='學生上課')
    outSchool = models.ManyToManyField(OutSchoolPeople,
                                       blank=True,
                                       related_name='attend',
                                       verbose_name='校外旁聽')

    def total_in_stu(self):
        return self.inSchool.all().count()

    def total_out_stu(self):
        return self.outSchool.all().count()
