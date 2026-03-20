from pydantic import BaseModel
from typing import List
from datetime import date


class StudentOut(BaseModel):
    """ StudentOut
    """
    id: int
    first_name: str
    last_name: str
    email: str
    birth_date: date


class StudentIn(BaseModel):
    """ StudentIn
    """
    first_name: str
    last_name: str
    email: str
    birth_date: date


class CourseOut(BaseModel):
    """ CourseOut
    """
    id: int
    name: str
    description: str
    students: List[StudentOut] = []


class CourseIn(BaseModel):
    """ CourseIn
    """
    name: str
    description: str


class EnrollmentIn(BaseModel):
    """ registration on kurs
     """
    student_id: int
    course_id: int


class EnrollmentOut(BaseModel):
    """ info registration
     """
    id: int
    student: StudentOut
    course: CourseOut
    enrolled_at: date


class GradeIn(BaseModel):
    """ Add Garade
     """
    student_id: int
    course_id: int
    score: float


class GradeOut(BaseModel):
    """ information Grade
    """
    id: int
    student: StudentOut
    course: CourseOut
    score: float
    graded_at: date


class CourseAverageOut(BaseModel):
    """ Average kurs
     """
    course: CourseOut
    average_score: float
