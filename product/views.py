from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .filters import ProductsFilter

from .serializers import ProductImagesSerializer, ProductSerializer

from .models import Product, ProductImages

# Create your views here.
@api_view(['GET'])
def get_products(request):
    
    filterSet = ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count = filterSet.qs.count()
    #pagination 
    resPerPage = 2
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterSet.qs,request)
    # products = Product.objects.all()

    serializer = ProductSerializer(queryset, many=True)

    return Response({ 
        'count': count,
        'resPerPage': resPerPage,
        'products': serializer.data
        })


@api_view(['GET'])
def get_product(request,pk):
    
    product = get_object_or_404(Product,id=pk)

    serializer = ProductSerializer(product, many=False)

    return Response({'product': serializer.data})


@api_view(['POST'])
def upload_product_images(request):
    
    data=request.data
    files = request.FILES.getlist('images')

    images= []
    for f in files:
        image = ProductImages.objects.create(product=Product(data['product']), image=f)
        images.append(image)

    serializer = ProductImagesSerializer(images, many=True)

    return Response(serializer.data)