from .models import Bookmark,Customer,CustomerBookmark
from django.db.models import Q
import datetime
from django.contrib.gis.geos import Point
from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import GeometryDistance
class BookmarkFactory(object):

    """ This class defines the handling of object for the bookmark model """

    def __init__(self):
        print("bookmark initiated")


    def create(self,data,customer_id):

        """ this function create the customer bookmark and update the relationship in bookmark table """

        bmk = Bookmark(**data)
        bmk.save()
        if bmk:
            #save relationship
            cst = CustomerBookmark()
            cst.customer_id=customer_id
            cst.bookmark_id=bmk.id
            cst.save()

        return bmk


    def get_order_string(self,column,order):

        """ this function defines like create query string for queryset ordering """
        order=order.lower()
        if "asc" in order:
            order=''
        elif "desc" in order:
            order='-'

        return order+column
    
    def get_bookmark_filter(self,data):

        """ This function handles bookmark filter based  """

        queryset=Bookmark.objects.all()
        cus_id=[]
        cus_check=0
        
        if "radius" in data and "latitude" in data and "longitude" in data:
            cus_check=1
            radius = data["radius"] 
            latitude=data["latitude"]
            longitude = data["longitude"]
            current_location = Point(float(latitude), float(longitude),srid=4326)
            cst_obj=Customer.objects.filter(geo_location__dwithin=(current_location, radius))\
            .annotate(distance=GeometryDistance("geo_location", current_location))\
            .order_by("distance")  #ordery by distance means
            
            for cst in cst_obj:
                print(cst.distance)
                cus_id.append(cst.id)
                
            
            
        if "customer_id" in data:
            cus_check=1
            if cus_id:
                if int(data["customer_id"]) in cus_id:
                    cus_id=[int(data["customer_id"])]
                    
                else:
                    cus_id=[]
            else:
                cus_id=[int(data["customer_id"])]
               
        # print(cus_id)     
        if cus_id:
            bm_id=CustomerBookmark.objects.filter(customer_id__in=cus_id)
            queryset=Bookmark.objects.filter(id__in=bm_id)
        elif cus_check==1:
            return []

        # elif cus_check<1:
        #     queryset=
        
        # if data:
            """ this condition handles filtering based on query parameter from the input """
        Qset=0
        if "source_name" in data and  "url" in data  and "date_range" in data:
            Qset=Q(source_name=data["source_name"]) & Q(url=data["url"]) & Q(updated_at__gte=data["date_range"]) & Q(updated_at__lte=datetime.datetime.now())
            
        elif "source_name" in data and  "url" in data:
            Qset=Q(source_name=data["source_name"]) & Q(url=data["url"])

        elif "url" in data  and "date_range" in data:
            Qset=Q(url=data["url"]) & Q(updated_at__gte=data["date_range"]) & Q(updated_at__lte=datetime.datetime.now())

        elif "source_name" in data and "date_range" in data:
            Qset=Q(source_name=data["source_name"]) & Q(updated_at__gte=data["date_range"]) & Q(updated_at__lte=datetime.datetime.now())
        else:
            if "source_name" in data:
                Qset=Q(source_name=data["source_name"])
            elif "url" in data:
                Qset=Q(url=data["url"])
            elif "date_range" in data:
                Qset = Q(updated_at__gte=data["date_range"]) & Q(updated_at__lte=datetime.datetime.now())


        if "title" in data and Qset:
            Qset = Qset & Q(title__icontains=data["title"])
        elif "title" in data:
            Qset = Q(title__icontains=data["title"])

        if Qset:
            queryset = queryset.filter(Qset)

        if "sort_by" in data or "sort_dir" in data:

            queryset=queryset.order_by(str(self.get_order_string(data["sort_by"],data["sort_dir"])))

        bmk_list=[]
        for q in queryset:
            bmk_dict = {}
            bmk_dict["id"]=q.id
            bmk_dict["source_name"]=q.source_name
            bmk_dict["title"]=q.title
            bmk_dict["url"]=q.url 
            bmk_dict["created_at"]=q.created_at
            bmk_dict["updated_at"]=q.updated_at
            bmk_list.append(bmk_dict)

       
        
        return bmk_list

        






theBookmarkFactory=BookmarkFactory()

class CustomerFactory(object):


    def __init__(self):
        print("customer_initiated")

    def create(self,data):
        """ This function creates new customer """
        resp={}
        if self.check_username_exist(data["username"]):

            
            resp["status"]='Failure'
            resp["message"]='Username already exist'
            
        else:
            customer_details=Customer()
            
            if customer_details:
                if "first_name" in data:
                    customer_details.first_name=data['first_name']
                else:
                    customer_details.first_name=""
                if "last_name" in data:
                    customer_details.last_name=data['last_name']
                if "email" in data:
                    customer_details.email=data['email']
                else:
                    customer_details.email=""
                if "username" in data:
                    customer_details.username=data['username']
                else:
                    customer_details.username=""
                if "password" in data:
                    hash_password=make_password(data['password'])
                    customer_details.password=hash_password
                else:
                    customer_details.password=""
                
                if "mobile_no" in data:
                    customer_details.mobile_no=data['mobile_no']
                else:
                    customer_details.mobile_no=""

                if "latitude" in data and "longitude" in data:
                    customer_details.geo_location = Point(float(data["latitude"]),float(data["longitude"]))
                else:
                    customer_details.geo_location=Point(0,0)
                
                
                customer_details.save()
                resp["status"]='Success'
                resp["message"]='Customer created successfully'

        return resp


    def  check_username_exist(self,username):
        
        customer_details= Customer.objects.filter(username__iexact=username).first()
        if customer_details:
            return True
        print("pass")
        return False




theCustomerFactory = CustomerFactory()





