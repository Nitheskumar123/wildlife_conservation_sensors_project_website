from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
import random
from .models import Category,Timing,Products,Cart
from .forms import RegisterForm
from .models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .forms import UpdateProfileForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from email.mime.image import MIMEImage
from django.contrib.auth.decorators import login_required
from .models import Booking
from .forms import BookingForm
from reportlab.pdfgen import canvas

def index(request):
    return render(request, "index.html")

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "signup.html", context)


def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()

    if not user_otp:
        messages.warning(request, "No OTP found for this user.")
        return redirect("verify-email", username=username)

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '')
        if user_otp.otp_code == otp_code:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                
                subject = "WELCOME MAIL"
                message = f"Hi {user.username}, Welcome to our website"
                sender = "nithes262004@gmail.com"
                receiver = [user.email]
                html_content = render_to_string('new-email.html', {'username': user.username})
                msg = EmailMultiAlternatives(subject, message, sender, receiver)
                msg.attach_alternative(html_content, "text/html")
                

                msg.send(fail_silently=False)
                
                '''send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )'''

                return redirect("signin")
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=username)
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=username)

    context = {"username": username}
    return render(request, "verify_token.html", context)


def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]

        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

            subject = "Email Verification"
            message = f"""
            Hi {user.username}, here is your OTP {otp.otp_code}
            it expires in 5 minutes, use the URL below to redirect back to the website
            http://127.0.0.1:8000/verify-email/{user.username}
            """
            sender = "nithes262004@gmail.com"
            receiver = [user.email,]

            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)
        else:
            messages.warning(request, "This email doesn't exist in the database")
            return redirect("resend-otp")

    context = {}
    return render(request, "resend_otp.html", context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect("index")
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")

    return render(request, "login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have successfully logged out.")
    return redirect("signin")


def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')  
        else:  
            form = UpdateProfileForm(instance=user)
    
        context = {"form": form}
        return render(request, "update_profile.html", context)
    else:
        return redirect('signin')  

def profile(request):
    if request.user.is_authenticated:
        return render(request, "profile.html")

def about(request):
    return render(request,'aboutus.html')


def menu(request):
    menus=Category.objects.filter(status=0)
    return render(request,'menu.html',{'menus':menus})
def timing(request,name):
    timings=Timing.objects.filter(category__name=name,status=0)
    return render(request,'timings.html',{'timings':timings})

def products(request, category_name, timing_name):
    items = Products.objects.filter(category__name=category_name, status=False, timing__name=timing_name)
    return render(request, 'items.html', {'items': items})

@login_required
def book_table(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('mybooks') 
    else:
        form = BookingForm() 

    return render(request, 'book_table.html', {'form': form})



@login_required
def my_books(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_books.html', {'bookings': bookings})

def contact(request):
    return render(request,'contact.html')


def viewitem(request, category_name, timing_name, item_name):
    
    item = get_object_or_404(Products, category__name=category_name, timing__name=timing_name, name=item_name, status=False)
    return render(request, 'viewitems.html', {'item': item})

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_qty = data.get('item_quantity')
                product_id = data.get('pid')
                
                if not product_id:
                    return JsonResponse({'status': 'Invalid Product ID'}, status=400)
                
                product_id = int(product_id)  # Ensure product_id is an integer
                product_status = Products.objects.get(id=product_id)
                
                if product_status:
                    if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                    else:
                        if product_status.quantity >= product_qty:
                            Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                            return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                        else:
                            return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON'}, status=400)
            except Products.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
            except ValueError:
                return JsonResponse({'status': 'Invalid Product ID'}, status=400)
            except Exception as e:
                return JsonResponse({'status': str(e)}, status=500)
        else:
           
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)

def cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"cart.html",{'cart':cart})
    else:
        return redirect("/")
def removecart(request,id):
    cartitem=Cart.objects.get(id=id)
    cartitem.delete()
    return redirect("/cart")



def checkout(request):
   
    
            cartitems=Cart.objects.filter(user=request.user)
            total_price=0
            for item in cartitems:
                total_price=total_price+item.product.selling_price*item.product_qty

            userprofile=Profile.objects.filter(user=request.user).first()
    
            context={'cartitems':cartitems,'total_price':total_price,'userprofile':userprofile}


            return render(request,'checkout.html',context)


from .models import Order, OrderItem, Cart,Profile

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from resfinal.models import CustomUser, Profile, Order, Cart, OrderItem
import random

def placeorder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            currentuser = request.user

            if not currentuser.first_name:
                currentuser.first_name = request.POST.get('fname')
                currentuser.last_name = request.POST.get('lname')
                currentuser.save()

            if not Profile.objects.filter(user=request.user).exists():
                userprofile = Profile()
                userprofile.user = request.user
                userprofile.phone = request.POST.get('phone')
                userprofile.address = request.POST.get('address')
                userprofile.city = request.POST.get('city')
                userprofile.state = request.POST.get('state')
                userprofile.country = request.POST.get('country')
                userprofile.save()

            neworder = Order()
            neworder.user = request.user
            neworder.fname = request.POST.get('fname')
            neworder.lname = request.POST.get('lname')
            neworder.email = request.POST.get('email')
            neworder.phone = request.POST.get('phone')
            neworder.address = request.POST.get('address')
            neworder.city = request.POST.get('city')
            neworder.state = request.POST.get('state')
            neworder.country = request.POST.get('country')
            neworder.pincode = request.POST.get('pincode')
            neworder.payment_mode = request.POST.get('payment_mode')
            neworder.payment_id = request.POST.get('payment_id')

            cart = Cart.objects.filter(user=request.user)
            cart_total_price = 0
            for item in cart:
                cart_total_price += item.product.selling_price * item.product_qty

            neworder.total_price = cart_total_price
            trackno = 'nithes' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno).exists():
                trackno = 'nithes' + str(random.randint(1111111, 9999999))

            neworder.tracking_no = trackno
            neworder.status = 'Completed'
            neworder.save()

            # Create OrderItems from Cart items
            neworderitems = Cart.objects.filter(user=request.user)
            for item in neworderitems:
                OrderItem.objects.create(
                    order=neworder,
                    product=item.product,
                    price=item.product.selling_price,
                    quantity=item.product_qty
                )

            # Clear the cart after placing the order
            Cart.objects.filter(user=request.user).delete()

            # Change status to 'Completed'
            
            neworder.save()

            messages.success(request, "Your order has been placed successfully.")
            payMode = request.POST.get('payment_mode')
            if payMode == "Paid by Razorpay":
                return JsonResponse({'status': "Your order has been placed successfully"})

            return JsonResponse({'status': "Your order has been placed successfully"})

        else:
            return JsonResponse({'status': "Order Not placed"})

    else:
        return JsonResponse({'status': "Order Not placed"})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart  

