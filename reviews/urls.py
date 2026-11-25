from django.urls import path

from reviews.views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView

app_name = 'reviews'

urlpatterns = [
    path('add/<int:recipe_pk>/', ReviewCreateView.as_view(), name='review_add'),
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]