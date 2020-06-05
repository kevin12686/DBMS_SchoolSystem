from django.urls import path
from .views import (InSchoolPeopleList,
                    InSchoolPeopleCreate,
                    InSchoolPeopleUpdate,
                    OutSchoolPeopleList,
                    OutSchoolPeopleCreate,
                    OutSchoolPeopleUpdate,
                    CourseList,
                    CourseCreate,
                    CourseUpdate, )

urlpatterns = [
    path('', InSchoolPeopleList.as_view(), name='InSchoolPeopleList'),
    path('inSchool/', InSchoolPeopleList.as_view(), name='InSchoolPeopleList'),
    path('inSchool/create/', InSchoolPeopleCreate.as_view(), name='InSchoolPeopleCreate'),
    path('inSchool/update/<pk>/', InSchoolPeopleUpdate.as_view(), name='InSchoolPeopleUpdate'),
    path('outSchool/', OutSchoolPeopleList.as_view(), name='OutSchoolPeopleList'),
    path('outSchool/create/', OutSchoolPeopleCreate.as_view(), name='OutSchoolPeopleCreate'),
    path('outSchool/update/<pk>/', OutSchoolPeopleUpdate.as_view(), name='OutSchoolPeopleUpdate'),
    path('course/', CourseList.as_view(), name='CourseList'),
    path('course/create/', CourseCreate.as_view(), name='CourseCreate'),
    path('course/update/<pk>/', CourseUpdate.as_view(), name='CourseUpdate'),
]
