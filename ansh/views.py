from django.shortcuts import render,redirect,get_object_or_404
from .models import Coffee,Cart,Checkout,Orderp
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
import razorpay
# from razorpay import Client

# Client.set_app_details({"title" : "<YOUR_APP_TITLE>", "version" : "<YOUR_APP_VERSION>"})







@csrf_exempt

# Create your views here.

def registerform(request):
    return render(request,"register.html")

def register(request):
   
    c=""
    if request.method=='POST':
        uname=request.POST['username']
        # fname=request.POST['fname']
        # lname=request.POST['lname']
        email=request.POST['email']
        pwd=request.POST['psw']
        rpwd=request.POST['psw-repeat']
        if(pwd==rpwd):
                user = User.objects.create_user(uname, email, pwd)
                subject = "Registered"
                body = """Account Created Successfully"""
                sender = "Anshankolothumthodi@gmail.com"
                recipients = [email]
                password = "yhfiidhlffahefsy"


                def send_email(subject, body, sender, recipients, password):
                    msg = MIMEText(body)
                    msg['Subject'] = subject
                    msg['From'] = sender
                    msg['To'] = ', '.join(recipients)
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                        smtp_server.login(sender, password)
                        smtp_server.sendmail(sender, recipients, msg.as_string())
                    print("Message sent!")


                send_email(subject, body, sender, recipients, password)
                return redirect('/')
        else:
            c=True
            d={"message":c}
            return render(request,'register.html',d)
            
    user.save()
    return render(request,"login.html")

def loginform(request):
    return render(request,"login.html")