@login_required
def razorpaycheck(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_price = 0
        
        for item in cart:
            total_price += item.product.selling_price * item.product_qty
        
        return JsonResponse({
            'total_price': total_price
        })
    else:
        return JsonResponse({
            'error': 'User is not authenticated'
        }, status=401) 

def myorders(request):
    orders=Order.objects.filter(user=request.user)
    context={'orders':orders}

    return render(request,'my-orders.html',context)
def vieworder(request,trackno):
    order=Order.objects.filter(tracking_no=trackno).filter(user=request.user).first()
    orderitems=OrderItem.objects.filter(order=order)
    context={'order':order,'orderitems':orderitems}
    return render(request,'vieworder.html',context)



from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from io import BytesIO
import requests

def generate_pdf(request, order_id):
    # Fetch order details from the database
    order = get_object_or_404(Order, id=order_id)
    orderitems = OrderItem.objects.filter(order=order)

    # Prepare response for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill-{order.id}.pdf"'

    # Create PDF document
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Company details
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, "Company Name: SNK")
    p.drawString(100, 735, "Address: 1568, Church Road Kashmere Gate,")
    p.drawString(100, 720, "New Delhi, Delhi, India - 110006.")

    # Inserting logo as image
    logo_url = "https://t3.ftcdn.net/jpg/05/18/90/42/360_F_518904265_94N2jWJUNC41QaD7IduC1mahEVu9yaSn.jpg"
    try:
        logo_response = requests.get(logo_url)
        if logo_response.status_code == 200:
            logo_image = ImageReader(BytesIO(logo_response.content))
            p.drawImage(logo_image, 400, 750, width=100, height=50, preserveAspectRatio=True)
    except Exception as e:
        print(f"Failed to fetch or insert logo image: {e}")

    # Order details
    y = 700
    p.drawString(100, y, f"First Name: {order.fname}")
    p.drawString(100, y-15, f"Last Name: {order.lname}")
    p.drawString(100, y-30, f"Email: {order.email}")
    p.drawString(100, y-45, f"Phone: {order.phone}")
    p.drawString(100, y-60, f"Address:")
    p.drawString(120, y-75, f"{order.address}")
    p.drawString(120, y-90, f"{order.city}, {order.state}")
    p.drawString(120, y-105, f"{order.country} - {order.pincode}")

    # Order items
    y -= 130
    for item in orderitems:
        p.drawString(100, y, f"Product: {item.product.name}")
        p.drawString(300, y, f"Quantity: {item.quantity}")
        p.drawString(400, y, f"Price: {item.price}")
        y -= 15

    # Grand total, payment mode, status, tracking number
    y -= 30
    p.drawString(100, y, f"Grand Total: {order.total_price}")
    y -= 15
    p.drawString(100, y, f"Payment Mode: {order.payment_mode}")
    y -= 15
    p.drawString(100, y, f"Order Status: {order.status}")
    y -= 15
    p.drawString(100, y, f"Tracking Number: {order.tracking_no}")

    p.showPage()
    p.save()

    # Get PDF content from buffer and add it to response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
