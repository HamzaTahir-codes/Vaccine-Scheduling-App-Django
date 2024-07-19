from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Campaign, Slot
from vaccination.models import Vaccination
from .forms import CampaignForm, SlotForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class CampaignList(LoginRequiredMixin, generic.ListView):
    model =  Campaign
    template_name = "campaign/campaign-list.html"
    paginate_by = 10
    ordering = ["-id"]

class CampaignDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaign
    template_name = "campaign/campaign-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registration"] = Vaccination.objects.filter(campaign = self.kwargs["pk"]).count()
        return context
    
class CreateCampaign(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaign/campaign-create.html"
    permission_required = ("campaign.add_campaign",)
    success_message = "Campaign Created Successfully"
    success_url = reverse_lazy("campaign:campaign-list")

class UpdateCampaign(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaign/campaign-update.html"
    permission_required = ("campaign.change_campaign",)
    success_message = "Campaign Updated Successfully!"
    success_url = reverse_lazy("campaign:campaign-list")

class DeleteCampaign(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Campaign
    template_name = "campaign/campaign-delete.html"
    permission_required = ("campaign.delete_campaign",)
    success_message = "Campaign Deleted Successfully!"
    success_url = reverse_lazy("campaign:campaign-list")


""" SLOTS SECTION """

class SlotList(LoginRequiredMixin, generic.ListView):
    model = Slot
    template_name = "campaign/slot-list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Slot.objects.filter(campaign = self.kwargs["campaign_id"])
        return queryset
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["campaign_id"] = self.kwargs["campaign_id"]
        return context
    
class SlotDetail(LoginRequiredMixin, generic.DetailView):
    model = Slot
    template_name = "campaign/slot-detail.html"

class SlotCreate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Slot
    form_class = SlotForm
    template_name = "campaign/slot-create.html"
    permission_required = ("campaign.add_slot",)
    success_message = "Slot Created Successfully!"

    def get_success_url(self):
        return reverse_lazy("campaign:slot-list", kwargs = {"campaign_id": self.kwargs["campaign_id"]})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"] 
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        initial["campaign"] = Campaign.objects.get(id = self.kwargs["campaign_id"])
        return initial

class SlotUpdate(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Slot
    form_class = SlotForm
    template_name = "campaign/slot-update.html"
    permission_required = ("campaign.change_slot",)
    success_message = "Slot Updated Successfully!"

    def get_success_url(self) -> str:
        return reverse_lazy("campaign:slot-list", kwargs = {"campaign_id": self.kwargs["campaign_id"]})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"] 
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        initial["campaign"] = Campaign.objects.get(id = self.kwargs["campaign_id"])
        return initial
    
class SlotDelete(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Slot
    template_name = "campaign/slot-delete.html"
    permission_required = ("campaign.delete_slot",)
    success_message = "Slot Deletion Successfull!"

    def get_success_url(self):
        return reverse_lazy("campaign:slot-list", kwargs = {"campaign_id": self.get_object().campaign.id})