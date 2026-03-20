from typing import List, Dict
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Student, Course, Enrollment, Grade
from .schemas import (
    StudentIn, StudentOut,
    CourseIn, CourseOut,
    EnrollmentIn, EnrollmentOut,
    GradeIn, GradeOut,
    CourseAverageOut
)
from .auth import SimpleBearerAuth
from datetime import date

router = Router()
auth_scheme = SimpleBearerAuth()


@router.get("/students", response=List[StudentOut], auth=auth_scheme)
def list_students(request) -> List[StudentOut]:
    """Retrieve a list of all students
    """
    return list(Student.objects.all())


@router.post("/students", response=StudentOut, auth=auth_scheme)
def create_student(request, payload: StudentIn) -> StudentOut:
    """Create a new student
    """
    student = Student.objects.create(**payload.model_dump())
    return student


@router.get("/students/{student_id}", response=StudentOut, auth=auth_scheme)
def get_student(request, student_id: int) -> StudentOut:
    """Retrieve a single student by ID
    """
    student = get_object_or_404(Student, id=student_id)
    return student


@router.put("/students/{student_id}", response=StudentOut, auth=auth_scheme)
def update_student(request, student_id: int, payload: StudentIn) -> StudentOut:
    """Update student information
    """
    student = get_object_or_404(Student, id=student_id)
    for attr, value in payload.model_dump().items():
        setattr(student, attr, value)
    student.save()
    return student


@router.delete("/students/{student_id}", auth=auth_scheme)
def delete_student(request, student_id: int) -> Dict[str, bool]:
    """Delete a student
    """
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return {"success": True}


@router.get("/courses", response=List[CourseOut], auth=auth_scheme)
def list_courses(request) -> List[CourseOut]:
    """Retrieve a list of all courses
    """
    return list(Course.objects.all())


@router.post("/courses", response=CourseOut, auth=auth_scheme)
def create_course(request, payload: CourseIn) -> CourseOut:
    """Create a new course
    """
    course = Course.objects.create(**payload.model_dump())
    return course


@router.get("/courses/{course_id}", response=CourseOut, auth=auth_scheme)
def get_course(request, course_id: int) -> CourseOut:
    """Retrieve a single course by ID
    """
    course = get_object_or_404(Course, id=course_id)
    return course


@router.put("/courses/{course_id}", response=CourseOut, auth=auth_scheme)
def update_course(request, course_id: int, payload: CourseIn) -> CourseOut:
    """Update course information
    """
    course = get_object_or_404(Course, id=course_id)
    for attr, value in payload.model_dump().items():
        setattr(course, attr, value)
    course.save()
    return course


@router.delete("/courses/{course_id}", auth=auth_scheme)
def delete_course(request, course_id: int) -> Dict[str, bool]:
    """Delete a course
    """
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return {"success": True}


@router.post("/enrollments", response=EnrollmentOut, auth=auth_scheme)
def enroll_student(request, payload: EnrollmentIn) -> EnrollmentOut:
    """Enroll a student in a course
    """
    student = get_object_or_404(Student, id=payload.student_id)
    course = get_object_or_404(Course, id=payload.course_id)
    enrollment, _ = Enrollment.objects.get_or_create(
        student=student,
        course=course,
        defaults={"enrolled_at": date.today()}
    )
    return enrollment


@router.post("/grades", response=GradeOut, auth=auth_scheme)
def add_grade(request, payload: GradeIn) -> GradeOut:
    """Add or update a student's grade for a course
    """
    student = get_object_or_404(Student, id=payload.student_id)
    course = get_object_or_404(Course, id=payload.course_id)
    grade, _ = Grade.objects.update_or_create(
        student=student,
        course=course,
        defaults={"score": payload.score, "graded_at": date.today()}
    )
    return grade


@router.get("/courses/{course_id}/average", response=CourseAverageOut, auth=auth_scheme)
def course_average(request, course_id: int) -> CourseAverageOut:
    """Get the average grade for a course
    """
    course = get_object_or_404(Course, id=course_id)
    avg_score = Grade.objects.filter(course=course).aggregate(Avg("score"))["score__avg"] or 0.0
    return {"course": course, "average_score": avg_score}