def loginpage(request):
    c=""
    username = request.POST["username"]
    password = request.POST["psw"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/home/')
    else:
        c=True
        d={"message":c}
        return render(request,"login.html",d)
    
def log_out(request):
    logout(request)
    return redirect("/")

    
@login_required


def home(request):
    d={"user":request.user}
    return render(request,"home.html",d)

@login_required

def store(request):
    p=Coffee.objects.all()
    d={"coffee": p}
    return render(request,"store.html",d)

@login_required


def addsuccess(request):
    return render(request,"addsuccess.html")

@login_required


def items(request):
    p=Coffee.objects.all()
    d={"coffee": p}
    return render(request,"items.html",d)

@login_required


def updatesuccess(request):
    return render(request,"updatesuccess.html")

@login_required


def removed(request):
    return render(request,"removed.html")

@login_required


    
def buy(request, id):
    p = Coffee.objects.get(id=id)
    
    if request.method == 'POST':
        quantity = int(request.POST["qnt"])
        im=request.POST['ima']
        userid = request.user
        
        # Check if the item already exists in the cart for this user
        k = Cart.objects.filter(itemname=p.name, userid=userid).first()
        
        totall = quantity * int(p.price)
        
        if k:
            # If the item already exists, update the quantity and total
            k.itemqnt += quantity
            k.total += totall
            k.save()
        else:
            # If it's a new item in the cart, create a new cart entry
            x= Cart(
                itemname=p.name,
                itemquantity=p.quantity,
                itemprice=p.price,
                itemqnt=quantity,
                userid=userid,
                total=totall,
                imag=im
            )
            x.save()
        
        return redirect('/showcart/')    

@login_required

def addtocart(request, id):
    p = Coffee.objects.get(id=id)
    
    if request.method == 'POST':
        quantity = int(request.POST["qnt"])
        im=request.POST['ima']
        userid = request.user
        
        # Check if the item already exists in the cart for this user
        k = Cart.objects.filter(itemname=p.name, userid=userid).first()
        
        totall = quantity * int(p.price)
        
        if k:
            # If the item already exists, update the quantity and total
            k.itemqnt += quantity
            k.total += totall
            k.save()
        else:
            # If it's a new item in the cart, create a new cart entry
            x= Cart(
                itemname=p.name,
                itemquantity=p.quantity,
                itemprice=p.price,
                itemqnt=quantity,
                userid=userid,
                total=totall,
                imag=im
            )
            x.save()
        
        return redirect('/store/')

@login_required



@login_required


def mycart(request):
    return render(request,"cart.html")

@login_required


def showcart(request):

    totalp=0

    p=Cart.objects.all().filter(userid=request.user)
    
    for x in p:
            
            totalp=totalp+x.total
    check=Checkout(totalprice=totalp)
    check.save()
    d={"coffee":p,
           "checkout":check}

    return render(request,"showcart.html",d)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart

def remove_cart_item(request, itemname, userid):
    # Filter Cart items based on itemname and userid
    cart_items = Cart.objects.filter(itemname=itemname, userid=userid)
    
    if cart_items.exists():
        cart_item = cart_items.first()  # Get the first matching item (or logic for choosing one)
        
        # Decrease the quantity by 1
        if cart_item.itemqnt > 1:
            cart_item.itemqnt -= 1
            cart_item.total -= cart_item.itemprice  # Decrease total by price
            cart_item.save()
        else:
            # If quantity is 1, delete the item
            cart_item.delete()
    
    return redirect('/showcart/')  # Redirect back to the showcart view

    
@login_required


def purchased(request,paymentid,orderid):
    order=Orderp.objects.get(razorpay_order_id=orderid)
    order.ispaid=True
    order.razorpay_payment_id=paymentid
    order.save()

    return render(request,"purchased.html")


def payfail(request):


    return render(request,"payfail.html")



@login_required


def buyform(request,id):
    p=Coffee.objects.get(id=id)
    d={"coffee":p}
    return render(request,"buyform.html",d)

@login_required


def buyform1(request,id):
    p=Coffee.objects.get(id=id)
    d={"coffee":p}
    return render(request,"buyform1.html",d)

@login_required



def addform(request):
    return render(request,"addform.html")

@login_required


def updateform(request,id):
    p=Coffee.objects.get(id=id)
    d={"coffee":p}
    return render(request,"updateform.html",d)

@login_required


def add(request):
    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']
        image = request.FILES.get('img')  
        x = Coffee(name=name, quantity=quantity, price=price, image=image)
        x.save()

    return render(request, "addsuccess.html")

@login_required

def update(request,id):
    p=Coffee.objects.get(id=id)
    if request.method=="POST":
        name=request.POST['name']
        quantity=request.POST['quantity']
        price=request.POST['price']
        image = request.FILES.get('img')
    p.name=name
    p.quantity=quantity
    p.price=price
    p.image=image
    p.save()
    return redirect('/items/')

@login_required

def remove(request,id):
    p=Coffee.objects.get(id=id)
    p.delete()
    return render(request,"removed.html")

@login_required


def cartremove(request,itemname,userid):
    p=Cart.objects.all().filter(itemname=itemname)
    p.delete()
    q=Cart.objects.all().filter(userid=request.user)
    d={"coffee":q}
    return redirect('/showcart/')

@login_required

def checkout(request):
    # client = razorpay.Client(auth=("rzp_test_1j5JxKhdrgP8gG", "6PCwTzdEeazNErFK6mDlCRL4"))

    # data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
    # payment = client.order.create(data=data)
    
    totalp=0

    p=Cart.objects.all().filter(userid=request.user)
    
    for x in p:
            
            totalp=totalp+x.total
    check=Checkout(totalprice=totalp)
    check.save()
    d={"coffee":p,
           "checkout":check}
    return render(request,"checkout.html",d)

@login_required

def ordernow(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        address=request.POST['address']
        email=request.POST['email']
        phone=request.POST['phone']
        city=request.POST['city']
        state=request.POST['state']
        zipcode=request.POST['zipcode']
        userid=request.user
        
    totalp=0
    p=Orderp.objects.all().filter(userid=request.user)
    q=Cart.objects.all().filter(userid=request.user)
    
    for x in q:
            
            totalp=totalp+x.total
    check=Checkout(totalprice=totalp)

    
    check.save()
        # for x in q:
            
        #     totalp=totalp+x.total
        # subject = "Oredered"
        # body = """Order Placed Successfully
                

                # """
        # for t in q:
        #     body=body+f"{t.itemname}-{t.itemquantity}-{t.itemprice}-{t.itemqnt}-{t.itemqnt*t.itemprice}\n"
        # body=body+f"Total= ₹{totalp}"    

        # sender = "Anshankolothumthodi@gmail.com"
        # recipients = [email]
        # password = "yhfiidhlffahefsy"


        # def send_email(subject, body, sender, recipients, password):
        #             msg = MIMEText(body)
        #             msg['Subject'] = subject
        #             msg['From'] = sender
        #             msg['To'] = ', '.join(recipients)
        #             with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        #                 smtp_server.login(sender, password)
        #                 smtp_server.sendmail(sender, recipients, msg.as_string())
        #             print("Message sent!")


        # send_email(subject, body, sender, recipients, password)

        # from twilio.rest import Client
        # account_sid = 'AC77d1b9c4ade6f469e7ff5b88488eb65a'
        # auth_token = '62afdb5471594433d8d0da7c5954ecc8'
        # client = Client(account_sid, auth_token)
        # body1 = """Order Placed Successfully on Coffe Stall
                

        #         """
        # for t in q:
        #     body1=body1+f"{t.itemname}-{t.itemquantity}-{t.itemprice}-{t.itemqnt}-{t.itemqnt*t.itemprice}\n"
        # body1=body1+f"Total= ₹{totalp}" 
        # message = client.messages.create(
        # messaging_service_sid='MGbfbf2750b4a259b4800f6ef9e5da81fb',
        # body=body1,
        # to=phone
        # )
        # print(message.sid)  

#     return render(request,"purchased.html")

# @login_required

# def myorder(request):
    client = razorpay.Client(auth=("rzp_test_6LPRQFPLbqHgqV", "szGpp0XUNPYsHyeW1iaajHt7"))

    DATA = {
            "amount": totalp*100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": fname+" "+lname,
                "key2": email,
                "key3":phone
            }
        }
    payment=client.order.create(data=DATA)
    y = Orderp(fname=fname, lname=lname,address=address,email=email,phone=phone,city=city,state=state,zipcode=zipcode,userid=userid,razorpay_order_id=payment['id'])
    y.save()
    print("*****************************************************************")
    print(payment)
    print("*****************************************************************")

    
    d={"coffee":q,
           "checkout":check,
           "order":p,
           "payment":payment}
    
    return render(request,"myorder.html",d)

@login_required

def ordercancel(request):
 p=Orderp.objects.all().filter(userid=request.user)
 p.delete()
 return redirect('/home/')


@login_required

def yourorder(request):
    totalp=0

    p=Orderp.objects.all().filter(userid=request.user)
    q=Cart.objects.all().filter(userid=request.user)

    for x in q:
            
            totalp=totalp+x.total
    check=Checkout(totalprice=totalp)
    check.save()
    d={"coffee":q,
           "checkout":check,
           "order":p}
    return render(request,"yourorder.html",d)

def clearcart(request):
    q=Cart.objects.all().filter(userid=request.user)
    q.delete()
    return redirect('/home/')



