from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from DAlphaFS.views import gotoHomePage, shared_dir
from datetime import datetime
import psycopg2 as pgad
# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    #check if hacked
    hack_msg=""
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            loginTime= datetime.today().strftime('%Y-%m-%d')
            ipAddress,login_info = get_client_ip(request)
            if(checkifLimitExceeded(username,loginTime)):
                hack_msg ="Oops! Your account: "+username +" has been locked. Contact admin"
                context = {"hack_msg":hack_msg}        
                return render(request, 'accounts/login.html', context)
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                loginTime= datetime.today().strftime('%Y-%m-%d')
                #userName = str(request.user)
                username = request.POST.get('username')
                ipAddress,login_info = get_client_ip(request)
                insertfailedlogin(username,ipAddress,loginTime,login_info)
                #hack_msg=""
                messages.info(request, 'Username or password incorrect')
                if(checkifLimitExceeded(username,loginTime)):
                    hack_msg ="Oops! Your attack has been locked. Contact admin"
        context = {"hack_msg":hack_msg}
        return render(request, 'accounts/login.html', context)

def homePage(request):
    return shared_dir(request)

def logoutUser(request):
    logout(request)
    return redirect('login')

def checkifLimitExceeded(username,loginTime):
    single_quote ="\'"
    select_sql = "SELECT COUNT(*) FROM \"public\".\"loginaddress\" WHERE \"loginaddress\".\"username\"="+single_quote+username+single_quote +" AND \"loginaddress\".\"loginTime\" like" + single_quote + "%"+loginTime + "%"+single_quote
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        print("Select SQL is"+select_sql)
        cur.execute(select_sql)
        attempt_cnt_result = cur.fetchone()    
        #for row_var in attempt_cnt_result:
        attempt_cnt = attempt_cnt_result[0]
        if(attempt_cnt>4):
            return True 
        return False
    except(Exception) as error:
        print(error)

def insertfailedlogin(username,ipAddress,loginTime,login_info):
    single_quote = "\'"
    current_time=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    insert_sql="INSERT INTO \"public\".\"loginaddress\" VALUES(" +single_quote + username + single_quote +","+single_quote + ipAddress + single_quote +"," + single_quote + current_time + single_quote +","+single_quote+login_info+single_quote+")"
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        cur.execute(insert_sql)
        conn.commit()
    except (Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print("Device name is"+request.META['HTTP_USER_AGENT'])
    #Start
    user_agent = request.user_agent
    browser = user_agent.browser.family
    print("Browser is"+browser)
    browser_version = user_agent.browser.version_string
    print("Browser version is"+browser_version)
    os = user_agent.os.family
    print("Os is"+os)
    os_version = user_agent.os.version_string
    print("Os version is"+os_version)
    is_pc = user_agent.is_pc
    print("Is pc:"+str(is_pc))
    is_mobile = user_agent.is_mobile
    print("Is mobile:"+str(is_mobile))
    login_info = os + os_version + browser
    #End
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip,login_info