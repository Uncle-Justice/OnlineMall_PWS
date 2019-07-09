from django.shortcuts import render
from django.http import HttpResponse
import requests as rq
import json
import main.models as models
from django.db.models import ObjectDoesNotExist
# Create your views here.

def login(request):
    if (request.method=='POST'):
        d=json.loads(request.body)
        code=d.get('code',None)
        if (code!=None):
            response=rq.get("https://api.weixin.qq.com/sns/jscode2session",params={'appid':'wx3297461e99ff27c4','secret':'b5e3c057d578ba17b7e2a0a719b34670','js_code':code,'grant_type':'authorization_code'})
            response.encoding='UTF-8'
            info=response.json()
            id=info.get('id',None)
            if (id!=None):
                (user,exist)=models.customer.objects.get_or_create(openid=id)
                return HttpResponse(json.dumps({'token':user.uuid,'openid':info.get('openid','null')}))
    return HttpResponse("Error")

# 改动
def catagorieslist(request):
    l=[]
    for i in models.catagory.objects.all():
        l.append({'id':i.id,'name':i.name,'description':'','img':{'url':''}})
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getCatagory(request):
    l=[]
    cname=request.GET.get('id',None)
    if cname==None:
        return HttpResponse("error")
    try:
        catagory=models.catagory.objects.get(id=cname)
        for i in catagory.spu_set.all():
            l.append({'name':i.name,'store':i.belong.name,'id':str(i.SPU_id)})
    except ObjectDoesNotExist:
        l['error']='Catagory does not exist'
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getCatagoryById(request,cid):
    l=[]
    try:
        catagory=models.catagory.objects.get(id=cid)
        for i in catagory.spu_set.all():
            for j in i.sku_set.all():
                for k in j.img_set.all():
                    URL= k.URL
            l.append({'id':str(i.SPU_id),'name':i.name,'store':i.belong.name,'main_img_url':'http://127.0.0.1:8000/static/images/'+URL})
    except ObjectDoesNotExist:
        l['error']='Catagory does not exist'
    return HttpResponse(json.dumps(l,ensure_ascii=False))

# 改动
def SPUlist(request):
    l=[]
    for i in models.SPU.objects.all():
        minprice=999999999
        URL=''
        try:
            URL=i.sku_set.all()[0].img_set.all()[0].URL
            URL='http://127.0.0.1:8000/static/images/'+ URL
        except:
            pass
        for j in i.sku_set.all():
            minprice=min(minprice,j.price)
        l.append({'id':str(i.SPU_id),'name':i.name,'price':minprice,'stock':'','main_img_url':URL})
    return HttpResponse(json.dumps(l,ensure_ascii=False))


def getSPU(request,uuid):
    l=dict()
    try:
        
        spu=models.SPU.objects.get(SPU_id=uuid)
        URL=spu.sku_set.all()[0].img_set.all()[0].URL
        URL='http://127.0.0.1:8000/static/images/'+ URL
        l['id']=str(spu.SPU_id)
        l['name']=spu.name
        l['properties']=spu.description
        l['summary']=spu.description
        l['store']=spu.belong.name
        l['main_img_url'] = URL
        l['SKU']=[]
        l['specification']=[]
        for i in spu.spec.all():
            tmp={'name':i.name}
            tmp['options']=[]
            for j in i.option_set.all():
                tmp['options'].append(j.name)
            l['specification'].append(tmp)
        minprice=999999999999
        for i in spu.sku_set.all():
            singleSKU={'SKU_id':str(i.SKU_id),'price':i.price,'stock':i.amount}
            optdict={}
            minprice=min(minprice,i.price)
            for j in i.options.all():
                optdict[j.belong.name]=j.name
            singleSKU['option']=optdict
            l['SKU'].append(singleSKU)
        l['price']=minprice
    except:
        l['error']='SPU does not exist'
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def storeList(request):
    l=[]
    for i in models.store.objects.all():
        l.append({'store_id':str(i.store_id),'name':i.name})
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getStore(request,id):
    l=dict()
    try:
        store=models.store.objects.get(store_id=id)
        l['store_id']=str(store.store_id)
        l['name']=store.name
        l['description']=store.description
        for i in store.spu_set.all():
            singleSKU={'SPU_id':str(i.SPU_id),'name':i.name}
    except:
        l['error']='Store does not exist'
    return HttpResponse(json.dumps(l,ensure_ascii=False))

def getAddress(request):
    
    try:
        uuid = request.META.get("HTTP_TOKEN")
        address=json.loads(models.customer.objects.get(uuid=uuid).address)
    except:
        address={'msg':'Address does not exist'}
    return HttpResponse(json.dumps(address,ensure_ascii=False))

def submitAddress(request):
    try:
        concat = request.POST
        postBody = str(request.body, encoding = "utf-8") 
        uuid = request.META.get("HTTP_TOKEN")
        models.customer.objects.filter(uuid=uuid).update(address=postBody)
        return HttpResponse('success submit')   
        print(postBody)
        msg='success'
    except:
        msg='failed'
    return HttpResponse(msg)

def doOrder(request):

    concat = request.POST
    postBody = request.body
    uuid = request.META.get("HTTP_TOKEN")
    # 创建order实例，django自动生成orderid,关联用户，前端发的body里面已经有了productid和个数，存进items里
    print(postBody)

    l=dict()
 
    l['id']='1'
    l['order_id']='13'
    l['pass']=1
    l['countyName']='复兴路'
    l['mobile']='15521332532'
    l['provinceName']='湖北省'
    l['detailInfo']='14号'

    return HttpResponse(json.dumps(l,ensure_ascii=False))