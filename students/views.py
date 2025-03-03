from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from .models import Enrollment
from .models import Course
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def home(request):
    if request.user.is_authenticated:
        return redirect('student_list')  # যদি ইউজার লগিন করা থাকে, তাহলে `student_list`-এ পাঠাবে
    return render(request, 'students/home.html')  # না হলে হোমপেজ দেখাবে

# 🟢 Student List দেখানো
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student_list.html", {"students": students})



# 🟢 নতুন Student যোগ করা
@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

# 🟢 Student এডিট করা
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

# 🟢 Student ডিলিট করা
@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')



# User Registration View

def register_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another one.")
                return render(request, "students/register.html", {"form": form})

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return render(request, "students/register.html", {"form": form})

            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome, " + username)
            return redirect('student_list')

        else:
            # Handle specific errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = RegistrationForm()

    return render(request, "students/register.html", {"form": form})





# User Login View
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("student_list")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "students/login.html")

# User Logout View
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")





@login_required
def student_profile(request, id):
    student = get_object_or_404(Student, id=id)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, "students/student_profile.html", {"student": student, "enrollments": enrollments})
@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, email=request.user.email)
    enrollments = Enrollment.objects.filter(student=student)
    
    total_students = Student.objects.count()
    total_courses = Course.objects.count()

    return render(request, "students/dashboard.html", {
        "student": student, 
        "enrollments": enrollments,
        "total_students": total_students,
        "total_courses": total_courses,
    })



@login_required
def enroll_course(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return HttpResponse("No student found for this email. Please contact admin.", status=404)

    if request.method == "POST":
        form = Enrollment(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            return redirect("dashboard")
    else:
        form = Enrollment()

    return render(request, "students/enroll_course.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, 'students/dashboard.html')

@login_required
def reports(request):
    return render(request, 'students/reports.html')