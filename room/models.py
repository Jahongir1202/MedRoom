from django.db import models

class MedRoom(models.Model):
    CHOOSE = [
        ('palata', 'Palata'),
        ('lux', 'Lux'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    chamber_type = models.CharField(max_length=10,choices=CHOOSE,default='palata')
    room = models.IntegerField(null=True, blank=True)
    ROOM = [
        ('joy1','Joy1'),
        ('joy2','Joy2')
    ]
    place = models.CharField(max_length=10,choices=ROOM, blank=True
                             )
    def __str__(self):
        return f"{self.room} {self.chamber_type}"

class Place(models.Model):
    ROOM = [
        ('joy1', 'Joy1'),
        ('joy2', 'Joy2'),
    ]
    med_room = models.ForeignKey(MedRoom, on_delete=models.CASCADE, related_name='places')
    place_slot = models.CharField(max_length=10, choices=ROOM)  # joy1 yoki joy2
    is_full_room = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    job = models.CharField(max_length=100, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    brought = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(null=True, blank=True)
    price_nurse = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_rented = models.BooleanField(default=False)


    @property
    def price_total(self):
        if self.price and self.day:
            return self.price * self.day
        return 0

    @property
    def nurse_total(self):
        if self.price_nurse and self.day:
            return self.price_nurse * self.day
        return 0

    @property
    def total_cost(self):
        return self.price_total + self.nurse_total

    def __str__(self):
        return f"{self.name} - {self.place_slot} - Room {self.med_room.room}"



class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Expenses(models.Model):
    price = models.IntegerField()
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    text = models.CharField(max_length=100)

    room = models.ForeignKey('MedRoom', on_delete=models.SET_NULL, null=True, blank=True)
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.last_name} - {self.price}"