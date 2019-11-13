from django.db import models
from users.models import CustomUser as User
from datetime import date
from PIL import Image # for resizing image file
from datetime import timedelta # for calculating age based on birth day
import pytz # for choices of common time zones
from django.utils import timezone

'''
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
'''

class Academy(models.Model):
    GENERAL = 'General'
    BJJ = 'Jiu-jitsu'
    MMA = 'MMA'
    TKD = 'Taekwondo'

    ACA_TYPE = [
        (GENERAL, 'General'),
        (BJJ, 'Jiu-jitsu'),
        (MMA, 'MMA'),
        (TKD, 'Taekwondo')
    ]

    TIME_ZONES = [(zone, zone) for zone in pytz.common_timezones]

    # when User account deleted, Academy will be deleted as well
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aca_name = models.CharField(max_length=30)
    aca_type = models.CharField(
        max_length=10,
        choices=ACA_TYPE,
        default=GENERAL
    )
    office_phone = models.CharField(max_length=12)
    location = models.CharField(max_length=255)
    time_zone = models.CharField(max_length=20,
                                 choices=TIME_ZONES,
                                 default='US/Pacific'
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
        ('F', 'Female'),
        ('N/A', 'Other')
    ]
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    HOLD = 'Hold'
    STATUS = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (HOLD, 'Hold')
    ]
    IMAGE_SIZE = (300, 350)

    aca = models.ForeignKey(
        Academy, related_name='mem_aca', on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    mem_type = models.CharField(max_length=10, choices=MEM_TYPE, default=STU)
    status = models.CharField(max_length=8, choices=STATUS, default=ACTIVE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=3, choices=GENDER)
    cell_phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255)
    address = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    img = models.ImageField(
        upload_to='mem_photos/',
        default='mem_photos/no-img.png',
        null=True, blank=True
    )
    member_since = models.DateField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # https://stackoverflow.com/questions/24373341/django-image-resizing-and-convert-before-upload
    def save(self):
        """
        Resizes a profile image.
        """
        if self.img:
            super().save()
            image = Image.open(self.img)
            size = Member.IMAGE_SIZE
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.img.path)

    # https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
    @property
    def age(self):
        """
        Calculate age based on the date of birth.
        :return: calculated age
        """
        today = timezone.localdate()
        age = (today - self.date_of_birth) // timedelta(365.2425)
        return age

    @classmethod
    def find_member_by_name(cls, aca_id, fname, lname):
        """
        Finds a member by academy id and member's first and last name.
        :param aca_id: academy id
        :param fname: member's first name
        :param lname: member's last name
        :return: Member object if found, otherwise, None
        """
        try:
            return Member.objects.get(aca_id=aca_id, first_name=fname,
                                      last_name=lname)
        except Member.DoesNotExist:
            return None

    @classmethod
    def find_member_by_id(cls, mem_id):
        """
        Finds a member by member id.
        :param mem_id: member id
        :return: Member object if found, otherwise, None
        """
        try:
            return Member.objects.get(id=mem_id)
        except Member.DoesNotExist:
            return None

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
        Member, null=True, blank=True,
        related_name='course_inst', on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.course_name + ' ' + self.course_days + ' ' + \
               self.time_range

    @property
    def time_range(self):
        return str(self.start_time)[0:5] + ' - ' + str(self.end_time)[0:5]

class Event(models.Model):
    aca = models.ForeignKey(
        Academy, related_name='e_aca', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class MemberEvent(models.Model):
    aca = models.ForeignKey(
        Academy, related_name='me_aca', on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        Member, related_name='me_mem', on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event, related_name='me_event', on_delete=models.SET('Deleted')
    )
    division = models.CharField(max_length=30)
    weight = models.FloatField(blank=True, null=True)
    reward = models.CharField(max_length=20, blank=True, null=True)

class Rank(models.Model):
    GENERAL = 'General'
    BJJ = 'Jiu-jitsu'
    TKD = 'Taekwondo'
    CUST = 'Custom'
    RANK_TYPE = [
        (CUST, 'Custom'),
        (BJJ, 'Jiu-jitsu'),
        (GENERAL, 'General'),
        (TKD, 'Taekwondo'),
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
            ('Yellow', 'Yellow'),
            ('Ad-Yellow', 'Ad-Yellow'),
            ('Orange', 'Orange'),
            ('Purple', 'Purple'),
            ('Ad-Purple', 'Ad-Purple'),
            ('Green', 'Green'),
            ('Blue', 'Blue'),
            ('Ad-Blue', 'Ad-Blue'),
            ('Brown', 'Brown'),
            ('Red', 'Red'),
            ('Ad-Red', 'Ad-Red'),
            ('Danbo', 'Danbo'),
            ('Black', 'Black')
        ]
    }
    TKD_DAYS = {'White':16, 'Yellow':16, 'Ad-Yellow':16, 'Orange':16,
                'Purple':24, 'Ad-Purple':24, 'Green':24, 'Blue':24,
                'Ad-Blue':24, 'Brown':24, 'Red':24, 'Ad-Red':30, 'Danbo':None,
                'Black':None}

    aca = models.ForeignKey(
        Academy, related_name='rank_aca', on_delete=models.CASCADE
    )
    #rank_type = models.CharField(max_length=10, choices=RANK_TYPE)
    rank_order = models.IntegerField()
    rank = models.CharField(max_length=20)
    # number of attendance required
    days_required = models.IntegerField()

    def __str__(self):
        return (self.rank or 'X')

class MemberRank(models.Model):
    aca = models.ForeignKey(
        Academy, related_name='mr_aca', on_delete=models.CASCADE
    )
    member = models.OneToOneField(
        Member, related_name='mr_mem', on_delete=models.CASCADE
    )
    rank = models.ForeignKey(Rank, related_name='mr_rank',
                                on_delete=models.SET_NULL, null=True)
    days_attended = models.IntegerField(default=0, blank=True)
    total_days = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.member) + '/' + (str(self.rank) or 'X')

class Attendance(models.Model):
    aca = models.ForeignKey(
        Academy, related_name='att_aca', on_delete=models.CASCADE
    )
    date_attended = models.DateField()
    time_attended = models.TimeField()
    member = models.ForeignKey(
        Member, related_name='att_mem', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, null=True,
        related_name='att_course', on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.member) + '\'s attendance record on ' + str(
            self.date_attended)

