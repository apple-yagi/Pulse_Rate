import logging
import os, sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import io
import pathlib
import numpy as np

from .analysis import *

from scipy.fftpack import fft
from scipy import signal

import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File

from .models import Pulse_Rate

from .forms import InquiryForm, PulseRateCreateForm, PulseRateFilterForm

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('pulse_rate:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'send message')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class PulseRateListView(LoginRequiredMixin, generic.ListView):
    model = Pulse_Rate
    template_name = 'pulse_rate_list.html'
    paginate_by = 5

    def get_queryset(self):
        pulse_rates = Pulse_Rate.objects.filter(user=self.request.user).order_by('-created_at')
        return pulse_rates


class PulseRateDetailView(LoginRequiredMixin, generic.DetailView):
    model = Pulse_Rate
    template_name = 'pulse_rate_detail.html'


class PulseRateCreateView(LoginRequiredMixin, generic.CreateView):
    model = Pulse_Rate
    template_name = 'pulse_rate_create.html'
    form_class = PulseRateCreateForm
    success_url = reverse_lazy('pulse_rate:pulse_rate_list')

    def form_valid(self, form):
        pulse_rate = form.save(commit=False)
        pulse_rate.user = self.request.user
        pulse_rate.save()
        messages.success(self.request, 'データを登録しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "データの登録に失敗しました")
        return super().form_invalid(form)


class PulseRateUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Pulse_Rate
    template_name = 'pulse_rate_update.html'
    form_class = PulseRateCreateForm

    def get_success_url(self):
        return reverse_lazy('pulse_rate:pulse_rate_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'データを更新しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'データの更新に失敗しました')
        return super().form_invalid(form)


class PulseRateDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Pulse_Rate
    template_name = 'pulse_rate_delete.html'
    success_url = reverse_lazy('pulse_rate:pulse_rate_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "データを削除しました")
        return super().delete(request, *args, **kwargs)


class PulseRateAnalysisView(LoginRequiredMixin, generic.DetailView, generic.UpdateView):
    model = Pulse_Rate
    template_name = 'pulse_rate_analysis.html'
    form_class = PulseRateFilterForm

    def get_success_url(self):
        return reverse_lazy('pulse_rate:pulse_rate_analysis', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        return super().form_valid(form)


def get_svg(request, pk):
    setPlt(pk)       # create the plot
    svg = pltToSvg() # convert plot to SVG
    # plt.cla()        # clean up plt so it can be re-used
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


def get_filter_svg(request, pk):
    set_filter_Plt(pk)
    svg = pltToSvg()
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


class DescriptionView(generic.TemplateView):
    template_name = 'description.html'