import os
import csv
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

def dashboard(request):
    """Render the dashboard template"""
    return render(request, 'dashboard.html')
def pressure(request):
    return render(request,'pressure.html')

def get_sensor_data(request):
    """API endpoint to get sensor data"""
    sound_data = read_sound_sensor_data()
    temp_data = read_temperature_sensor_data()
    pressure_data = read_pressure_sensor_data()
    animal_location_data = read_animal_location_data()  # Add this line
    animal_movement_data = read_animal_movement_data()  # Add this line
    
    # Calculate statistics for summary
    sound_stats = calculate_sound_stats(sound_data)
    temp_stats = calculate_temp_stats(temp_data)
    pressure_stats = calculate_pressure_stats(pressure_data)
    
    # Debug print
    print(f"Sound Stats: {sound_stats}")
    print(f"Temp Stats: {temp_stats}")
    print(f"Pressure Stats: {pressure_stats}")
    print(f"Animal Location Data Count: {len(animal_location_data)}")
    print(f"Animal Movement Data Count: {len(animal_movement_data)}")
    
    return JsonResponse({
        'sound_data': sound_data,
        'temp_data': temp_data,
        'pressure_data': pressure_data,
        'sound_stats': sound_stats,
        'temp_stats': temp_stats,
        'pressure_stats': pressure_stats,
        'animal_location_data': animal_location_data,  # Add this line
        'animal_movement_data': animal_movement_data   # Add this line
    })


def read_pressure_sensor_data():
    """Read pressure sensor data from CSV file"""
    pressure_data = []
    csv_path = os.path.join(settings.BASE_DIR, 'bin', 'WildlifeConservation_PressureSensor.csv')
    print(f"Reading pressure data from: {csv_path}")
    
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for i, row in enumerate(reader):
                if not row:  # Skip empty rows
                    continue
                
                try:
                    # Extract values from CSV
                    reading = int(row.get('Reading', '0'))
                    hour = int(row.get('Hour', '0'))
                    barometric = float(row.get('Barometric', '0'))
                    capacitive = float(row.get('Capacitive', '0'))
                    piezoelectric = float(row.get('Piezoelectric', '0'))
                    resonant = float(row.get('Resonant', '0'))
                    avg_pressure = float(row.get('AvgPressure', '0'))
                    actual_pressure = float(row.get('ActualPressure', '0'))
                    pressure_trend = float(row.get('PressureTrend', '0'))
                    humidity = float(row.get('Humidity', '0'))
                    wind_speed = float(row.get('WindSpeed', '0'))
                    animal_activity = int(row.get('AnimalActivity', '0'))
                    status = row.get('Status', 'Unknown')
                    
                    # Create data entry
                    pressure_data.append({
                        'reading': reading,
                        'hour': hour,
                        'barometric': barometric,
                        'capacitive': capacitive,
                        'piezoelectric': piezoelectric,
                        'resonant': resonant,
                        'avg_pressure': avg_pressure,
                        'actual_pressure': actual_pressure,
                        'pressure_trend': pressure_trend,
                        'humidity': humidity,
                        'wind_speed': wind_speed,
                        'animal_activity': animal_activity,
                        'status': status
                    })
                        
                except (ValueError, KeyError) as e:
                    print(f"Skipping row {i + 1} due to format issue: {e}")
                    continue
                
    except Exception as e:
        print(f"Error reading pressure data: {e}")
        # Fallback: Add dummy data if file reading fails
        pressure_data = generate_dummy_pressure_data()
    
    # If no data was read, use dummy data
    if not pressure_data:
        print("No pressure data found, using dummy data")
        pressure_data = generate_dummy_pressure_data()
        
    return pressure_data

