from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Student


# ---------------- LOGIN ----------------
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # NORMAL DJANGO LOGIN
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password')

    return render(request, 'students/login.html')


# ---------------- LOGOUT ----------------
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    total_students = Student.objects.count()

    course_data = (
        Student.objects
        .exclude(course__isnull=True)
        .exclude(course__exact='')
        .values('course')
        .annotate(total=Count('id'))
        .order_by('course')
    )

    labels = []
    data = []

    for item in course_data:
        labels.append(item['course'])
        data.append(item['total'])

    return render(request, 'students/dashboard.html', {
        'total_students': total_students,
        'labels': labels,
        'data': data
    })


# ---------------- ADD STUDENT ----------------
@login_required
def add_student(request):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "You don't have permission to add students")
        return redirect('view_students')

    if request.method == 'POST':
        Student.objects.create(
            name=request.POST.get('name'),
            roll_no=request.POST.get('roll'),
            email=request.POST.get('email'),
            course=request.POST.get('course'),
            phone=request.POST.get('phone')
        )
        messages.success(request, "Student added successfully")
        return redirect('view_students')

    return render(request, 'students/add_student.html')


# ---------------- VIEW STUDENTS ----------------
@login_required
def view_students(request):
    query = request.GET.get('q')

    students = Student.objects.all()
    if query:
        students = students.filter(name__icontains=query)

    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'students/view_students.html', {
        'students': page_obj,
        'query': query
    })


# ---------------- EDIT STUDENT ----------------
@login_required
def edit_student(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "You don't have permission to edit students")
        return redirect('view_students')

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.roll_no = request.POST.get('roll')
        student.email = request.POST.get('email')
        student.course = request.POST.get('course')
        student.phone = request.POST.get('phone')
        student.save()

        messages.success(request, "Student updated successfully")
        return redirect('view_students')

    return render(request, 'students/edit_student.html', {'student': student})


# ---------------- DELETE STUDENT ----------------
@login_required
def delete_student(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Only admin can delete students")
        return redirect('view_students')

    student = get_object_or_404(Student, id=id)
    student.delete()

    messages.success(request, "Student deleted successfully")
    return redirect('view_students')
