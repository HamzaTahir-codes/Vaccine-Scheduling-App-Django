from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from vaccine.models import Vaccine
from campaign.models import Campaign, Slot
from .models import Vaccination
from .forms import VaccinationForm
from django.utils import timezone
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from .utils import generate_pdf


class ChooseVaccine(LoginRequiredMixin, generic.ListView):
    model = Vaccine
    template_name = "vaccination/choose-vaccine.html"
    paginate_by = 10    
    ordering = ["name"]

class ChooseCampaign(LoginRequiredMixin, generic.ListView):
    model = Campaign
    template_name = "vaccination/choose-campaign.html"
    paginate_by = 10
    ordering = ["start_date"]

    def get_queryset(self):
        return super().get_queryset().filter(vaccine = self.kwargs["vaccine_id"])
    
class ChooseSlot(LoginRequiredMixin, generic.ListView):
    model = Slot
    template_name = "vaccination/choose-slot.html"
    paginate_by = 10
    ordering = ["date"]

    def get_queryset(self):
        return super().get_queryset().filter(campaign = self.kwargs["campaign_id"], date__gte = timezone.now())
    
class ConfirmVaccination(View):
    form_class = VaccinationForm

    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(id = self.kwargs["campaign_id"])
        slot = Slot.objects.get(id = self.kwargs["slot_id"])
        form = self.form_class(initial={
            "patient" : request.user,
            "campaign" : campaign,
            "slot" : slot,
        })
        context = {
            "patient" : request.user,
            "campaign" : campaign,
            "slot" : slot,
            "form" : form,
        }
        return render(request, "vaccination/confirm-vaccination.html", context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            is_reserved = Slot.reserve_vaccine(self.kwargs["campaign_id"], self.kwargs["slot_id"])
            if is_reserved:
                form.save()
                return HttpResponse("Your Vaccination has been Scheduled!")
            return HttpResponseBadRequest("Your Vaccination can't be Scheduled at this moment!")
        return HttpResponseBadRequest("Please Enter Valuid Data!")

class VaccinationList(LoginRequiredMixin, generic.ListView):
    model = Vaccination
    template_name = "vaccination/vaccination-list.html"
    paginate_by = 10
    ordering = ["id"]

    def get_queryset(self):
        return super().get_queryset().filter(patient = self.request.user)
    
class VaccinationDetail(LoginRequiredMixin, generic.DetailView):
    model = Vaccination
    template_name = "vaccination/vaccination-detail.html"

def appointment_letter(request, vaccination_id):
    vaccination = Vaccination.objects.get(id = vaccination_id)
    context = {
        "pdf_title" : f"{vaccination.patient.get_full_name()} | Appointment Letter",
        "date" : str(timezone.now()),
        "title" : "Appointment Letter!",
        "subtitle" : "To Whom It May Concern",
        "content" : f"This is to inform that the {vaccination.campaign.vaccine.name} Vaccination of Mr/Mrs {vaccination.patient.get_full_name()} is scheduled on {vaccination.slot.date}.",
    }
    return generate_pdf(context)

def vaccination_certificate(request, vaccination_id):
    vaccination = Vaccination.objects.get(id = vaccination_id)
    if vaccination.is_vaccinated:
        context = {
            "pdf_title" : f"{vaccination.patient.get_full_name()} | Vaccination Certificate",
            "date" : str(timezone.now()),
            "title" : "Vaccination Certificate!",
            "subtitle" : "To Whom It May Concern",
            "content" : f"This is to certify that Mr./Mrs. {vaccination.patient.get_full_name()} has successfully taken {vaccination.campaign.vaccine.name} on {vaccination.date}. The vaccination was scheduled on {vaccination.slot.date} {vaccination.slot.start_time} at {vaccination.campaign.center.name}.",
        }
        return generate_pdf(context)
    return HttpResponseBadRequest("User not Vaccinated!")