def generate_dummy_pressure_data():
    """Generate dummy pressure data for testing"""
    data = []
    import random
    
    current_pressure = 1013.25  # Standard atmospheric pressure
    trend = 0.0
    
    for i in range(1, 30):
        hour = (i - 1) % 24
        
        # Create realistic variations
        barometric = current_pressure + random.uniform(-2, 2)
        capacitive = current_pressure + random.uniform(5, 15)
        piezoelectric = current_pressure + random.uniform(-5, 5)
        resonant = current_pressure + random.uniform(0, 10)
        
        avg_pressure = (barometric + capacitive + piezoelectric + resonant) / 4
        actual_pressure = avg_pressure + random.uniform(-10, 0)
        
        # Update trend
        if i > 1:
            trend = actual_pressure - data[-1]['actual_pressure']
        
        humidity = random.uniform(40, 80)
        wind_speed = random.uniform(0, 30)
        animal_activity = 1 if random.random() > 0.7 else 0
        
        # Determine status
        status = "Normal"
        if avg_pressure > 1030:
            status = "High Pressure System"
        elif avg_pressure < 1000:
            status = "Low Pressure System"
        elif abs(trend) > 5:
            status = "Rapid Pressure Change"
            
        data.append({
            'reading': i,
            'hour': hour,
            'barometric': round(barometric, 2),
            'capacitive': round(capacitive, 2),
            'piezoelectric': round(piezoelectric, 2),
            'resonant': round(resonant, 2),
            'avg_pressure': round(avg_pressure, 2),
            'actual_pressure': round(actual_pressure, 2),
            'pressure_trend': round(trend, 2),
            'humidity': round(humidity, 2),
            'wind_speed': round(wind_speed, 2),
            'animal_activity': animal_activity,
            'status': status
        })
        
        # Update current pressure for next iteration
        current_pressure = actual_pressure
        
    return data

def calculate_pressure_stats(pressure_data):
    """Calculate statistics from pressure sensor data"""
    if not pressure_data:
        return {
            'avg_pressure': 0,
            'min_pressure': 0,
            'max_pressure': 0,
            'avg_humidity': 0,
            'avg_wind_speed': 0,
            'pressure_changes': 0,
            'animal_activity_count': 0
        }
    
    total_pressure = sum(entry['actual_pressure'] for entry in pressure_data)
    min_pressure = min(entry['actual_pressure'] for entry in pressure_data)
    max_pressure = max(entry['actual_pressure'] for entry in pressure_data)
    
    total_humidity = sum(entry['humidity'] for entry in pressure_data)
    total_wind = sum(entry['wind_speed'] for entry in pressure_data)
    
    # Count significant pressure changes (trend > 1)
    pressure_changes = sum(1 for entry in pressure_data if abs(entry['pressure_trend']) > 1)
    animal_activity = sum(entry['animal_activity'] for entry in pressure_data)
    
    return {
        'avg_pressure': total_pressure / len(pressure_data),
        'min_pressure': min_pressure,
        'max_pressure': max_pressure,
        'avg_humidity': total_humidity / len(pressure_data),
        'avg_wind_speed': total_wind / len(pressure_data),
        'pressure_changes': pressure_changes,
        'animal_activity_count': animal_activity
    }

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def read_sound_sensor_data():
    """Read sound sensor data from CSV file (Index,Sound,Result)"""
    sound_data = []
    csv_path = os.path.join(settings.BASE_DIR, 'bin', 'WildlifeSound_Monitoring.csv')
    print(f"Reading sound data from: {csv_path}")

    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip the header

            for i, row in enumerate(reader):
                if not row or len(row) < 3:
                    print(f"Skipping row {i + 2} due to insufficient columns: {row}")
                    continue

                try:
                    index_str, sound_str, status = [col.strip() for col in row]

                    if not is_float(sound_str):
                        raise ValueError(f"Invalid float value: {sound_str}")

                    reading_num = int(index_str)
                    avg_sound = float(sound_str)

                    sound_data.append({
                        'reading': reading_num,
                        'value': avg_sound,
                        'status': status
                    })

                except (ValueError, IndexError) as e:
                    print(f"Skipping row {i + 2} due to format issue: {e}")
                    continue

    except Exception as e:
        print(f"Error reading sound data: {e}")
        sound_data = generate_dummy_sound_data()

    if not sound_data:
        print("No sound data found, using dummy data")
        sound_data = generate_dummy_sound_data()

    return sound_data

