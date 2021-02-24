from django.shortcuts import render
from .models import StoreString
from django.http import  HttpResponseRedirect 
from django.urls import reverse
import random
import string
# Create your views here.

storestring = [] #พักเก็บ string ที่สุ่มแต่ละครั้ง
repeatString = [] #พักเก็บ string ทีซ้ำ

def home(request): # home.html
    repeatString.clear() # ทุกครั้งที่กลับมาหน้า home จะทำการ clear ข้อมูลในlist
    return render(request,'randomStr/home.html')

def randomString(request): # แสดงชุด string ที่ได้ random มาทั้งหมดใน1ครั้ง
    if request.method == 'POST':
        newString = ''
        lenString = int(request.POST['lengthofstring']) #จำนวนชุด
        groupString = int(request.POST['groupofstring']) #ความยาว string
        stringAll = string.ascii_letters + string.digits + string.punctuation #strings ที่จะนำไปเก็บในlist
        letter= list(stringAll)  #นำมาเก็บลงเป็นlist
        for i in range(0,groupString): 
            for s in range(0,lenString): 
                newString = newString + random.choice(letter) #นำ string ที่สุ่มได้จากlistมาต่อกัน
            storestring.append(newString) # ตัวแปล
            newString = ''
        return render(request, 'randomStr/home.html',{'letter':storestring})
    return HttpResponseRedirect(reverse('randomString'))

def addRandomStr(request): # insert ข้อมูลลง database
    context ={} # dictionary
    if request.method == 'POST':
        if (len(storestring) == 0): # เมื่อกด submit โดยไม่มีข้อมูล
            return render(request,'randomStr/home.html',{'message':"ไม่มีข้อมูลให้ insert"})
        else:
            for randomStr in storestring:
                if (len(StoreString.objects.filter(randomStr= randomStr)) != 1): #string ไม่ซ้ำให้ insert ลงdatabase
                    f = StoreString(randomStr = randomStr)
                    f.save()
                else:
                    repeatString.append(randomStr) # สรหะ  เก็บ string ตัวที่ซ้ำกับ database
            storestring.clear()
        if (len(repeatString) != 0): # ถ้า list repeatString มีข้อมูล ให้แสดง string ที่ซ้ำ
            return render(request, 'randomStr/listRandom.html' ,{'repeatString': repeatString})
        return render(request, 'randomStr/home.html' ,{'message':'Insert ข้อมูลเรียบร้อย'})
    return HttpResponseRedirect(reverse('randomString'))
    
def allRandomString(request): # แสดงจำนวนชุด string ที่มีใน database
    if request.method == 'POST':
        if (len(StoreString.objects.all()) == 0): #เช็คว่ามีstring ใน databaseมั้ย
            return render(request, 'randomStr/allRandom.html', {'message':'ยังไม่มีข้อมูล'})
        randomStr = StoreString.objects.all()
        return render(request, 'randomStr/allRandom.html',{'randomStr': randomStr})
    return HttpResponseRedirect(reverse("home"))

def deleteRandomString(request): # ลบ string ตัวที่กดลบ
    context = {}
    if request.method == 'POST':
        delString = request.POST['deleteRandomString']
        randString = StoreString.objects.filter(randomStr = delString) # ค้าหา string  ที่ต้องการจะลบใน database
        randString.delete()
        context['allString'] = StoreString.objects.all()
        context['message'] = "ลบเรียบร้อย"
        randomStr = StoreString.objects.all()
        return render(request, 'randomStr/allRandom.html',context)
    return HttpResponseRedirect(reverse("home"))
