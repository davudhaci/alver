from django.shortcuts import render,HttpResponse,get_object_or_404,redirect,reverse
from . import models
from user import forms
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse


# Create your views here.

def kole(ls):
    allinone = ls
    one =[]
    for i in allinone:
        for j in i:
            one+=[j]
        


    def SortKey(word):  # burdaki word'a sorted funksiyasi "one" listinin icerisindeki elmentleri gezir ve SortKeye gonderir davami--
        return word.created_date # burdada biz created_date(yeni meselcun one[0].create_date kimi) e gore sortlasdiracaqimizi bildiririik.

    one = sorted(one,key=SortKey)[::-1]  #Sort modulunun key parametri heyat qurtariri ! :D
            

    
    palasa = len(one)//4 + 1
    x = 0
    
    son=[]
    for i in range(palasa):
        son+=[one[x:x+4]]
        x+=4

    return son

@login_required(login_url="/user/login/")
def complete(request):
    productId = json.loads(request.body)["prodcutId"]
    types = json.loads(request.body)["type"]

    if types == "elan":
        MyModel = models.Elan.objects.get(id=productId)
        print(MyModel,"MYMODELLL")

        MyModel.packet = "pre"
        MyModel.save()
    elif types == "sticker":
        
        MyModel = models.Article.objects.get(id=productId)
        print(MyModel,"MYMODELLL")
        MyModel.packet = "pre"
        MyModel.save()
    

    
    
    return JsonResponse("Əməliyatinız Uğurla Başa çatdı",safe=False)




def index(request):
    keyword = request.GET.get("s")

    if  keyword:

        
        articles = models.Article.objects.filter(title__contains=keyword,packet='nrml')[::-1]
        elanlar = models.Elan.objects.filter(title__contains=keyword,packet='nrml')[::-1]

        Premiumarticles = models.Article.objects.filter(title__contains=keyword,packet='pre')[::-1]
        Premiumelanlar = models.Elan.objects.filter(title__contains=keyword,packet='pre')[::-1]        
 
        son = kole([articles,elanlar])
        pre = kole([Premiumarticles,Premiumelanlar])

        print(pre)


        return render(request,"searchIndex.html",{
        "son":son,
        "sonyox":son[0],
        "pre":pre,
        "preyox":pre[0],
        })



    """
    userPremium = models.PacketsArticle.objects.filter(packet='pre')[::-1][:4] # [:10] Butun Articllar Sonuncu 10 dene
  
    elanPremium = models.PacketElan.objects.filter(packet='pre')[::-1][:4] # [:10] Butun Articllar Sonuncu 10 dene

    userNormal = models.PacketsArticle.objects.filter(packet='nrml')[::-1][:12] # [:10] Butun Articllar Sonuncu 10 dene

    userNormal = models.PacketsArticle.objects.filter(packet='nrml')[::-1][:12] # [:10] Butun Articllar Sonuncu 10 dene
    """
    
    articles = models.Article.objects.filter(packet='nrml')[::-1][:10] # [:10] Butun Articllar Sonuncu 10 dene

    elanlar = models.Elan.objects.filter(packet='nrml')[::-1][:14] #bunun evezine modelde Meta classi acip altina : ordering = ['-created_date'] yazsaq yenede eyni sey olacaq
    
    Premiumarticles = models.Article.objects.filter(packet='pre')[::-1][:15] # [:10] Butun Articllar Sonuncu 10 dene

    Premiumelanlar = models.Elan.objects.filter(packet='pre')[::-1][:15] #bunun evezine modelde Meta classi acip altina : ordering = ['-created_date'] yazsaq yenede eyni sey olacaq

    son = kole([articles,elanlar])
    pre = kole([Premiumarticles,Premiumelanlar])

    
    print(pre)

    return render(request,"index.html",{
    "son":son,
    "sonyox":son[0],
    "pre":pre,
    "preyox":pre[0],
    })




def about(request):
    contex={
        "salam":"salam",
        "sifre":1234,
    }
    return render(request,"about.html",contex)