def read_temperature_sensor_data():
    """Read temperature sensor data from CSV file"""
    temp_data = []
    # Corrected path to temperature sensor CSV
    csv_path = os.path.join(settings.BASE_DIR, 'bin', 'WildlifeConservation_22BCE2778.csv')
    print(f"Reading temperature data from: {csv_path}")
    
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)  # Use DictReader for better access to column names
            
            for i, row in enumerate(reader):
                if not row:  # Skip empty rows
                    continue
                
                try:
                    # Check if the 'ActualTemp' column is in the CSV and extract the value
                    temp_value = row.get('ActualTemp')
                    
                    if temp_value:
                        # Try to convert the temperature value to float
                        temp_value = float(temp_value.strip().rstrip('°C'))
                        
                        # Determine status based on temperature
                        status = "Normal"
                        if temp_value <=0:
                            status = "Frost Warning"
                            
                        temp_data.append({
                            'reading': i + 1,  # Increment reading number for each row
                            'value': temp_value,
                            'status': status
                        })
                    else:
                        print(f"Skipping row {i + 1} due to missing 'ActualTemp' value")
                        continue
                    
    
                    
                except (ValueError, IndexError) as e:
                    print(f"Skipping row {i + 1} due to format issue: {e}")
                    continue
                
    except Exception as e:
        print(f"Error reading temperature data: {e}")
        # Fallback: Add dummy data if file reading fails
        temp_data = generate_dummy_temp_data()
    
    # If no data was read, use dummy data
    if not temp_data:
        print("No temperature data found, using dummy data")
        temp_data = generate_dummy_temp_data()
        
    return temp_data

def generate_dummy_sound_data():
    """Generate dummy sound data for testing"""
    data = []
    import random
    for i in range(1, 50):
        value = random.uniform(10, 70)
        status = "Normal"
        if value > 50:
            status = "Predator Activity Detected"
        elif value > 30:
            status = "Human Activity Detected"
            
        data.append({
            'reading': i,
            'value': value,
            'status': status
        })
    return data

def generate_dummy_temp_data():
    """Generate dummy temperature data for testing"""
    data = []
    import random
    for i in range(1, 30):
        value = random.uniform(-5, 35)
        status = "Normal"
        if value < 0:
            status = "Frost Warning"
            
        data.append({
            'reading': i,
            'value': value,
            'status': status
        })
    return data

def calculate_sound_stats(sound_data):
    """Calculate statistics from sound sensor data"""
    if not sound_data:
        return {
            'avg': 0,
            'max': 0,
            'human_activity_count': 0,
            'predator_activity_count': 0
        }
    
    total_sound = sum(entry['value'] for entry in sound_data)
    max_sound = max(entry['value'] for entry in sound_data)
    human_activity = sum(1 for entry in sound_data if entry['status'] == 'Human Activity Detected')
    predator_activity = sum(1 for entry in sound_data if entry['status'] == 'Predator Activity Detected')
    
    return {
        'avg': total_sound / len(sound_data),
        'max': max_sound,
        'human_activity_count': human_activity,
        'predator_activity_count': predator_activity
    }

def calculate_temp_stats(temp_data):
    """Calculate statistics from temperature sensor data"""
    if not temp_data:
        return {
            'avg': 0,
            'min': 0,
            'max': 0,
            'frost_warning_count': 0
        }
    
    total_temp = sum(entry['value'] for entry in temp_data)
    min_temp = min(entry['value'] for entry in temp_data)
    max_temp = max(entry['value'] for entry in temp_data)
    frost_warnings = sum(1 for entry in temp_data if entry['status'] == 'Frost Warning')
    
    return {
        'avg': total_temp / len(temp_data),
        'min': min_temp,
        'max': max_temp,
        'frost_warning_count': frost_warnings
    }

