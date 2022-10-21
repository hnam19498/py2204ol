from django.db import models
from django import forms


class Student(models.Model): # tên table liên kết với class model: <tên app viết thường>_<tên class viết thường>
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.BooleanField()
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.TextField(default="Nam Định")

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return f'{self.name} is Place'

    class Meta:
        db_table = "Place" # db_table: đặt tên tuỳ chọn của table trong DB

class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE, # khi mình xoá khoá chính liên kết FK thì sẽ tự động xoá theo FK
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.place.name}'s restaurant"

    class Meta:
        db_table = "Restaurant"

# Trong quan hệ 1-1 A với B thì class nào giữ OneToOneField() thì muốn truy qua class còn lại thì dùng tên thuộc tính trong giữ OneToOneField()
# Ngược lại thì class kia dùng .<tên class viết thường>

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'Reporter'

class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']
        db_table = 'Publication'

    def __str__(self):
        return self.title

class Article(models.Model):
    publications = models.ManyToManyField(Publication)
    # class A 1-n B: từ A truy cập tất cả các dòng liên kết <tên biến class A>.<tên class B(viết thường)>_set
    # từ class B, truy cập ngược liên kết với A: <tên biến class B>.<tên class A(viết thường)>
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.headline

    class Meta:
        db_table = 'Article'
        ordering = ['headline'] # dùng để sắp xếp  ['<tên>'] = tăng dần, ['-<tên>'] = giảm dần

class Pet(models.Model):

    TYPE_CHOICES = (
        ('cat', 'Cat'),
        ('dog', 'Dog'),
    )
    
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField('Tên', max_length=20)
    age = models.IntegerField('Tuổi')
    type = models.CharField('Phân loại', max_length=3, choices=TYPE_CHOICES)
    weight = models.IntegerField('Chiều cao')
    length = models.IntegerField('Chiều dài')
    color = models.CharField('Màu sắc', max_length=7)
    vacinated = models.BooleanField("Đã tiêm vắc xin")
    dewormed = models.BooleanField('Đã tẩy giun')
    sterilized = models.BooleanField('Đã tiệt trùng')
    
    class Meta:
        db_table = "Pet"
