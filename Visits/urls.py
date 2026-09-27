from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "operations"
urlpatterns = [
    path("visit/<int:pk>/card/", views.VisitView.as_view(), name="visit_detail"),
    path("visit/<int:pk>/review/", views.StaffVisitReviewView.as_view(), name="visit_review"),
    path("visit/<int:pk>/supervisor-review/", views.SupervisorVisitView.as_view(), name="supervisor_visit_review"),
    path("visit/<int:pk>/",views.SupervisorVisitView.as_view(),name="visit"),


    path("visit/update_status_by_supervisor/<int:Id>/", views.update_status_by_supervisor, name="update_status_by_supervisor"),



    path('visit/<int:pk>/pdf/', views.ExportVisitPDFView.as_view(), name='export_visit_pdf'),

    # 3. مسار عرض البيانات للعميل والعامة (يعمل فقط إذا كانت الحالة مكتملة أو قيد المراجعة)
    # path("visit/<int:pk>/public/", views.PublicVisitReportView.as_view(), name="visit_public"),


    path("visit/request/<int:Id>/",views.save_report,name="save_report",),
    path("visit/json/<int:Id>/", views.save_inspection_items, name="save_inspection_items"),


    path('visit/inspection/<int:table_id>/', views.visit_inspection_view, name='visit_inspection'),






    #     path("visit/<int:pk>/start/", views.StartVisitView.as_view(), name="start_visit"),
    #     path("visit/<int:pk>/card/", views.visit_card, name="visit_card"),
]