def read_animal_location_data():
    """Read animal location data from CSV file"""
    animal_data = []
    csv_path = os.path.join(settings.BASE_DIR, 'bin', 'AnimalLocations.csv')
    print(f"Reading animal location data from: {csv_path}")
    
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for i, row in enumerate(reader):
                if not row:  # Skip empty rows
                    continue
                
                try:
                    # Extract values from CSV
                    animal_id = int(row.get('AnimalID', '0'))
                    animal_type = int(row.get('AnimalType', '0'))
                    animal_name = row.get('AnimalName', 'Unknown')
                    longitude = float(row.get('Longitude', '0'))
                    latitude = float(row.get('Latitude', '0'))
                    timestamp = row.get('Timestamp', '')
                    
                    # Create data entry
                    animal_data.append({
                        'animal_id': animal_id,
                        'animal_type': animal_type,
                        'animal_name': animal_name,
                        'longitude': longitude,
                        'latitude': latitude,
                        'timestamp': timestamp
                    })
                        
                except (ValueError, KeyError) as e:
                    print(f"Skipping row {i + 1} due to format issue: {e}")
                    continue
                
    except Exception as e:
        print(f"Error reading animal location data: {e}")
        # Fallback: Add dummy data if file reading fails
        animal_data = generate_dummy_animal_data()
    
    # If no data was read, use dummy data
    if not animal_data:
        print("No animal location data found, using dummy data")
        animal_data = generate_dummy_animal_data()
        
    return animal_data

def read_animal_movement_data():
    """Read animal movement data from CSV file"""
    movement_data = []
    csv_path = os.path.join(settings.BASE_DIR, 'bin', 'AnimalMovements.csv')
    print(f"Reading animal movement data from: {csv_path}")
    
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for i, row in enumerate(reader):
                if not row:  # Skip empty rows
                    continue
                
                try:
                    # Extract values from CSV
                    reading_id = int(row.get('ReadingID', '0'))
                    animal_id = int(row.get('AnimalID', '0'))
                    animal_type = int(row.get('AnimalType', '0'))
                    animal_name = row.get('AnimalName', 'Unknown')
                    longitude = float(row.get('Longitude', '0'))
                    latitude = float(row.get('Latitude', '0'))
                    timestamp = row.get('Timestamp', '')
                    
                    # Create data entry
                    movement_data.append({
                        'reading_id': reading_id,
                        'animal_id': animal_id,
                        'animal_type': animal_type,
                        'animal_name': animal_name,
                        'longitude': longitude,
                        'latitude': latitude,
                        'timestamp': timestamp
                    })
                        
                except (ValueError, KeyError) as e:
                    print(f"Skipping row {i + 1} due to format issue: {e}")
                    continue
                
    except Exception as e:
        print(f"Error reading animal movement data: {e}")
        # Fallback: Add dummy data if file reading fails
        movement_data = generate_dummy_movement_data()
    
    # If no data was read, use dummy data
    if not movement_data:
        print("No animal movement data found, using dummy data")
        movement_data = generate_dummy_movement_data()
        
    return movement_data

def generate_dummy_animal_data():
    """Generate dummy animal location data for testing"""
    animal_names = ['Lion', 'Tiger', 'Bear', 'Wolf', 'Elephant', 'Giraffe', 'Zebra', 'Rhino', 'Buffalo', 'Hippo']
    data = []
    import random
    import datetime
    
    # Base coordinates for Bandipur National Park area
    base_lat = 11.8
    base_lon = 76.5
    
    for i in range(1, 51):
        animal_type = (i - 1) % 10
        animal_name = animal_names[animal_type]
        
        # Create location with some random variation
        longitude = base_lon + random.uniform(0, 0.7)
        latitude = base_lat + random.uniform(0, 0.4)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data.append({
            'animal_id': i,
            'animal_type': animal_type,
            'animal_name': animal_name,
            'longitude': longitude,
            'latitude': latitude,
            'timestamp': timestamp
        })
    
    return data

def generate_dummy_movement_data():
    """Generate dummy animal movement data for testing"""
    animal_names = ['Lion', 'Tiger', 'Bear', 'Wolf', 'Elephant', 'Giraffe', 'Zebra', 'Rhino', 'Buffalo', 'Hippo']
    data = []
    import random
    import datetime
    
    # Base coordinates for Bandipur National Park area
    base_lat = 11.8
    base_lon = 76.5
    reading_id = 0
    
    for i in range(1, 11):
        animal_type = (i - 1) % 10
        animal_name = animal_names[animal_type]
        
        # Create location with some random variation
        longitude = base_lon + random.uniform(0, 0.7)
        latitude = base_lat + random.uniform(0, 0.4)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data.append({
            'reading_id': reading_id,
            'animal_id': i,
            'animal_type': animal_type,
            'animal_name': animal_name,
            'longitude': longitude,
            'latitude': latitude,
            'timestamp': timestamp
        })
    
    return data

def animal(request):
    return render(request,'animal_location.html')