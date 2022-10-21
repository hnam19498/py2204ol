import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','testweb.settings')
django.setup()

from myapp.models import Student
# student1 = Student(name="Ronaldo",age=37,gender=True,email="ronaldo@mail.com", phone="123",address="England")
# student1.save()

# #Lưu ý, khi tạo object từ class như trên, cần thêm lệnh để thêm record vào database: <tên object>.save()

# student2 = Student.objects.create(name="Messi",age=35,gender=True,email="messi@mail.com",phone="321",address="France")
# # Dùng qua <tên class>.objects.create("") thì không cần .save()

students = Student.objects.all() # = với: select * from Student
for student in students:
    print(student.name)


student = Student.objects.get(id=1) # trả về duy nhất 1 giá trị

student.__dict__

student = Student.objects.filter(id=1) # trả về 1 danh sách