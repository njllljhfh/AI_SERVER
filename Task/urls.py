from django.urls import re_path

from Task.views import MyTest, Algorithm1, Algorithm2, Algorithm3

urlpatterns = [
    re_path(r"^myTest$", MyTest.as_view(), name="myTest"),
    re_path(r"^algorithm1$", Algorithm1.as_view(), name="algorithm1"),
    re_path(r"^algorithm2$", Algorithm2.as_view(), name="algorithm2"),
    re_path(r"^algorithm3$", Algorithm3.as_view(), name="algorithm3"),
]
