from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.views import View
from django.db.models import Q
from main.models import Student, StudentRequest


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to dashboard on success
        else:
            messages.error(request, "Invalid username or password.")

        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login')


class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        total_requests = StudentRequest.objects.count()
        new_requests = StudentRequest.objects.filter(status="new").count()
        in_progress_requests = StudentRequest.objects.filter(status="in_progress").count()
        completed_requests = StudentRequest.objects.filter(status='completed').count()
        rejected_requests = StudentRequest.objects.filter(status='rejected').count()


        UZBEK_MONTHS = [
            "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
            "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
        ]

        # End of current month (May 2025)
        end_date = timezone.now().replace(hour=23, minute=59, second=59, microsecond=0)
        # Start of June 2024 (12 months ago)
        start_date = end_date - relativedelta(months=11)
        start_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        last_year_requests = StudentRequest.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).count()
        # List of month starts
        all_months = [start_date + relativedelta(months=i) for i in range(12)]

        # Generate monthly counts
        monthly_data_list = []
        for idx, (start, end) in enumerate(zip(all_months, all_months[1:] + [all_months[-1] + relativedelta(months=1)])):
            count = StudentRequest.objects.filter(
                created_at__gte=start,
                created_at__lt=end
            ).count()

            month_name = UZBEK_MONTHS[start.month - 1]  # month: 1-12
            monthly_data_list.append({
                'month': month_name,
                'count': count
            })

        context = {
            "total_requests": total_requests,
            "new_requests": new_requests,
            "in_progress_requests": in_progress_requests,
            "completed_requests": completed_requests,
            "rejected_requests": rejected_requests,
            "compare_percentages": int((completed_requests + rejected_requests) / total_requests * 100) if total_requests else 0,
            "last_year_requests": last_year_requests,
            "monthly_data": monthly_data_list,
        }

        return render(request, "index.html", context)


class AllListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_staff:
            requests_list = StudentRequest.objects.all()
        else:
            if request.user.office:
                requests_list = StudentRequest.objects.filter(office=request.user.office)
            else:
                raise Http404("Page not found")
        paginator = Paginator(requests_list, 10)  # Show 10 requests per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "title": "Barcha So'rovlar",
            "total_count": requests_list.count(),
            "requests": page_obj
        }
        return render(request, "list_data.html", context)


class NewListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_staff:
            requests_list = StudentRequest.objects.filter()
        else:
            if request.user.office:
                requests_list = StudentRequest.objects.filter(office=request.user.office).filter(Q(status="new") | Q(status="in_progress"))
            else:
                raise Http404("Page not found")
        paginator = Paginator(requests_list, 10)  # Show 10 requests per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "title": "Yangi So'rovlar",
            "total_count": requests_list.count(),
            "requests": page_obj
        }
        return render(request, "list_data.html", context)


class DoneListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_staff:
            requests_list = StudentRequest.objects.filter(status="completed")
        else:
            if request.user.office:
                requests_list = StudentRequest.objects.filter(office=request.user.office).filter(status="completed")
            else:
                raise Http404("Page not found")
        paginator = Paginator(requests_list, 10)  # Show 10 requests per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "title": "Bajarilgan So'rovlar",
            "total_count": requests_list.count(),
            "requests": page_obj
        }
        return render(request, "list_data.html", context)


class RejectedListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_staff:
            requests_list = StudentRequest.objects.filter(status='rejected')
        else:
            if request.user.office:
                requests_list = StudentRequest.objects.filter(office=request.user.office).filter(status='rejected')
            else:
                raise Http404("Page not found")
        paginator = Paginator(requests_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "title": "Rad Etilgan So'rovlar",
            "total_count": requests_list.count(),
            "requests": page_obj
        }
        return render(request, "list_data.html", context)


class StudentRequestDetailView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        student_request = get_object_or_404(StudentRequest, pk=pk)
        if student_request.status == "new":
            student_request.status = "in_progress"
            student_request.save()
        context = {
            "request": student_request,
            "uneditable": student_request.status in ("completed", "rejected"),
        }
        return render(request, "response_form.html", context)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        student_request = get_object_or_404(StudentRequest, pk=pk)

        if student_request.status in ("completed", "rejected"):
            return redirect("new_list")

        response = request.POST.get("response")
        response_file = request.FILES.get("response_file")
        status = request.POST.get("status")

        student_request.response = response
        student_request.response_file = response_file
        student_request.status = "completed" if status == 'on' else "rejected"
        student_request.save()

        return redirect("new_list")


def get_status_stats(request):
    new_requests = StudentRequest.objects.filter(Q(status="new") | Q(status="in_progress")).count()
    completed_requests = StudentRequest.objects.filter(status='completed').count()
    rejected_requests = StudentRequest.objects.filter(status='rejected').count()

    total = new_requests + completed_requests + rejected_requests

    data = {
        'labels': ['Yangi/Davom etmoqda', 'Bajarilgan', 'Rad etilgan'],
        'counts': [new_requests, completed_requests, rejected_requests],
        'percent': round((completed_requests / total) * 100 if total > 0 else 0)
    }
    return JsonResponse(data)

