from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Student


# ================= DEMO LOGIN DECORATOR =================
def demo_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('demo_login'):
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper


# ================= LOGIN =================
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ✅ DEMO LOGIN (Render Free compatible)
        if username == 'admin' and password == 'admin123':
            request.session['demo_login'] = True
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password')

    return render(request, 'students/login.html')


def logout_user(request):
    request.session.flush()
    return redirect('login')


# ================= DASHBOARD =================
@demo_login_required
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

    labels = [c['course'] for c in course_data]
    data = [c['total'] for c in course_data]

    return render(request, 'students/dashboard.html', {
        'total_students': total_students,
        'labels': labels,
        'data': data
    })


# ================= ADD STUDENT =================
@demo_login_required
def add_student(request):
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


# ================= VIEW STUDENTS =================
@demo_login_required
def view_students(request):
    query = request.GET.get('q')
    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)

    paginator = Paginator(students, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'students/view_students.html', {
        'students': page_obj,
        'query': query
    })


# ================= EDIT STUDENT =================
@demo_login_required
def edit_student(request, id):
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


# ================= DELETE STUDENT =================
@demo_login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Student deleted successfully")
    return redirect('view_students')
