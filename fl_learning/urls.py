from django.urls import path


from fl_learning.views import FLModelTrainAPIView, FLModelPredictAPIView

urlpatterns = [
    path('fl_train/', FLModelTrainAPIView.as_view(), name='fl_train'),
    path('fl_predict/', FLModelPredictAPIView.as_view(), name='fl_predict')
]