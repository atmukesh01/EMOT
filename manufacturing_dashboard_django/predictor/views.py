# File: predictor/views.py

from django.shortcuts import render
from .ml_model import predict_quality # Import our prediction function

def dashboard_view(request):
    predicted_quality = None
    
    if request.method == 'POST':
        # Get data from the form
        temp = float(request.POST.get('temperature'))
        pressure = float(request.POST.get('pressure'))
        speed = float(request.POST.get('speed'))
        
        # Get prediction from our model
        predicted_quality = predict_quality(temp, pressure, speed)
    
    # Prepare the context to pass to the template
    context = {
        'predicted_quality': predicted_quality
    }
    
    return render(request, 'predictor/dashboard.html', context)