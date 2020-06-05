from django.db.models import Max, Min, Avg
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import InSchoolPeople, OutSchoolPeople, Course, Award, Section


# Create your views here.


class InSchoolPeopleList(ListView):
    model = InSchoolPeople
    template_name = 'peopleList.html'

    def get_queryset(self):
        return self.model.objects.exclude(teach=None)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['student_list'] = self.model.objects.exclude(learn=None)
        context['max_cradit'] = context['student_list'].aggregate(Max('learn__credit'))['learn__credit__max']
        context['min_cradit'] = context['student_list'].aggregate(Min('learn__credit'))['learn__credit__min']
        context['avg_cradit'] = context['student_list'].aggregate(Avg('learn__credit'))['learn__credit__avg']
        return context


class InSchoolPeopleCreate(CreateView):
    model = InSchoolPeople
    template_name = 'peopleForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('InSchoolPeopleList')


class InSchoolPeopleUpdate(UpdateView):
    model = InSchoolPeople
    template_name = 'peopleForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('InSchoolPeopleList')


class OutSchoolPeopleList(ListView):
    model = OutSchoolPeople
    template_name = 'outpeopleList.html'


class OutSchoolPeopleCreate(CreateView):
    model = OutSchoolPeople
    template_name = 'outpeopleForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('OutSchoolPeopleList')


class OutSchoolPeopleUpdate(UpdateView):
    model = OutSchoolPeople
    template_name = 'outpeopleForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('OutSchoolPeopleList')


class CourseList(ListView):
    model = Course
    template_name = 'courseList.html'


class CourseCreate(CreateView):
    model = Course
    template_name = 'courseForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('CourseList')


class CourseUpdate(UpdateView):
    model = Course
    template_name = 'courseForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('CourseList')
