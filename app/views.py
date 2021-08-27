
from django.shortcuts import render, redirect, reverse 
from django.http import HttpResponse, HttpResponseRedirect
from .models import*
from .util import *
import random 



from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def Index(request):
    artist = Artist.objects.all()
    return render(request, "app/index-1.html", {'artist': artist, 'total_artists': len(artist)})


def IndexPage(request):
    artist = Artist.objects.all()
    return render(request, "app/index-logged-out.html", {'artist': artist, 'total_artists': len(artist)})

def RegirtrationPage(request):
    return render(request,"app/pages-register.html")

def LoginPage(request):
    return render(request,"app/pages-login.html")

def RegisterUser(request):
    try:
        if request.POST['role']=="User":
            email = request.POST['email']
            role = request.POST['role']
            password = request.POST['password']
            fname = request.POST['fname']
            lname = request.POST['lname']
            cpassword = request.POST['cpassword']
            
            contact = request.POST['contact']
            address = request.POST['address']
            

            

            user = Admin.objects.filter(Email=email)
            if user:
                message = "User already exist"
                return render(request,"app/pages-register.html",{'msg':message})
            else:
                if password==cpassword:
                    
                    newuser = Admin.objects.create(Role=role,Email=email,Password=password)
                    newemp = User.objects.create(admin_id=newuser,Firstname=fname,Lastname=lname,Contact=contact,Address=address)
                    return render(request,"app/pages-login.html")
                else:
                    message = "Password and Cpassword doesn't same"
                    return render(request,"app/pages-register.html",{'msg':message})

        else:
            if request.POST['role']=="Artist":
                print("-----------------try------------------")
                email = request.POST['email']
                role = request.POST['role']
                password = request.POST['password']
                fname = request.POST['fname']
                print(f"-----fname------{fname}----------------")
                lname = request.POST['lname']
                cpassword = request.POST['cpassword']
               
                contact = request.POST['contact']
                address = request.POST['address']

                user = Admin.objects.filter(Email=email)
                if user:
                    message = "User already exist"
                    return render(request,"app/pages-register.html",{'msg':message})
                else:
                    if password==cpassword:
                        
                        newuser = Admin.objects.create(Role=role,Email=email,Password=password)
                        newemp = Artist.objects.create(admin_id=newuser,Firstname=fname,Lastname=lname,Contact=contact,Address=address)
                        return render(request,"app/pages-login.html")
                    else:
                        message = "Password and Cpassword doesn't same"
                        return render(request,"app/pages-register.html",{'msg':message})
    except Exception as e1:
        print("Artist Registration Exception ---------->",e1)
        return render(request, "app/pages-register.html")

def LoginUser(request):
    try:
        if request.POST['role'] == "User":
            print("-----------------try------------------")

            email = request.POST['email']
            password = request.POST['password']

            user = Admin.objects.get(Email=email)
            artists = Admin.objects.filter(Role="Artist")
            artist = Artist.objects.all()

            if user.Password == password and user.Role == "User":

                emp = User.objects.get(admin_id=user)
                print(f"********************:{emp}")
                request.session['Email'] = user.Email
                request.session['Firstname'] = emp.Firstname
                request.session['Lastname'] = emp.Lastname
                request.session['id'] = user.id
                request.session['uid'] = emp.id
                request.session['Role'] = user.Role
                try:
                    print("Try Called")
                    request.session['user_image'] = emp.image.url
                except:
                    print("Except Called")
                    pass

                print(len(artists))
                data = {'artist': artist, 'person': emp,
                    'artists': artists, 'total_artists': len(artists)}
                return render(request, "app/index-1.html", data)
            else:
                message = "Password and Role doesn't match"
                return render(request, "app/pages-login.html", {'msg': message})
        else:
            if request.POST['role']=="Artist":
                print("-----------------try------------------")
                email = request.POST['email']
                password = request.POST['password']

                user = Admin.objects.get(Email=email)
                
                if user.Password==password and user.Role=="Artist":
                    hir=Artist.objects.get(admin_id=user)
                    request.session['Email']=user.Email
                    request.session['Firstname']=hir.Firstname
                    request.session['Lastname']=hir.Lastname
                    request.session['id']=user.id
                    print("Session : ",request.session['id'])
                    request.session['aid'] = hir.id
                    request.session['Role']=user.Role
                    try:
                        print("Try Called")
                        request.session['artist_image']=hir.image.url
                    except:
                        print("Except Called")
                        pass
                    
                    return render(request,"app/dashboard.html",{'person':hir})

            else:
                message = "Password and Role doesn't match"
                return render(request,"app/pages-login.html",{'msg':message})
    except Exception as e1:
        print("Login Exception....",e1)
        return render(request, "app/pages-login.html")


