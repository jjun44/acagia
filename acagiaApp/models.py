from django.db import models
from users.models import CustomUser as User
from datetime import date

class Address(models.Model):
    STATES = [
        # left: shown in the db, right: shown in the form
        ('CA', 'California'),
        ('NY', 'New York')
    ]
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2, choices=STATES)
    zip = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        location = ''
        if self.street and self.zip:
            location = self.street + ', ' + self.city + ', ' + self.state +\
                        ', ' + self.zip
        elif self.street and not self.zip:
            location = self.street + ', ' + self.city + ', ' + self.state
        else:
            location = self.city + ', ' + self.state
        return location

class Academy(models.Model):
    MMA = 'MMA'
    GENERAL = 'General'
    ACA_TYPE = [
        (GENERAL, 'General'),
        (MMA, 'MMA')
    ]
    # when User account deleted, Academy will be deleted as well
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aca_name = models.CharField(max_length=30)
    aca_type = models.CharField(
        max_length=10,
        choices=ACA_TYPE,
        default=GENERAL
    )
    office_phone = models.CharField(max_length=12)
    # when Address deleted, Academy won't be deleted
    addr = models.ForeignKey(
        Address, related_name='aca_addr',
        null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.aca_name

class Member(models.Model):
    STU = 'Student'
    INST = 'Instructor'
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
    aca = models.ForeignKey(
        Academy, related_name='mem_aca', on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mem_type = models.CharField(max_length=10, choices=MEM_TYPE, default=STU)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    cell_phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=40)
    img = models.ImageField(
        height_field='300',
        width_field='200',
        upload_to='profiles/',
        null=True, blank=True
    )
    member_since = models.DateField(auto_now_add=True)
    addr = models.ForeignKey(
        Address, related_name='mem_addr',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def age(self):
        """
        Calculate age based on the date of birth.
        :return: calculated age
        """
        today = date.today()
        age = str((today - self.date_of_birth) / 365).split()[0]
        return age

class Student(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    HOLD = 'Hold'
    STATUS = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (HOLD, 'Hold')
    ]
    status = models.CharField(max_length=7, choices=STATUS, default=ACTIVE)
    mem = models.OneToOneField(
        Member, related_name='stu_mem', on_delete=models.CASCADE
    )

    @classmethod
    def create(cls, member_id):
        student = cls(mem_id=member_id)
        return student

class Course(models.Model):
    M = 'M'
    T = 'T'
    W = 'W'
    TH = 'Th'
    F = 'F'
    SAT = 'Sa'
    SUN = 'S'
    DAYS = [
        (M, 'Mon'),
        (T, 'Tu'),
        (W, 'Wed'),
        (TH, 'Th'),
        (F, 'Fri'),
        (SAT, 'Sat'),
        (SUN, 'Sun')
    ]

    aca = models.ForeignKey(
        Academy, related_name='course_aca', on_delete=models.CASCADE
    )
    course_name = models.CharField(max_length=40)
    course_days = models.CharField(max_length=37)
    start_time = models.TimeField()
    end_time = models.TimeField()
    instructor = models.ForeignKey(
        Member, null=True,
        related_name='course_inst', on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.course_name + ' ' + self.course_days + ' ' + \
               self.time_range

    @property
    def time_range(self):
        return str(self.start_time) + ' - ' + str(self.end_time)

class Event(models.Model):
    event_date = models.DateField()
    event_start_time = models.TimeField(blank=True, null=True)
    event_end_time = models.TimeField(blank=True, null=True)
    event_name = models.CharField(max_length=30)

class StudentEvent(models.Model):
    aca = models.ForeignKey(
        Academy, related_name='se_aca', on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student, related_name='se_stu', on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event, related_name='se_event', on_delete=models.SET('Deleted')
    )
    division = models.CharField(max_length=30)
    weight = models.FloatField(blank=True, null=True)
    reward = models.CharField(max_length=20, blank=True, null=True)

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
    rank = models.CharField(max_length=10, choices=RANK[TKD], default='None')

    def __str__(self):
        return self.rank_type + ' - ' + self.rank

class StudentRank(models.Model):
    student = models.ForeignKey(
        Student, related_name='sr_stu', on_delete=models.CASCADE
    )
    rank = models.ForeignKey(
        Rank, null=True, related_name='sr_rank', on_delete=models.SET_NULL
    )
    days_at_this_rank = models.IntegerField(default=0)

class Attendance(models.Model):
    aca = models.ForeignKey(
        Academy, related_name='att_aca', on_delete=models.CASCADE
    )
    date_attended = models.DateField(auto_now_add=True)
    time_attended = models.TimeField(auto_now_add=True)
    member = models.ForeignKey(
        Member, related_name='att_mem',
        null=True, on_delete=models.SET_NULL
    )
    course = models.ForeignKey(
        Course, null=True,
        related_name='att_course', on_delete=models.SET_NULL
    )
