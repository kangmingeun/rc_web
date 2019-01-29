from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Category, Location, Store, Photo
from account.models import Profile
import json, datetime

# Create your views here.

# 가맹점 신청 / 정보수정
@login_required
def edit_store(request):
    try:
        store = (Store.objects.filter(Q(representative_id=request.user.pk) & ~Q(status=3)))[0]
        photo = (Photo.objects.filter(Q(store_id=store.pk)))[0]
    except:
        store = Store()
        photo = Photo()

    if request.method == 'POST':
        store.name = request.POST.get('name', None)
        store.representative = request.user
        store.corporate_number = request.POST.get('corporate_number', None)
        store.location = get_object_or_404(Location, id=request.POST.get('location', 1))
        store.category = get_object_or_404(Category, id=request.POST.get('category', 1))
        store.phone_number = request.POST.get('phone_number', None)
        store.url = request.POST.get('url', None)
        store.address = request.POST.get('address', None)
        store.opening_hour = request.POST.get('opening_hour', None) 
        store.opening_minute = request.POST.get('opening_minute', None)
        store.closing_hour = request.POST.get('closing_hour', None)
        store.closing_minute = request.POST.get('closing_minute', None)
        store.description = request.POST.get('description', None)
        store.status = 1
        store.save()
        
        photo.store_id = store.pk
        photo.image = request.FILES['image']
        photo.save()
        
        profile = get_object_or_404(Profile, user_id=request.user.pk)
        profile.type = 1
        profile.save()

        return redirect('store:info')
    else:
        category = Category.objects.all().order_by('id')
        category_list = []
        for domain in category:
            temp = {
                'id' : domain.id,
                'domain' : domain.domain   
            }
            category_list.append(temp)
        categorys = {
            'category_list' : category_list
        }
        json_category = json.dumps(categorys)

        location = Location.objects.all().order_by('id')
        location_list = []
        for loc in location:
            temp = {
                'id' : loc.id,
                'loc' : loc.loc   
            }
            location_list.append(temp)
        locations = {
            'location_list' : location_list
        }
        json_location = json.dumps(locations)

        data = {
            'store' : store,
            'photo' : photo,
            'categorys' : json_category,
            'locations' : json_location
        }
        return render(request, 'store/store_edit.html', data)

# 카테고리 리스트 가져오기
def get_categorys():
    categorys = Category.objects.all()
    domain_list = []
    for domain in categorys:
        domain_list.append(domain)
    return domain_list

# 로케이션 리스트 가져오기
def get_locations():
    locations = Location.objects.all()
    location_list = []
    for loc in locations:
        location_list.append(loc)
    return location_list

# 내 가맹점 정보 조회
@login_required
def get_myStore(request):
    user = request.user
    store = Store.objects.filter(Q(representative_id = user.pk) & ~Q(status=3))
    photo = Photo.objects.filter(Q(store_id=store[0].pk))
    domain = get_categorys()
    loc = get_locations()
    status = ['승인대기중', '승인됨']

    data = {
        'store' : store[0],
        'photo' : photo[0],
        'status': status[store[0].status-1],
        'domain': domain[store[0].category_id-1],
        'loc'   : loc[store[0].location_id-1],
        'rdate' : (store[0].registered_date).strftime('%Y-%m-%d %H:%M:%S'),
        'mdate' : (store[0].modified_date).strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, 'store/store_info.html', data)

# 가맹점 삭제
@login_required
def del_store(request, s_id):
    store = (Store.objects.filter(Q(pk=s_id) & ~Q(status=3)))[0]
    if store.representative_id == request.user.pk:
        store.status = 3
        store.save()
        profile = get_object_or_404(Profile, user=request.user)
        profile.type = 2
        profile.save()
        # 삭제 성공
    return redirect('index')

# QR Code 페이지 생성
@login_required
def get_qrcode(request):
    store = (Store.objects.filter(Q(representative=request.user) & Q(status=2)))[0]
    return render(request, 'store/store_QRcode.html', dict(store=store))

# 가맹점 리스트
def get_storeList(request):
    pass