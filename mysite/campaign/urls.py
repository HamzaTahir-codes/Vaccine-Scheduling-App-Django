from django.urls import path
from . import views

app_name = "campaign"

urlpatterns = [
    path("", views.CampaignList.as_view(), name="campaign-list"),
    path("<int:pk>/", views.CampaignDetailView.as_view(), name="campaign-detail"),
    path("create/", views.CreateCampaign.as_view(), name="campaign-create"),
    path("update/<int:pk>/", views.UpdateCampaign.as_view(), name="campaign-update"),
    path("delete/<int:pk>/", views.DeleteCampaign.as_view(), name="campaign-delete"),
    path("<int:campaign_id>/slot/", views.SlotList.as_view(), name="slot-list"),
    path("slot/<int:pk>/", views.SlotDetail.as_view(), name="slot-detail"),
    path("<int:campaign_id>/slot/create/", views.SlotCreate.as_view(), name="slot-create"),
    path("<int:campaign_id>/slot/update/<int:pk>/", views.SlotUpdate.as_view(), name="slot-update"),
    path("slot/delete/<int:pk>/", views.SlotDelete.as_view(), name="slot-delete"),
]
