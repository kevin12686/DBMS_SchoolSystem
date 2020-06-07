from django.db import connection
from django.db.models import Max, Min, Avg
from django.apps import apps
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import InSchoolPeople, OutSchoolPeople, Course, Award, Section, SectionAttending


# Create your views here.


class InSchoolPeopleList(ListView):
    model = InSchoolPeople
    template_name = 'peopleList.html'

    def get_queryset(self):
        return self.model.objects.exclude(teach=None)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['student_list'] = self.model.objects.exclude(name__in=self.object_list.values('name'))
        context['max_height'] = context['student_list'].aggregate(Max('height'))['height__max']
        context['min_height'] = context['student_list'].aggregate(Min('height'))['height__min']
        context['avg_height'] = context['student_list'].aggregate(Avg('height'))['height__avg']
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


class InSchoolPeopleDelete(DeleteView):
    model = InSchoolPeople
    template_name = 'deleteConfirm.html'

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


class OutSchoolPeopleDelete(DeleteView):
    model = OutSchoolPeople
    template_name = 'deleteConfirm.html'

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


class CourseDelete(DeleteView):
    model = Course
    template_name = 'deleteConfirm.html'

    def get_success_url(self):
        return reverse('CourseList')


class AwardList(ListView):
    model = Award
    template_name = 'awardList.html'


class AwardCreate(CreateView):
    model = Award
    template_name = 'awardForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('AwardList')


class AwardUpdate(UpdateView):
    model = Award
    template_name = 'awardForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('AwardList')


class AwardDelete(DeleteView):
    model = Award
    template_name = 'deleteConfirm.html'

    def get_success_url(self):
        return reverse('AwardList')


class SectionList(ListView):
    model = Section
    template_name = 'sectionList.html'


class SectionCreate(CreateView):
    model = Section
    template_name = 'sectionForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('SectionList')


class SectionUpdate(UpdateView):
    model = Section
    template_name = 'sectionForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('SectionList')


class SectionDelete(DeleteView):
    model = Section
    template_name = 'deleteConfirm.html'

    def get_success_url(self):
        return reverse('SectionList')


class SectionAttendingList(ListView):
    model = SectionAttending
    template_name = 'attendList.html'


class SectionAttendingCreate(CreateView):
    model = SectionAttending
    template_name = 'attendForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('AttendList')


class SectionAttendingUpdate(UpdateView):
    model = SectionAttending
    template_name = 'attendForm.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('AttendList')


class SectionAttendingDelete(DeleteView):
    model = SectionAttending
    template_name = 'deleteConfirm.html'

    def get_success_url(self):
        return reverse('AttendList')


class SQLQuery(TemplateView):
    template_name = 'sqlQuery.html'

    def post(self, request, *args, **kwargs):
        query = request.POST.get('query', '')
        context = self.get_context_data(**kwargs)
        context['query'] = query
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            context['fields'] = [field[0] for field in cursor.description]
            context['results'] = cursor.fetchall()
        except Exception as e:
            context['fields'] = ['Error']
            context['results'] = [(str(e),)]
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = dict()
        for models in apps.get_app_config('school').get_models():
            context['models'][models._meta.db_table] = list()
            for field in models._meta.fields:
                context['models'][models._meta.db_table].append(field.name)
        return context
