from django.db import models
from users.models import CustomUser as User
from datetime import date

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
    location = models.CharField(max_length=255)
    '''
    # when Address deleted, Academy won't be deleted
    addr = models.ForeignKey(
        Address, related_name='aca_addr',
        null=True, blank=True, on_delete=models.SET_NULL
    )
    '''

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

    aca = models.ForeignKey(
        Academy, related_name='mem_aca', on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    mem_type = models.CharField(max_length=10, choices=MEM_TYPE, default=STU)
    status = models.CharField(max_length=7, choices=STATUS, default=ACTIVE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=3, choices=GENDER)
    cell_phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255)
    address = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    img = models.ImageField(
        height_field='300',
        width_field='200',
        upload_to='profiles/',
        null=True, blank=True
    )
    member_since = models.DateField(auto_now_add=True)

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
        return self.course_name

    @property
    def time_range(self):
        return str(self.start_time) + ' - ' + str(self.end_time)

class Event(models.Model):
    event_date = models.DateField()
    event_start_time = models.TimeField(blank=True, null=True)
    event_end_time = models.TimeField(blank=True, null=True)
    event_name = models.CharField(max_length=30)

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
    rank = models.CharField(max_length=10, choices=RANK[GENERAL],
                            default='None')

    def __str__(self):
        return self.rank_type + ' - ' + self.rank

class MemberRank(models.Model):
    member = models.ForeignKey(
        Member, related_name='sr_mem', on_delete=models.CASCADE
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
        Member, related_name='att_mem', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, null=True,
        related_name='att_course', on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.member) + '\'s attendance record on ' + str(
            self.date_attended)