def DashboardSettingPage(request,pk):
    edata = Admin.objects.get(id=pk)
    print(f"edata:{edata}")
    user_data = Artist.objects.get(admin_id=edata.id)
    print(f"artist_fname:{user_data}")
    print("Session : ", request.session['id'])
    user = Artist.objects.filter(admin_id=edata.id)
    return render(request, "app/dashboard-settings.html", {'user_data': user_data,'user':user})


def EditPage(request, pk):
    Rdata = Admin.objects.get(id=pk)
    print("--------RData:", Rdata)
    udata = Admin.objects.get(id=pk)

    user_data = Artist.objects.get(admin_id=udata.id)

    return render(request, "app/dashboard-settings-edit.html", {'user_data': user_data, 'role': Rdata.Role})


def UpdateData(request, pk):
    udata = Admin.objects.get(id=pk)
    user_data = Artist.objects.get(admin_id=udata.id)
    skills = request.POST['skills']
    
    user_data.Firstname = request.POST['fname'] if request.POST['fname'] else user_data.Firstname
    user_data.Lastname = request.POST['lname'] if request.POST['lname'] else user_data.Lastname
    udata.Email = request.POST['email'] if request.POST['email'] else udata.Email
    try:
        user_data.image = request.FILES['image'] if request.FILES['image'] else user_data.image
    except:
        pass
    user_data.Address = request.POST['address'] if request.POST['address'] else user_data.Address

    user_data.AboutMe = request.POST['aboutme'] if request.POST['aboutme'] else user_data.AboutMe
    user_data.Tagline = request.POST['tagline'] if request.POST['tagline'] else user_data.Tagline
    user_data.Nationality = request.POST['nationality'] if request.POST['nationality'] else user_data.Nationality

    user_data.Skills = skills
    user_data.save()

    saveuser = "Null"
    saveuser_email = "Null"
    if request.POST['fname'] or request.POST['lname'] or request.POST['email'] or request.POST['address'] or request.POST['aboutme']:
        saveuser = user_data.save()
        saveuser_email = udata.save()
        request.session['Firstname'] = user_data.Firstname
        request.session['Lastname'] = user_data.Lastname
        request.session['Email'] = udata.Email
        request.session['artist_image'] = user_data.image.url
        request.session['AboutMe'] = user_data.AboutMe
        url = f"/setting/{udata.id}"
        return redirect(url)

    return render(request, "app/dashboard-settings-edit.html", {'user_data': user_data})


def Logoutpage(request):

    del request.session['Email']
    del request.session['id']
    del request.session['Firstname']
    del request.session['Lastname']
    del request.session['Role']
    return redirect(IndexPage)


def DashboardSettingUser(request,pk):
    edata=Admin.objects.get(id=pk)
    print(f"edata:{edata}")
    user_data = User.objects.get(admin_id=edata.id)
    print(f"user_fname:{user_data.Firstname}")
    return render(request, "app/dashboard-settings-user.html",{'user_data': user_data})


def DashboardSettingUserEdit(request,pk):
    Rdata = Admin.objects.get(id=pk)
    print("--------RData:", Rdata)
    udata = Admin.objects.get(id=pk)

    user_data = User.objects.get(admin_id=udata.id)
    return render(request, "app/dashboard-settings-user-edit.html", {'user_data': user_data, 'role': Rdata.Role})


