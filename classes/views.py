from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Classroom, Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('classroom-list')
	context = {
		"form": form
	}
	return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	return redirect('classroom-list')

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	students = Student.objects.filter(classroom=classroom)
	students = students.order_by('first_name','-exam_grade')
	context = {
		"classroom": classroom,
		"students": students,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_anonymous:
		messages.warning(request, "Please signin")
		return redirect('signin')
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			classroom_obj=form.save(commit=False)
			classroom_obj.teacher = request.user
			classroom_obj.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_staff or request.user == classroom.teacher):
		messages.warning(request, "You are unauthorized to perform this action")
		return redirect('classroom-list')
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_staff or request.user == classroom.teacher):
		messages.warning(request, "You are unauthorized to perform this action")
		return redirect('classroom-list')
	classroom.delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')

def student_create(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_staff or request.user == classroom.teacher):
		messages.warning(request, "You are not authorized to perform this action")
		return redirect(classroom)
	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST, request.FILES or None)
		if form.is_valid():
			student_obj=form.save(commit=False)
			student_obj.classroom = classroom
			student_obj.save()
			messages.success(request, "Successfully Created!")
			return redirect(classroom)
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'create_student.html', context)

def student_update(request, student_id):
	student = Student.objects.get(id=student_id)
	classroom_id=student.classroom.id
	if not (request.user.is_staff or request.user == student.classroom.teacher):
		messages.warning(request, "You are not authorized to perform this action")
		return redirect(classroom)
	form = StudentForm(instance=student)
	if request.method == "POST":
		form = StudentForm(request.POST, request.FILES or None, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-detail',classroom_id)
		print (form.errors)
	context = {
	"form": form,
	"student": student,
	}
	return render(request, 'update_student.html', context)

def student_delete(request, student_id):
	student = Student.objects.get(id=student_id)
	classroom_id = student.classroom.id
	if not (request.user.is_staff or request.user == student.classroom.teacher):
		messages.warning(request, "You are unauthorized to perform this action")
		return redirect('classroom-detail', classroom_id)
	classroom.delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-detail', classroom_id)