def dynamic(request,id):
    articlenow = get_object_or_404(models.Article,id=id)

    articles = models.Article.objects.filter(status=articlenow.status,packet='nrml')[::-1][:4] # [:10] Butun Articllar Sonuncu 10 dene

    elanlar = models.Elan.objects.filter(status=articlenow.status,packet='nrml')[::-1][:4] #bunun evezine modelde Meta classi acip altina : ordering = ['-created_date'] yazsaq yenede eyni sey olacaq
    
    Premiumarticles = models.Article.objects.filter(status=articlenow.status,packet='pre')[::-1][:4] # [:10] Butun Articllar Sonuncu 10 dene

    Premiumelanlar = models.Elan.objects.filter(status=articlenow.status,packet='pre')[::-1][:4] #bunun evezine modelde Meta classi acip altina : ordering = ['-created_date'] yazsaq yenede eyni sey olacaq

    son = kole([articles,elanlar])
    pre = kole([Premiumarticles,Premiumelanlar])
    print(son,pre,"SOOONNN PRREEE")

    try:
        articleImages=models.ArticleImage.objects.filter(product = articlenow)
        print(articleImages,'\n',articleImages[0].product_image.url,"BUUUUU ARTICCCLEEE IMAGEESSSDIR")
        content = {
            'article':articlenow,
            'articleImages':articleImages,
            'son':son,
            'pre':pre,
        }

        return render(request,"product.html",content)
    except:


        content = {
            "article":articlenow,
            'son':son,
            'pre':pre,
        }

        return render(request,"product.html",content)


def create(request):
    keyword = request.GET.get("s")

    if  keyword:

        
        articles = models.Article.objects.filter(title__contains=keyword)
        palasa = len(articles)//4 + 1
        print(palasa)
        x = 0
        
        son=[]
        for i in range(palasa):
            son+=[articles[x:x+4]]
            x+=4

                    #articles = get_object_or_404(models.Article,title__contains=keyword) Bele de munkundur.



        return render(request,"searchIndex.html",{
        "son":son[::-1]
        })



    articles = models.Article.objects.all() # Butun Articllar Sonuncu 10 dene
    articles = articles[::-1]
    palasa = len(articles)//4 + 1
    print(palasa)
    x = 0
    
    son=[]
    for i in range(palasa):
        son+=[articles[x:x+4]]
        x+=4

    


    return render(request,"yoxla.html",{
    "son":son
    })

@login_required(login_url="/user/login")
def deleteArticle(request,id):
    
    article = get_object_or_404(models.Article,id=id)
    if article.author == request.user:
        article.delete()

        messages.success(request, 'Elan Silindi')


        return redirect("user:dashboard")
    else:
        messages.warning(request, 'Bu Meqaleni Silenmersen !!')


        return redirect("user:dashboard")

@login_required(login_url="/user/login")
def updateArticle(request,id):
    
    if request.method == "POST":
        
        form = forms.StickerForm(request.POST,request.FILES)

        if form.is_valid():
            Sticker = form.save(commit=False)
            Sticker.author = request.user

            imgHead = request.FILES.get("image")
            ctgry = request.POST.get("status")

            fs = FileSystemStorage()
            file_path=fs.save(imgHead.name,imgHead)

            Sticker.image = file_path 

            Sticker.save()

            ac  = models.ArticleCategory()

            ac.product = Sticker
            ac.category= ctgry

            ac.save()


            try:
                files = request.FILES.getlist("file[]")
                for img in files:
                    print (img)
                    newfs=FileSystemStorage()
                    newPath= newfs.save(img.name,img)



                    newImage = models.ArticleImage(product=Sticker,product_image=newPath)
                    newImage.save()
                    
                return redirect(reverse('dynamic',kwargs={"id":Sticker.id}))



            except:



                return redirect(reverse('dynamic',kwargs={"id":Sticker.id}))


    article = get_object_or_404(models.Article,id=id)
    form = forms.StickerForm(instance=article)
        
    return render(request,"updateArticle.html",{"form":form})



def Category(request,ctgry,nov):
    print(ctgry,nov)

    articles = models.Article.objects.filter(status=nov,packet='nrml')[::-1] # [:10] Butun Articllar Sonuncu 10 dene

    elanlar = models.Elan.objects.filter(status=nov,packet='nrml')[::-1] #bunun evezine modelde Meta classi acip altina : ordering = ['-created_date'] yazsaq yenede eyni sey olacaq
    
    Premiumarticles = models.Article.objects.filter(status=nov,packet='pre')[::-1] # [:10] Butun Articllar Sonuncu 10 dene

    Premiumelanlar = models.Elan.objects.filter(status=nov,packet='pre')[::-1] #bunun evezine modelde Meta classi acip altina : ordering = ['-created_date'] yazsaq yenede eyni sey olacaq

    son = kole([articles,elanlar])
    pre = kole([Premiumarticles,Premiumelanlar])



    return render(request,"katiqoriya.html",{
    "son":son,
    "pre":pre,
    "nov":ctgry,
    "sonyox":son[0],
    "preyox":pre[0],
    })

@login_required(login_url="/user/login/")
def buySticker(request,id):

    return render(request,"buy.html",{"id":id,"type":"sticker"})