def UpdateDataUser(request,pk):
    udata = Admin.objects.get(id=pk)
    user_data = User.objects.get(admin_id=udata.id)

    user_data.Firstname = request.POST['fname'] if request.POST['fname'] else user_data.Firstname
    user_data.Lastname = request.POST['lname'] if request.POST['lname'] else user_data.Lastname
    user_data.Address = request.POST['address'] if request.POST['address'] else user_data.Address
    udata.Email = request.POST['email'] if request.POST['email'] else user_data.Email
    udata.Contact = request.POST['contact'] if request.POST['contact'] else user_data.Contact
    try:
        user_data.image = request.FILES['image'] if request.FILES['image'] else user_data.image
    except:
        pass
    user_data.save()
    udata.save()
    request.session['Firstname'] = user_data.Firstname
    request.session['Lastname'] = user_data.Lastname
    request.session['Email'] = udata.Email
    request.session['user_image'] = user_data.image.url
    url = f"/settinguser/{udata.id}"
    return redirect(url)
    return render(request, "app/dashboard-settings-user-edit.html", {'user_data': user_data})





def Dashboard(request):
    accept = WorkRequest.objects.filter(Validatereq="Accept")
    all_req = WorkRequest.objects.filter(Validatereq="pending")
    artist = Artist.objects.all()
    return render(request, "app/dashboard.html",{'accept':len(accept),'pending':len(all_req),'artist':artist})





def DashboardCandidates(request):
    artist_id = request.session['id']
    print(artist_id)
    get_artist = Artist.objects.get(admin_id=artist_id)
    print("GET ARTIST:", get_artist.id)
    all_req = WorkRequest.objects.filter(
        artist_id=get_artist.id, Validatereq="pending")
    print("ALL REQUEST:", all_req)
    artist = Artist.objects.all()
    # print(artist_id, get_artist.admin_id.pk)
    # print(get_artist.admin_id.Email)
    # for i in all_req:
    #    print(i.user.pk)

    return render(request, "app/dashboard-manage-candidates.html", {'work_request': all_req, 'total_req': len(all_req),'artist':artist})


def RequestStatus(request, pk):
    if request.method == "POST":
        request_status = request.POST['workreq']
        workreq = WorkRequest.objects.get(id=pk)
        print("==============================", request_status)
        print("===============request===============", workreq.Message)
        if request_status == "Accept":
            print("ACCEPTED")
            workreq.Validatereq = "Accept"
            workreq.save()
        elif request_status == "Reject":
            print("REJECTTED")
            workreq.Validatereq = "Reject"
            workreq.save()
        return redirect("candidate")


def UserAllRequest(request):
    user_id = request.session['id']
    print(user_id)
    get_user = User.objects.get(admin_id=user_id)
    print(get_user)
    ar_req = WorkRequest.objects.filter(user_id=get_user.id)
    print("Request", ar_req)
    return render(request, "app/user-all-request.html", {'workrequest': ar_req[::-1], 'total_req': len(ar_req)})

    return render(request, "app/user-all-request.html")


def Dashboardjobs(request):
    artist_id = request.session['id']
    print(artist_id)
    get_artist = Artist.objects.get(admin_id=artist_id)
    print("GET ARTIST:", get_artist.id)
    all_req = WorkRequest.objects.filter(
        artist_id=get_artist.id, Validatereq="Accept")
    print("ALL REQUEST:", all_req)
    artist = Artist.objects.all()
    return render(request, "app/dashboard-manage-jobs.html", {'work_request': all_req, 'total_req': len(all_req),'artist':artist})

    return render(request, "app/dashboard-manage-jobs.html")





def DashboardMsg(request):
    return render(request, "app/dashboard-messages.html")




def view_art_post(request):
    admin = Admin.objects.get(Email=request.session['Email'])
    artist = Artist.objects.get(admin_id=admin)
    post = Post.objects.filter(artist=artist)
    return render(request, "app/view_art_post.html", {'post': post[::-1]})

def add_art_post(request):
    if request.method == "POST":
        admin = Admin.objects.get(Email=request.session['Email'])
        artist = Artist.objects.get(admin_id=admin)
        Post.objects.create(
            artist=artist,
            post_name=request.POST['post_name'],
            post_desc=request.POST['post_desc'],
            post_image=request.FILES['post_image']
        )
        msg = "post added"
        return HttpResponseRedirect(reverse('view_art_post'))
    else:
        return HttpResponseRedirect(reverse('view_art_post'))

