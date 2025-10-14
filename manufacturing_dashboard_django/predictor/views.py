from django.shortcuts import render
from django.http import JsonResponse
from .ml_model import get_quality_prediction, find_best_parameters, generate_mock_spectrum, identify_plastic

# This dictionary acts as our local database for the visualize feature
PLASTIC_DATABASE = {
  "PET": { "name": "Polyethylene Terephthalate (PET)", "viscosity": "18-22 Pa·s", "steps": [{ "name": "Shredding", "icon": "✂️", "description": "Shred plastic into small flakes." }, { "name": "Washing & Separation", "icon": "💧", "description": "Wash flakes; PET sinks in water for separation." }]},
  "HDPE": { "name": "High-Density Polyethylene (HDPE)", "viscosity": "25-30 Pa·s", "steps": [{ "name": "Shredding", "icon": "✂️", "description": "Shred HDPE products into flakes." }, { "name": "Washing", "icon": "💧", "description": "Wash residues; HDPE floats in water." }]},
  "PVC": { "name": "Polyvinyl Chloride (PVC)", "viscosity": "35-40 Pa·s", "steps": [{ "name": "Grinding", "icon": "⚙️", "description": "Grind into a fine powder due to rigidity." }, { "name": "Chemical Recycling", "icon": "🧪", "description": "Use solvents to dissolve PVC and separate additives." }]},
  "LDPE": { "name": "Low-Density Polyethylene (LDPE)", "viscosity": "20-25 Pa·s", "steps": [] },
  "PP": { "name": "Polypropylene (PP)", "viscosity": "15-20 Pa·s", "steps": [] },
  "PS": { "name": "Polystyrene (PS)", "viscosity": "10-15 Pa·s", "steps": [] },
  "PC": { "name": "Polycarbonate (PC)", "viscosity": "30-35 Pa·s", "steps": [] },
  "ABS": { "name": "Acrylonitrile Butadiene Styrene (ABS)", "viscosity": "22-28 Pa·s", "steps": [] },
}

def home(request):
    """Renders the base template, which serves as the homepage."""
    return render(request, 'predictor/base.html')

def predict_quality_view(request):
    """
    Handles the initial page load and the AJAX prediction.
    This version prepares all data for the template to avoid logic in the HTML.
    """
    # Base configuration for the parameters is now defined here in Python
    params_config = [
        {'name': 'temperature', 'label': 'Temperature (°C)', 'default': ''},
        {'name': 'pressure', 'label': 'Pressure (psi)', 'default': ''},
        {'name': 'speed', 'label': 'Speed (rpm)', 'default': ''},
        {'name': 'viscosity', 'label': 'Viscosity (Pa·s)', 'default': ''},
        {'name': 'maintenance', 'label': 'Hours Since Maintenance', 'default': ''},
        {'name': 'cycle_time', 'label': 'Cycle Time (s)', 'default': ''},
    ]

    # This handles the AJAX request when the "Predict Quality" button is clicked
    if request.method == 'POST':
        try:
            params = {
                'temperature_c': float(request.POST.get('temperature') or '0'),
                'pressure_psi': float(request.POST.get('pressure') or '0'),
                'speed_rpm': float(request.POST.get('speed') or '0'),
                'viscosity_pas': float(request.POST.get('viscosity') or '0'),
                'hours_since_maintenance': float(request.POST.get('maintenance') or '0'),
                'cycle_time_s': float(request.POST.get('cycle_time') or '0'),
            }
            prediction = get_quality_prediction(params)
            if prediction is not None:
                return JsonResponse({'predicted_quality': prediction})
            else:
                return JsonResponse({'error': 'Model is not loaded on the server.'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'A server error occurred: {str(e)}'}, status=500)

    # This handles the initial page load (a GET request)
    context = {
        'params_config': params_config
    }
    return render(request, 'predictor/predict_quality.html', context)


def find_best_parameters_view(request):
    """
    Handles the form for finding the best parameters, including locked ones.
    """
    params_config = [
        {'name': 'temperature', 'key': 'temperature_c', 'label': 'Temperature (°C)', 'default': ''},
        {'name': 'pressure', 'key': 'pressure_psi', 'label': 'Pressure (psi)', 'default': ''},
        {'name': 'speed', 'key': 'speed_rpm', 'label': 'Speed (rpm)', 'default': ''},
        {'name': 'viscosity', 'key': 'viscosity_pas', 'label': 'Viscosity (Pa·s)', 'default': ''},
        {'name': 'maintenance', 'key': 'hours_since_maintenance', 'label': 'Hours Since Maintenance', 'default': ''},
        {'name': 'cycle_time', 'key': 'cycle_time_s', 'label': 'Cycle Time (s)', 'default': ''},
    ]
    
    context = {}

    if request.method == 'POST':
        posted_values = request.POST
        target_quality = float(posted_values.get('target_quality') or '0')
        
        locked_params = {}
        for key in posted_values:
            if key.startswith('lock_'):
                param_name = key.split('_', 1)[1]
                locked_params[param_name] = posted_values.get(param_name)
        
        # Format the results for clean display in the template
        result_data = find_best_parameters(target_quality, locked_params)
        formatted_results = []
        if result_data:
            for config in params_config:
                param_name = config['name']
                formatted_results.append({
                    'label': config['label'],
                    'value': result_data['best_parameters'].get(param_name),
                    'is_locked': param_name in locked_params
                })
            context['achieved_quality'] = result_data['achieved_quality']

        for param in params_config:
            param['value'] = posted_values.get(param['name'], param['default'])
            param['is_locked'] = param['name'] in locked_params
        
        context.update({
            'target_quality': target_quality,
            'formatted_results': formatted_results,
            'locked_keys': locked_params.keys()
        })

    else: # This handles the initial GET request
        for param in params_config:
            param['value'] = param['default']
            param['is_locked'] = False

    context['params_config'] = params_config
    return render(request, 'predictor/find_best_parameters.html', context)


def visualize_view(request):
    """Handles the image upload and ML-based plastic identification."""
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