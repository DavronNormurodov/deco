from django.urls import path, include

urlpatterns = [
    path('', include(('users.urls', 'users'), 'users'), ),
    path('products/', include(('product.urls', 'product'), 'product'), ),
    path('', include(('employee.urls', 'employee'), 'employee'), ),
]

# test