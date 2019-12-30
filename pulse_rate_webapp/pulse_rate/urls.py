from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'pulse_rate'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('pulse_rate-list/', views.PulseRateListView.as_view(), name="pulse_rate_list"),
    path('pulse_rate-detail/<int:pk>/', views.PulseRateDetailView.as_view(), name="pulse_rate_detail"),
    # path('pulse_rate-detail/<int:pk>/plot/', views.get_svg, name="plot"),
    path('pulse_rate-create/', views.PulseRateCreateView.as_view(), name="pulse_rate_create"),
    path('pulse_rate-update/<int:pk>/', views.PulseRateUpdateView.as_view(), name="pulse_rate_update"),
    path('pulse_rate-delete/<int:pk>/', views.PulseRateDeleteView.as_view(), name="pulse_rate_delete"),

    path('pulse_rate-analysis/<int:pk>/', views.PulseRateAnalysisView.as_view(), name="pulse_rate_analysis"),
    path('pulse_rate-detail/<int:pk>/plot/', views.get_filter_svg, name="plot_filter"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
