from django.urls import path
from .views import HomeView, AllListView, NewListView, DoneListView, RejectedListView, StudentRequestDetailView, \
    LoginView, logout_view

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("all_list/", AllListView.as_view(), name="all_list"),
    path("new_list/", NewListView.as_view(), name="new_list"),
    path("done_list/", DoneListView.as_view(), name="done_list"),
    path("rejected_list/", RejectedListView.as_view(), name="rejected_list"),
    path("detail/<int:pk>/", StudentRequestDetailView.as_view(), name="detail_view"),

]
