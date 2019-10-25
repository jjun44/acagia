from django.db import models
from users.models import CustomUser as User

class Address(models.Model):
    STATES = [
        ('CA', 'California'),
        ('NY', 'New York')
    ]
    street = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2, choices=STATES)
    zip = models.IntegerField(null=True, blank=True)

class Academy(models.Model):
    MMA = 'MMA'
    GENERAL = 'General'
    ACA_TYPE = [
        (MMA, 'MMA'),
        (GENERAL, 'General')
    ]
    aca_name = models.CharField(max_length=30)
    aca_type = models.CharField(
        max_length=10,
        choices=ACA_TYPE,
        default=GENERAL
    )
    office_phone = models.CharField(max_length=12)
    # when User account deleted, Academy will be deleted as well
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # when Address deleted, Academy won't be deleted
    addr = models.ForeignKey(
        Address, related_name='aca_addr',
        null=True, blank=True, on_delete=models.SET_NULL
)

class Member(models.Model):
    STU = 'Stu'
    INST = 'Inst'
    OTHER = 'Other'
    MEM_TYPE = [
        (STU, 'Student'),
        (INST, 'Instructor'),
        (OTHER, 'Other')
    ]
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mem_type = models.CharField(max_length=4, choices=MEM_TYPE, default=STU)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    cell_phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=40)
    img = models.ImageField(
        height_field='300',
        width_field='200',
        upload_to='mem_photos',
        null=True, blank=True
    )
    pay_day = models.DateField(auto_now_add=True, editable=True)
    aca = models.ForeignKey(
        Academy, related_name='aca', on_delete=models.CASCADE
    )
    addr = models.ForeignKey(
        Address, related_name='mem_addr',
        blank=True, null=True, on_delete=models.SET_NULL
    )

class Instructor(models.Model):
    date_of_hire = models.DateField(auto_now_add=True, editable=True)
    mem = models.OneToOneField(
        Member, related_name='inst_detail', on_delete=models.CASCADE
    )

class Student(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Hold', 'Hold')
    ]
    date_of_start = models.DateField(auto_now_add=True, editable=True)
    status = models.CharField(max_length=7, choices=STATUS)
    mem = models.OneToOneField(
        Member, related_name='stu_detail', on_delete=models.CASCADE
    )

class Course(models.Model):
    course_name = models.CharField(max_length=40)
    course_days = models.CharField(max_length=7)
    start_time = models.TimeField()
    end_time = models.TimeField()
    inst = models.ForeignKey(
        Instructor, null=True,
        related_name='inst', on_delete=models.SET_NULL
    )

class Competition(models.Model):
    comp_date = models.DateField()
    comp_name = models.CharField(max_length=30)
    division = models.CharField(max_length=20)
    weight = models.FloatField(blank=True, null=True)
    reward = models.CharField(max_length=20, blank=True, null=True)
    stu = models.ForeignKey(
        Student, related_name='comp_stu', on_delete=models.CASCADE
    )

class Rank(models.Model):
    GENERAL = 'General'
    BJJ = 'BJJ'
    TKD = 'TKD'
    RANK_TYPE = [
        (GENERAL, 'General'),
        (BJJ, 'Jiu-jitsu'),
        (TKD, 'Taekwondo')
    ]
    RANK = {
        GENERAL:[
            ('Novice', 'Novice'),
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
            ('Master', 'Master')
        ],
        BJJ:[
            ('White', 'White'),
            ('Blue', 'Blue'),
            ('Purple', 'Purple'),
            ('Brown', 'Brown'),
            ('Black', 'Black'),
            ('Red/Black', 'Red/Black'),
            ('Red/White', 'Red/White'),
            ('Red', 'Red')
        ],
        TKD:[
            ('White', 'White'),
            ('Orange', 'Orange'),
            ('Yellow', 'Yellow'),
            ('Green', 'Green'),
            ('Purple', 'Purple'),
            ('Blue', 'Blue'),
            ('Brown', 'Brown'),
            ('Red', 'Red'),
            ('Red/Black', 'Red/Black'),
            ('Black', 'Black')
        ]
    }
    rank_type = models.CharField(max_length=10, choices=RANK_TYPE)
    rank = models.CharField(max_length=10, choices=RANK[TKD])
    days_attended = models.IntegerField(default=0)
    stu = models.ForeignKey(
        Student, related_name='rank_stu', on_delete=models.CASCADE
    )

class Attendance(models.Model):
    date_attended = models.DateTimeField(auto_now_add=True)
    stu = models.ForeignKey(
        Student, related_name='attend_stu',
        null=True, on_delete=models.SET_NULL
    )
    course = models.ForeignKey(
        Course, null=True,
        related_name='course', on_delete=models.SET_NULL
    )