def view_art_post_details(request,pk):
    admin = Admin.objects.get(Email=request.session['Email'])
    print(admin)
    artist=Artist.objects.get(admin_id=admin)
    post=Post.objects.get(artist=artist,pk=pk)
    return render(request,"app/view_art_post_details.html",{'post':post})

def view_art_post_edit(request,pk):
    admin = Admin.objects.get(Email=request.session['Email'])
    print(admin)
    artist=Artist.objects.get(admin_id=admin)
    post=Post.objects.get(artist=artist,pk=pk)
    if request.method=="POST":
        post.post_name=request.POST['post_name']
        post.post_desc=request.POST['post_desc']
        try:
            post.post_image=request.FILES['post_image']
        except:
            pass
        post.save()
        post=Post.objects.get(artist=artist,pk=pk)
        return render(request,'app/view_art_post_details.html',{'post':post})

    else:
        return render(request,'app/view_art_post_details.html',{'post':post})

def art_post_delete(request,pk):
    admin = Admin.objects.get(Email=request.session['Email'])
    artist=Artist.objects.get(admin_id=admin)
    post=Post.objects.get(artist=artist,pk=pk)
    post.delete()
    return HttpResponseRedirect(reverse('view_art_post'))


def user_art_post_detail(request, pk):
    post = Post.objects.get(pk=pk)   
    return render(request, "app/user_art_post_detail.html",{'post':post})

def user_view_all_products(request,pk):
    product = Product.objects.filter(post_artist=pk)   
    return render(request, "app/user_view_all_products.html",{'product':product})

def user_view_all_post(request,pk):
    post = Post.objects.filter(artist=pk)   
    return render(request, "app/user_view_all_post.html",{'post':post})











def posts(request):
    products = view_post(request)
    print("HELLO", products)
    return render(request, "app/artist-post.html", {'products': products})



def view_post(request):
    admin = Admin.objects.get(Email=request.session['Email'])
    artist = Artist.objects.get(admin_id=admin)
    products = Product.objects.filter(post_artist=artist)
    return render(request, "app/artist-post.html", {'products': products[::-1]})


def add_post(request):
    if request.method == "POST":
        user = Admin.objects.get(Email=request.session['Email'])
        artist = Artist.objects.get(admin_id=user)
        Product.objects.create(
            post_artist=artist,
            title=request.POST['title'],
            # product_author=request.POST['product_author'],
            art_price=request.POST['art_price'],
            art_desc=request.POST['art_desc'],
            art_image=request.FILES['art_image']
        )
        
        return HttpResponseRedirect(reverse('view-post'))
    else:
        return HttpResponseRedirect(reverse('view-post'))

def user_post_detail(request, pk):
    wlist_flag=True
    cart_flag=True
    cart_qty = 0
    product = Product.objects.get(pk=pk)
    try:
        user = Admin.objects.get(Email=request.session['Email'])
        wishlist=WishList.objects.get(product=product,user=user)
        if wishlist:
            wlist_flag=False
    except Exception as e:
        print(e)

    try:
        admin=Admin.objects.get(id=request.session['id'])
        user =User.objects.get(admin_id=admin)
        cart=AddCart.objects.get(product=product,user=user)
        if cart:
            cart_flag=False
            cart_qty = int(cart.qty)
    except Exception as e:
        print(e)

    wlist = load_wishlist(request)
    cart = load_cart(request)
    
    return render(request, "app/user_post_detail.html",{'product':product, 'cart_qty':cart_qty, 'cart_flag':cart_flag, 'cart': cart , 'total_cart': len(cart), 'wlist_flag': wlist_flag, 'wlist':wlist, 'total_wlist': len(wlist)})

def update_cart(request,pk):
    print(pk)
    product=Product.objects.get(pk=pk)
    admin = Admin.objects.get(Email=request.session['Email'])
    user = User.objects.get(admin_id=admin)
    cart = AddCart.objects.get(product=product, user=user)
    cart.qty = request.POST['qty']
    cart.price = product.art_price
    cart.total = int(request.POST['qty']) * product.art_price
    cart.save()
    return redirect('mycart')


