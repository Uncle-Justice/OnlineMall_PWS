from django.db import models
import uuid
# Create your models here.

#TODO: specification may need to use one to many relationship, to prevent accident revise
class specification(models.Model):
    name=models.CharField('name',max_length=30)
    def __str__(self):
        return self.name

class option(models.Model):
    name=models.CharField('name',max_length=30)
    belong=models.ForeignKey(specification,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class catagory(models.Model):
    name=models.CharField('name',max_length=30)
    def __str__(self):
        return self.name

class store(models.Model):
    store_id=models.UUIDField('store_id',primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField('name',max_length=50)
    description=models.TextField('description')
    def __str__(self):
        return self.name

class SPU(models.Model):
    SPU_id=models.UUIDField('SPU_id',primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField('name',max_length=50)
    description=models.TextField('description')
    catagories=models.ManyToManyField(catagory)
    spec=models.ManyToManyField(specification)
    belong=models.ForeignKey(store,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class SKU(models.Model):
    SKU_id=models.UUIDField('SKU_id',primary_key=True, default=uuid.uuid4, editable=False)
    price=models.IntegerField('price')
    amount=models.IntegerField('amount')
    options=models.ManyToManyField(option)
    belong=models.ForeignKey(SPU,on_delete=models.CASCADE)
    def __str__(self):
        s=str(self.belong.name)
        for opt in self.options.all():
            s+="#"+opt.name
        return str(s)

class img(models.Model):
    URL=models.CharField('URL',max_length=200)
    belong=models.ForeignKey(SKU,on_delete=models.CASCADE)


class customer(models.Model):
    uuid=models.UUIDField('customer_id',primary_key=True, default=uuid.uuid4, editable=False)
    openid=models.CharField('openid',default='',max_length=100)
    nickname=models.CharField('nickname',max_length=50)
    address=models.CharField('address',max_length=100)
    phone_number=models.CharField('phone_number',max_length=20)
    def __str__(self):
        return str(self.uuid)+'#'+self.nickname

class order(models.Model):
    order_id=models.UUIDField('order_id',primary_key=True, default=uuid.uuid4, editable=False)
    price=models.IntegerField('price')
    create_time=models.TimeField('create_time')
    payment_time=models.TimeField('payment_time')
    confirm_time=models.TimeField('confirm_time')
    belong=models.ForeignKey(customer,on_delete=models.CASCADE)
    def __str__(self):
        return self.order_id


class item(models.Model):
    toSKU=models.ForeignKey(SKU,on_delete=models.CASCADE)
    toCustomer=models.ForeignKey(customer,related_name='cart',on_delete=models.CASCADE)
    number=models.IntegerField('number')
    def __str__(self):
        return str(self.toSKU.belong.name)+'#'+str(self.number)