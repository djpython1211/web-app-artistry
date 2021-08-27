from django.db import models


# Create your models here.

class Admin(models.Model):
    Email=models.EmailField(max_length=50)
    Password=models.CharField(max_length=50)
    Role=models.CharField(max_length=50)
    is_created = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    otp = models.IntegerField(default=123)
    

class Artist(models.Model):
    admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE)
    Firstname=models.CharField(max_length=50)
    Lastname=models.CharField(max_length=50)
    Contact=models.BigIntegerField()
    Address=models.CharField(max_length=100)
    image = models.ImageField(default="img/default.jpg", upload_to="img/")
    AboutMe =models.CharField(max_length=10000,default="abc")
    Tagline =models.CharField(max_length=100,default="abc")
    Nationality = models.CharField(max_length=100,default="None")
    Skills = models.CharField(max_length=100,default="None")
    Gender = models.CharField(max_length=10,default="other")
    is_req_created = models.DateTimeField(auto_now_add=True,null=True)
    

class User(models.Model):
    admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE)
    Firstname=models.CharField(max_length=50)
    Lastname=models.CharField(max_length=50)
    Contact=models.BigIntegerField()
    Address=models.CharField(max_length=100)
    image = models.ImageField(default="img/default.jpg",upload_to="img/")
    Gender = models.CharField(max_length=10,default="other")

class WorkRequest(models.Model): 
    artist=models.ForeignKey(Artist,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Message = models.CharField(max_length=500)
    Validatereq = models.CharField(max_length=20,default="pending")
    is_created = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    artist=models.ForeignKey(Artist,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Message = models.CharField(max_length=500)
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(default="pending",max_length=20)

class ReplyFeedback(models.Model):
    artist=models.ForeignKey(Artist,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    f_id=models.ForeignKey(Feedback,on_delete=models.CASCADE)
    reply = models.CharField(max_length=500,default="None")
    date = models.DateTimeField(auto_now=True)

    

class Product(models.Model):
    post_artist = models.ForeignKey(Artist,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    #product_author = models.CharField(max_length=100)
    #product_author = models.CharField(max_length=100)
    art_price = models.IntegerField()
    art_desc = models.TextField()
    art_image = models.ImageField(upload_to='artist_posts/')

    def __str__(self):
        return self.post_artist

class Post(models.Model):
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE)
    post_name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    post_desc = models.TextField()
    post_image = models.ImageField(upload_to='artist_post/')

    def __str__(self):
        return self.artist

class WishList(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	user=models.ForeignKey(Admin,on_delete=models.CASCADE)
	date=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.title+" - "+self.user.Firstname

class AddCart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    qty=models.CharField(max_length=10, default="1")
    price = models.CharField(max_length=10, default="0")
    total = models.BigIntegerField(default="0")

class Transaction(models.Model):
    made_by = models.ForeignKey(Admin, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