def mycart(request):
    admin = Admin.objects.get(id=request.session['id'])
    user = User.objects.get(admin_id=admin)
    cart = AddCart.objects.filter(user=user)
    wlist = load_wishlist(request)
    carts = load_cart(request)
    sub_total = 0
    for i in cart:
        sub_total = sub_total + i.total
    return render(request,"app/mycart.html",{'cart':cart, 'cart_amt': sub_total , 'total_wlist': len(wlist), 'total_cart': len(cart)})

def add_to_cart(request,pk):
    product=Product.objects.get(pk=pk)
    admin=Admin.objects.get(id=request.session['id'])
    user =User.objects.get(admin_id=admin)
    addcart = AddCart.objects.create(product=product,user=user,price=product.art_price,total=product.art_price)
    return redirect('mycart')
    

def load_cart(request):
    admin=Admin.objects.get(id=request.session['id'])
    user =User.objects.get(admin_id=admin)
    cart=AddCart.objects.filter(user=user)
    request.session['total_cart'] = len(cart)
    #print(cart)
    return cart

def remove_from_cart(request,pk):
    product=Product.objects.get(pk=pk)
    admin = Admin.objects.get(id=request.session['id'])
    user =User.objects.get(admin_id=admin)
    cart = AddCart.objects.get(product=product, user=user)
    cart.delete()
    return redirect('mycart')

def wishlist(request):
    user = Admin.objects.get(Email=request.session['Email'])
    wishlist = WishList.objects.filter(user=user)
    wlist = load_wishlist(request)
    return render(request, 'app/wishlist.html', {'wishlist': wishlist[::-1], 'total_wlist': len(wishlist)})


def add_to_wishlist(request,pk):
    product = Product.objects.get(pk=pk)
    admin = Admin.objects.get(Email=request.session['Email'])
    WishList.objects.create(product=product, user=admin)
    return redirect('wishlist')

def load_wishlist(request):
    user = Admin.objects.get(Email=request.session['Email'])
    wishlist = WishList.objects.filter(user=user)
    request.session['total_wlist'] = len(wishlist)
    return wishlist

def remove_from_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user = Admin.objects.get(Email=request.session['Email'])
    wishlist = WishList.objects.get(product=product,user=user)
    wishlist.delete()
    return redirect('wishlist')

def post_detail(request,pk):
    admin = Admin.objects.get(Email=request.session['Email'])
    print(admin)
    artist=Artist.objects.get(admin_id=admin)
    product=Product.objects.get(post_artist=artist,pk=pk)
    return render(request,"app/post-details.html",{'product':product})


def post_edit(request,pk):
    admin = Admin.objects.get(Email=request.session['Email'])
    print(admin)
    artist=Artist.objects.get(admin_id=admin)
    product=Product.objects.get(post_artist=artist,pk=pk)
    if request.method=="POST":
        product.title=request.POST['title']
        product.art_price=request.POST['art_price']
        product.art_desc=request.POST['art_desc']
        try:
            product.art_image=request.FILES['art_image']
        except:
            pass
        product.save()
        product=Product.objects.get(post_artist=artist,pk=pk)
        return render(request,'app/post-details.html',{'product':product})

    else:
        return render(request,'app/show11.html',{'product':product})


def post_delete(request,pk):
    admin = Admin.objects.get(Email=request.session['Email'])
    artist=Artist.objects.get(admin_id=admin)
    product=Product.objects.get(post_artist=artist,pk=pk)
    product.delete()
    #return render(request,'app/artist-post.html',{'product':view_post(request), 'total_products': view_post(request)})
    return HttpResponseRedirect(reverse('view-post'))

def all_post_view(request):
    all_data=Product.objects.all()
    return render(request,"app/all-post.html",{'all':all_data}) 

def freelancersFullLayout(request):
    all_artist_data = Artist.objects.all()
    return render(request,"app/freelancers-grid-layout-full-page.html",{'artist_data':all_artist_data})






def Pages404(request):
    return render(request,"app/pages-404.html")


def PagesCheckout(request):
    return render(request,"app/pages-checkout-page.html")

def PagesContact(request):
    return render(request,"app/pages-contact.html")


def PagesTemplate(request):
    return render(request,"app/pages-invoice-template.html")


def change_reviews(request):
    return render(request, "app/single-freelancer-profile.html")


