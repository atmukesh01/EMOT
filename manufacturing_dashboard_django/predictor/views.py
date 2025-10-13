from django.shortcuts import render
from .ml_model import get_quality_prediction, find_best_parameters, generate_mock_spectrum, identify_plastic

PLASTIC_DATABASE = {
  "PET": { "name": "Polyethylene Terephthalate (PET)", "viscosity": "18-22 Pa·s", "steps": [{ "name": "Shredding", "icon": "✂️", "description": "Shred plastic into small flakes." }, { "name": "Washing & Separation", "icon": "💧", "description": "Wash flakes; PET sinks in water for separation." }]},
  "HDPE": { "name": "High-Density Polyethylene (HDPE)", "viscosity": "25-30 Pa·s", "steps": [{ "name": "Shredding", "icon": "✂️", "description": "Shred HDPE products into flakes." }, { "name": "Washing", "icon": "💧", "description": "Wash residues; HDPE floats in water." }]},
  "PVC": { "name": "Polyvinyl Chloride (PVC)", "viscosity": "35-40 Pa·s", "steps": [{ "name": "Grinding", "icon": "⚙️", "description": "Grind into a fine powder due to rigidity." }, { "name": "Chemical Recycling", "icon": "🧪", "description": "Use solvents to dissolve PVC and separate additives." }]},
}

def home(request):
    return render(request, 'predictor/base.html')

def predict_quality_view(request):
    context = {}
    if request.method == 'POST':
        params = {
            'temperature_c': float(request.POST.get('temperature', 150)),
            'pressure_psi': float(request.POST.get('pressure', 50)),
            'speed_rpm': float(request.POST.get('speed', 1000)),
            'viscosity_pas': float(request.POST.get('viscosity', 15)),
            'hours_since_maintenance': float(request.POST.get('maintenance', 100)),
            'cycle_time_s': float(request.POST.get('cycle_time', 30)),
        }
        context['prediction'] = get_quality_prediction(params)
    
    return render(request, 'predictor/predict_quality.html', context)

def find_best_parameters_view(request):
    context = {}
    if request.method == 'POST':
        target_quality = float(request.POST.get('target_quality', 98)); 
        context['target_quality'] = target_quality
        locked_params = {k.replace('lock_', ''): v for k, v in request.POST.items() if k.startswith('lock_')}
        context['result'] = find_best_parameters(target_quality, locked_params)
    return render(request, 'predictor/find_best_parameters.html', context)

def requirements_view(request):
    return render(request, 'predictor/requirements.html')

def processes_view(request):
    return render(request, 'predictor/processes.html')

def visualize_view(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('plastic_image'):
        mock_spectrum = generate_mock_spectrum()
        identified_type = identify_plastic(mock_spectrum)
        result_data = PLASTIC_DATABASE.get(identified_type)
        
        if result_data:
            context['result'] = result_data
        else:
            context['error'] = f"Plastic type '{identified_type}' identified, but no processing steps found."

    return render(request, 'predictor/visualize.html', context)