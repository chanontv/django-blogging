import email
from django.shortcuts import render,redirect
from category.models import Category
from .models import Blogs
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .forms import RegisterForm, ChangePasswordForm , EditProfileForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your views here
def index(request):
    categories = Category.objects.all()
    blogs = Blogs.objects.all()
    lastest = Blogs.objects.all().order_by('-pk')[:2]

    #paginator
    paginator = Paginator(blogs,6)
    try:
        page = int(request.GET.get('page',1))
    except:
        page = 1
    try:
        blogPerpage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        blogPerpage = paginator.page(paginator.num_pages)

    return render(request,'index.html',
    {
        'categories':categories,
        'blogs':blogPerpage,
        'lastest':lastest,
    })

def blogDetail(request,id):
    popular = Blogs.objects.all().order_by('-views')[:3]
    suggestion = Blogs.objects.all().order_by('views')[:3]
    singleBlog = Blogs.objects.get(id=id)
    singleBlog.views = singleBlog.views+1
    singleBlog.save()
    return render(request,'blogDetail.html',
    {
        'blog':singleBlog,
        'popular':popular,
        'suggestion':suggestion,
    })

def registerForm(request):
    form = RegisterForm()
    context = {'form':form}
    return render(request,'register.html',context)

def register(request):
    """ 
    username = request.POST['username']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    password = request.POST['password']
    repassword = request.POST['repassword']

    #validation
    if password==repassword :
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')
            return redirect('/createForm')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email already exists')
            return redirect('/createForm')
        else :
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname
                )
            user.save()    
            return redirect('/')
    else :
        messages.info(request,'Passwords do not match')
        return redirect('/register') """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
    
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')
            return redirect('/registerform')
        
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email already exists')
            return redirect('/registerform')
                
        if form.is_valid():
            data = form.cleaned_data
        
            if data['password'] != data['repassword'] :
                messages.info(request,'Passwords do not match')
                return redirect('/registerform')
            elif len(data['password']) < 6:
                messages.info(request,'Passwords must be at least 6 characters')
                return redirect('/registerform')
            else:
                user = User()
                user.username = data['username']
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.email = data['email']
                user.password = make_password(data['password'])
                user.save()
                return redirect('/') 

def loginForm(request):
    return render(request,'login.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']

    #login
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return redirect('/')
    else :
        messages.info(request,'Not Found')
        return redirect('/loginform')

def changePassForm(request):
    form = ChangePasswordForm()
    context = {'form':form}
    return render(request,'updatePassword.html',context)

def changePass(request,id):
    oldpassword = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    renewpassword =  request.POST['renewpassword']
    user = User.objects.get(id=id)

    if newpassword != renewpassword:
        messages.info(request,'Passwords do not match')
        return redirect('/changepasswordform')
    if check_password(oldpassword, user.password):
        user.password = make_password(newpassword)
        user.save() 
        return redirect('/')

def updateProfileForm(request):
    form = EditProfileForm()
    context = {'form':form}
    return render(request,'updateProfile.html',context)

def updateProfile(request,id):
    """ first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    
    user = User.objects.get(id=id)

    user.first_name = first_name
    user.last_name = last_name
    user.email = email

    user.save()
    return redirect('/')  """

    form = EditProfileForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.get(id=id)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.save()
        return redirect('/') 

def logout(request):
    auth.logout(request)
    return redirect('/')

def createBlog(request):
    categories = Category.objects.all()
    return render(request,'createBlog.html',{
        'categories':categories,
    })

def createRecord(request):
    blogname = request.POST['blogname']
    desc = request.POST['desc']
    content = request.POST['content']
    category = request.POST['category']
    writer = request.POST['writer']
    #image = request.FILES['image']

    blog = Blogs.objects.create(
                name=blogname,
                description=desc,
                content=content,
                category_id=category,
                writer=writer,
                #image=image,
                )
    blog.save()
    messages.info(request,'Create Success.')    
    return redirect(f'/myblog/{writer}')

def myBlog(request,username):
    myblogs = Blogs.objects.all().filter(writer=username)
    return render(request,'myBlog.html',{
        'blogs' : myblogs,
        'writer': username
    })

def updateBlog(request,id):
    updateblogs = Blogs.objects.all().filter(id=id)
    categories = Category.objects.all()

    return render(request,'updateBlog.html',{
        'blogs': updateblogs,
        'categories': categories,
    })

def updateRecord(request,id):
    blogname = request.POST['blogname']
    desc = request.POST['desc']
    content = request.POST['content']
    category = request.POST['category']
    #image = request.FILES['image']

    blog = Blogs.objects.get(id=id)
    blog.name = blogname
    blog.description = desc
    blog.content = content
    blog.category_id = category
    #blog.image = image 
    blog.save()

    writer = request.user.username
    messages.info(request,'Update Success.')    
    return redirect(f'/myblog/{writer}')

def deleteBlog(request,username,id):
    writer = request.user.username
    if username == writer:
        myblogs = Blogs.objects.get(id=id)
        myblogs.delete()
        messages.info(request,'Delete Success.')
        return redirect(f'/myblog/{writer}')
    else:
        return render(request,'noaccess.html')