def DashboardReviews(request):
    admin = Admin.objects.get(Email=request.session['Email'])
    #print(admin)
    artist = Artist.objects.get(admin_id=admin)
    print("---> artist",artist)
    fall = Feedback.objects.all().filter(artist=artist)
    #print("---->>> fall",fall)
    r_fb=ReplyFeedback.objects.all().filter(artist=artist)
    #print("--->> r_fb",r_fb[0].f_id)
    print("\n\n---> fall # ",fall)
    print("\n -->>reply ",r_fb)
    for i in fall:
        for j in r_fb:
            if i.id == j.f_id.id:
                print("--->>>Reply is there")
            else:
                print("<<----not available")
    return render(request, "app/dashboard-reviews.html",{'fall':fall,'r_fb':r_fb})


def artist_reply(request):
    reply = request.POST['reply']
    fid = request.POST['feedbackid']
    uid = request.POST['usernameid']
    print("======>>> id ",id)
    print("------>>> fid",fid)
    u_id = User.objects.get(id=uid)
    admin_id = Admin.objects.get(Email=request.session['Email'])
    a_id = Artist.objects.get(admin_id=admin_id)
    f_id = Feedback.objects.get(id=fid)
    
    r_id = ReplyFeedback.objects.create(user=u_id,artist=a_id,reply=reply,f_id=f_id)
    print("---->>>> id inside the feedback",id)
    return render(request, "app/dashboard-reviews.html",{'reply':reply})

def all_feedback(request,pk):
    fall = Feedback.objects.filter(artist=pk)
    return render(request,"app/view_all_feedback.html",{'fall':fall})


def feedback(request):
    rating = request.POST['star']
    review = request.POST['desc']
    title = request.POST['title']
    id = request.POST['artistname']
    a_id = Artist.objects.get(id=id)
    admin_id = Admin.objects.get(Email=request.session['Email'])
    u_id = User.objects.get(admin_id=admin_id)
    fid = Feedback.objects.create(artist=a_id,user=u_id,Message=review,rating=int(rating),title=title)
    
    print("---->>>> id inside the feedback",id)
    return HttpResponseRedirect(reverse('freelancer-full-profile',args=(id)))

def FreelancerFullProfile(request,pk):
    print("---------------> pk",pk)
    all_artist_data = Artist.objects.get(id=pk)
    user = Artist.objects.filter(id=pk)
    products = Product.objects.filter(post_artist=all_artist_data).order_by('id')[:5]
    fall = Feedback.objects.filter(artist=pk).order_by('-id')[:5]
    rall = ReplyFeedback.objects.all()
    post = Post.objects.filter(artist=all_artist_data).order_by('id')[:3]
    return render(request,"app/single-freelancer-profile.html",{'key7':all_artist_data,'fall':fall,'user':user,'products':products[::-1],'rall':rall,'post':post})

def RequestPopUp(request):
    if request.method == 'POST':
        artist_mail = request.POST['artist-email']
        user_mail = request.POST['user-email']
        message = request.POST['message']
        pk = request.POST['pk']
        print("ARTIST EMAIL:",artist_mail)
        
        mail_artist = Admin.objects.get(Email = artist_mail)
        get_artist = Artist.objects.get(admin_id=mail_artist)

        mail_user = Admin.objects.get(Email = user_mail)
        get_user = User.objects.get(admin_id=mail_user)
        artist_data = Artist.objects.get(admin_id=mail_artist)
        
        print(f"Artist={mail_artist.Email}\nUser={mail_user.Email}")
        savereq = WorkRequest.objects.create(artist=get_artist,user=get_user,Message=message)
        msg = "Your request is sended"
        print(msg)
        # return render(request,"app/single-freelancer-profile.html",{'key7':artist_data,'msg':msg})
        all_artist_data = Artist.objects.get(id=pk)
        user = Artist.objects.filter(admin_id=mail_artist)
        products = Product.objects.filter(post_artist=artist_data).order_by('id')[:5]
        fall = Feedback.objects.filter(artist=pk).order_by('-id')[:5]
        rall = ReplyFeedback.objects.all()
        return render(request,"app/single-freelancer-profile.html",{'key7':artist_data,'key8':all_artist_data,'fall':fall,'user':user,'products':products[::-1],'rall':rall,'msg':msg})



