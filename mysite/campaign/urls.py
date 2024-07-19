from django.urls import path
from . import views

app_name = "campaign"

urlpatterns = [
    path("", views.CampaignList.as_view(), name="campaign-list"),
    path("<int:pk>/", views.CampaignDetailView.as_view(), name="campaign-detail"),
    path("create/", views.CreateCampaign.as_view(), name="campaign-create"),
    path("update/<int:pk>/", views.UpdateCampaign.as_view(), name="campaign-update"),
    path("delete/<int:pk>/", views.DeleteCampaign.as_view(), name="campaign-delete"),
]
