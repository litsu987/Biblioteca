from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=50)
    center = models.CharField(max_length=100)
    cycle = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Catalog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    catalog_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to='catalog_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class CatalogItem(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0)
    # Add other specific attributes for each catalog item type

class Copy(models.Model):
    catalog_item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # Available, Reserved, Loaned
    location = models.CharField(max_length=100)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100)
    details = models.TextField()
    status = models.CharField(max_length=50)

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.action}"