def ForgotPassword(request):
    return render(request,"app/forgot-password.html")

def ForgotPasswordPage(request):
   # try:
    if request.method == "POST":
        role = request.POST['role']
        email = request.POST['email']
        print(f"role={role}\nemail={email}")
        
        user = Admin.objects.filter(Email=email,Role=role)
        print("=====================USER",user)
        if len(user) > 0:
            print("CONDTION TRUE------------------")
            if user[0].Role == "User":
                print("CONDTION TRUE--123----------------")
                otp =random.randint(100000,999999)
                email_subject="User Verification"
                sendmail(email_subject,"mail_templates",email,{'otp':otp})
                user[0].otp = otp
                user[0].save()
                return render(request,"app/new-password.html",{"data" : user[0]})
            
            elif user[0].Role == "Artist":
                print("CONDTION TRUE--456----------------")
                # password == cpassword:
                otp =random.randint(100000,999999)
                # newuser = Admin.objects.create(Email=email,Otp=otp)
                email_subject="Artist Verification"
                sendmail(email_subject,"mail_templates",email,{'otp':otp})
                user[0].otp = otp
                user[0].save()
                return render(request,"app/new-password.html",{"data" : user[0]})
        else:
            if len(user) == 0:
                msg = "User and role doesn't match"
                return render(request,"app/forgot-password.html",{"msg":msg})
            
            # print("EEEEEELLLLLLLSSSSSSSSSSEEEEEEEEE")
            # msg = "User doesn't exist"
            # return render(request,"app/forgot-password.html",{"msg":msg})
    
    # except Exception as error:
        # print(f"Forgot-Password-Exception--------------------->{error}")
 
def validateotp(request):
    if request.method == "POST":
        role = request.POST['role']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['cpassword']
        u_otp = request.POST['otp']
        print(f"role={role}\nemail={email}")
        
        user = Admin.objects.filter(Email=email,Role=role)
        if len(user) > 0:
            if user[0].Role == "User":
                if (user[0].otp == int(u_otp)):
                    print("============OTP VALIDATED===============")
                    if password==c_password:
                        user[0].Password = password
                        user[0].save()
                        return render(request,"app/pages-login.html")
                    else:
                        msg = 'Your password and confirm password does not match'
                        return render(request,"app/new-password.html",{"data" : user[0],"msg":msg})
                else:
                    msg = 'Your OTP is incorrect'
                    return render(request,"app/new-password.html",{"data" : user[0],"msg":msg})
                
                return render(request,"app/new-password.html",{"data" : user[0]})
            
            elif user[0].Role == "Artist":
                if (user[0].otp == int(u_otp)):
                    if password==c_password:
                        user[0].Password = password
                        user[0].save()
                        return render(request,"app/pages-login.html")
                    else:
                        msg = 'Your password and confirm password does not match'
                        return render(request,"app/new-password.html",{"data" : user[0],"msg":msg})
                else:
                    msg = 'Your OTP is incorrect'
                    return render(request,"app/new-password.html",{"data" : user[0],"msg":msg})
                return render(request,"app/new-password.html",{"data" : user[0]})
        else:
            if len(user) == 0:
                msg = "User and role doesn't match"
                return render(request,"app/forgot-password.html",{"msg":msg})

def NewPassword(request):
    return render(request,"app/new-password.html") 
    # return HttpResponseRedirect(reverse('newpassword'))    



    ####### Admin #######

def AdminPage(request):
    print(request.method)
    if request.method == 'POST':
        uname = request.POST['uname']
        password = request.POST['password']
        print(uname, password)

        if uname == 'admin' and password == 'admin' :
            request.session['uname'] = uname
            request.session['password'] = password
            return render(request,"app/admin/a_index.html")
        else:
            message = "uname or Password are incorrect"
            print("*******")
            return render(request,"app/admin/login-register.html",{'msg':message})
    else:
        print('else')
        return render(request,"app/admin/login-register.html")


def AIndex(request):
    return render(request,"app/admin/a_index.html") 


def Inbox(request):
    return render(request,"app/admin/inbox.html") 

#####   Email   ########

def ViewEmail(request):
    return render(request,"app/admin/view-email.html") 

def ComposeEmail(request):
    return render(request,"app/admin/compose-email.html") 

#############   Interface    ############

def Animations(request):
    return render(request,"app/admin/animations.html")

def GoogleMap(request):
    return render(request,"app/admin/google-map.html")

def DataMap(request):
    return render(request,"app/admin/data-map.html")

def CodeEditor(request):
    return render(request,"app/admin/code-editor.html")

def ImageCropper(request):
    return render(request,"app/admin/image-cropper.html")

def Wizard(request):
    return render(request,"app//admin/wizard.html")


###############  charts  #############

def FlotCharts(request):
    return render(request,"app/admin/flot-charts.html")

def BarCharts(request):
    return render(request,"app/admin/bar-charts.html")

def LineCharts(request):
    return render(request,"app/admin/line-charts.html")

def AreaCharts(request):
    return render(request,"app/admin/area-charts.html")



###############  Tables  #############

def NormalTable(request):
    all_data = Artist.objects.all()
    return render(request,"app/admin/normal-table.html",{'a_1':all_data})

def DataTable(request):
    user_data = Artist.objects.all()
    return render(request,"app/admin/data-table.html",{'a_2':user_data})

def AdminEditPage(request,pk):
    edata = Artist.objects.get(pk=pk)
    return render(request,"app/admin/edit.html",{'key11':edata})

def AdminUpdateData(request,pk):
    print("UPdate----->",pk)
    udata = Admin.objects.get(id=pk)
    udata.is_active=request.POST['is_active']  
    udata.is_verified=request.POST['is_verifed']      
    udata.save()
    return HttpResponseRedirect(reverse('datatable'))

def AdminDeleteData(request,pk):
    ddata = Artist.objects.get(pk=pk)
    ddata.delete()
    return HttpResponseRedirect(reverse('datatable'))


###############  Forms  #############

def FormElements(request):
    return render(request,"app/admin/form-elements.html")

def FormComponents(request):
    return render(request,"app/admin/form-components.html")

def FormExamples(request):
    return render(request,"app/admin/form-examples.html")


###############  AppViews  #############

def Notification(request):
    return render(request,"app/admin/notification.html")

def Alert(request):
    return render(request,"app/admin/alert.html")
 
def Modals(request):
    return render(request,"app/admin/modals.html")

def Buttons(request):
    return render(request,"app/admin/buttons.html")

def Tabs(request):
    return render(request,"app/admin/tabs.html")

def Accordion(request):
    return render(request,"app/admin/accordion.html")

def Dialog(request):
    return render(request,"app/admin/dialog.html")

def Popovers(request):
    return render(request,"app/admin/popovers.html")

def ToolTips(request):
    return render(request,"app/admin/tooltips.html")

def DropDown(request):
    return render(request,"app/admin/dropdown.html")


#################   Pages   ###################

def Contact(request):
    return render(request,"app/admin/contact.html")

def Invoice(request):
    return render(request,"app/admin/invoice.html")

def Typography(request):
    return render(request,"app/admin/typography.html")

def Color(request):
    return render(request,"app/admin/color.html")


####### Paytm Block ##########


def initiate_payment(request):
    
    try:
        udata = Admin.objects.get(Email=request.session['Email'])
        print("------------>",udata)
        amount = int(request.POST['total'])
        print("------------>",amount)
    except Exception as err:
        print(err)
        return render(request, 'app/mycart.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=udata, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    
    print('SENT: ', checksum)
    return render(request, 'app/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app/callback.html', context=received_data)
        return render(request, 'app/callback.html', context=received_data)

def add_response(request,pk,status):
    admin = Admin.objects.get(Email=request.session['Email'])
    #print(admin)
    artist = Artist.objects.get(admin_id=admin)
    print("---> artist",artist)
    fall = Feedback.objects.all().filter(artist=artist)
    #print("---->>> fall",fall)
    r_fb=ReplyFeedback.objects.all().filter(artist=artist)

    #print("--->> r_fb",r_fb[0].f_id)
    print("\n\n---> fall # ",fall)
    print("\n -->>reply ",r_fb)
    
    fid = Feedback.objects.get(id=pk)
    fid.status=status
    fid.save()
    return HttpResponseRedirect(reverse('reviews'))

    