from django.shortcuts import render
from django.http import JsonResponse
from .ml_model import get_quality_prediction, find_best_parameters, run_full_image_pipeline
import base64

PLASTIC_DATABASE = {
    "PET": {
        "name": "Polyethylene Terephthalate (PET)", "viscosity": "18-22 Pa·s",
        "product_processes": {
            "Drink Bottles": [
                {"step": 1, "name": "Crystallization & Drying", "temp": "160-180°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "4-6 hours", "maintenance": "Check heaters every 250 hours."},
                {"step": 2, "name": "Injection Molding (Preform)", "temp": "250-275°C", "pressure": "10,000-15,000 psi", "speed": "50-100 mm/s", "cycle_time": "15-30 sec", "maintenance": "Clean mold surfaces daily."},
                {"step": 3, "name": "Stretch Blow Molding", "temp": "90-110°C (Reheat)", "pressure": "500-600 psi (Blow)", "speed": "N/A", "cycle_time": "5-10 sec", "maintenance": "Check blow nozzles daily."}
            ],
            "Polyester Fibers (Clothing)": [
                {"step": 1, "name": "Critical Drying", "temp": "170°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "6 hours", "maintenance": "Verify dryer dew point weekly."},
                {"step": 2, "name": "Melt Extrusion (Spinning)", "temp": "280-300°C", "pressure": "2500-3000 psi", "speed": "Variable (Pump)", "cycle_time": "Continuous", "maintenance": "Inspect spinneret for clogs daily."},
                {"step": 3, "name": "Drawing & Texturizing", "temp": "80-120°C (Heated Rollers)", "pressure": "N/A", "speed": "1000-4000 m/min", "cycle_time": "Continuous", "maintenance": "Check godet roller condition weekly."}
            ]
        }
    },
    "HDPE": {
        "name": "High-Density Polyethylene (HDPE)", "viscosity": "25-30 Pa·s",
        "product_processes": {
            "Milk Jugs (Blow Molding)": [
                {"step": 1, "name": "Drying", "temp": "80-90°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "1-2 hours", "maintenance": "Calibrate temperature sensors monthly."},
                {"step": 2, "name": "Extrusion (Parison)", "temp": "180-210°C", "pressure": "1000-1500 psi", "speed": "60-100 rpm", "cycle_time": "Continuous", "maintenance": "Inspect die head every 500 hours."},
                {"step": 3, "name": "Blow Molding & Cooling", "temp": "20-40°C (Mold)", "pressure": "80-120 psi (Blow)", "speed": "N/A", "cycle_time": "10-20 sec", "maintenance": "Check mold clamping force weekly."}
            ],
            "Pipes (Extrusion)": [
                {"step": 1, "name": "Extrusion", "temp": "190-240°C", "pressure": "1500-2500 psi", "speed": "50-80 rpm", "cycle_time": "Continuous", "maintenance": "Verify screw wear every 2000 hours."},
                {"step": 2, "name": "Vacuum Sizing & Cooling", "temp": "10-20°C (Water Bath)", "pressure": "Low Vacuum", "speed": "N/A", "cycle_time": "Continuous", "maintenance": "Clean sizing tank and spray nozzles daily."},
                {"step": 3, "name": "Haul-Off & Cutting", "temp": "Ambient", "pressure": "Variable (Grip)", "speed": "Matched to extrusion", "cycle_time": "N/A", "maintenance": "Check cutter blade sharpness weekly."}
            ]
        }
    },
    "PVC": {
        "name": "Polyvinyl Chloride (PVC)", "viscosity": "35-40 Pa·s",
        "product_processes": {
            "Pipes & Fittings": [
                {"step": 1, "name": "Compound Blending", "temp": "80-120°C", "pressure": "N/A", "speed": "1500-3000 rpm", "cycle_time": "10-15 min/batch", "maintenance": "Clean mixer blades weekly."},
                {"step": 2, "name": "Extrusion", "temp": "160-190°C", "pressure": "2000-4000 psi", "speed": "20-40 rpm (Low Shear)", "cycle_time": "Continuous", "maintenance": "Monitor for signs of degradation."},
                {"step": 3, "name": "Sizing & Cooling", "temp": "10-20°C (Water Bath)", "pressure": "Vacuum Sizing", "speed": "N/A", "cycle_time": "Continuous", "maintenance": "Clean sizing sleeve daily."}
            ],
            "Window Frames (Profiles)": [
                {"step": 1, "name": "High-Intensity Mixing", "temp": "110-130°C", "pressure": "N/A", "speed": "2000-3000 rpm", "cycle_time": "8-12 min/batch", "maintenance": "Check mixer seals monthly."},
                {"step": 2, "name": "Twin-Screw Extrusion", "temp": "175-195°C", "pressure": "3000-5000 psi", "speed": "15-35 rpm", "cycle_time": "Continuous", "maintenance": "Calibrate dosing feeders weekly."},
                {"step": 3, "name": "Calibration & Cooling", "temp": "15-25°C (Water)", "pressure": "Vacuum Calibration", "speed": "N/A", "cycle_time": "Continuous", "maintenance": "Inspect calibrator surfaces for wear."}
            ]
        }
    },
    "LDPE": {
        "name": "Low-Density Polyethylene (LDPE)", "viscosity": "20-25 Pa·s",
        "product_processes": {
            "Plastic Bags (Blown Film)": [
                {"step": 1, "name": "Melt Extrusion", "temp": "160-200°C", "pressure": "1500-2500 psi", "speed": "80-120 rpm", "cycle_time": "Continuous", "maintenance": "Clean die lips every 24 hours."},
                {"step": 2, "name": "Film Blowing & Cooling", "temp": "Ambient Air", "pressure": "Low Air Pressure", "speed": "N/A (Air Ring)", "cycle_time": "Continuous", "maintenance": "Check air ring for blockages daily."},
                {"step": 3, "name": "Winding & Cutting", "temp": "Ambient", "pressure": "N/A", "speed": "Variable (Winder)", "cycle_time": "Continuous", "maintenance": "Calibrate bag sealer and cutter weekly."}
            ],
            "Squeeze Bottles": [
                {"step": 1, "name": "Injection Molding", "temp": "180-240°C (Melt)", "pressure": "8,000-14,000 psi", "speed": "50-100 mm/s", "cycle_time": "10-30 sec", "maintenance": "Check for nozzle drool daily."},
                {"step": 2, "name": "Cooling", "temp": "20-60°C (Mold)", "pressure": "N/A", "speed": "N/A", "cycle_time": "Part of cycle", "maintenance": "Inspect cooling channels monthly."}
            ]
        }
    },
    "PP": {
        "name": "Polypropylene (PP)", "viscosity": "15-20 Pa·s",
        "product_processes": {
            "Automotive Parts (Bumpers)": [
                {"step": 1, "name": "Drying", "temp": "80°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "2-3 hours", "maintenance": "Check desiccant beds monthly."},
                {"step": 2, "name": "Injection Molding", "temp": "220-280°C (Melt)", "pressure": "12,000-20,000 psi", "speed": "40-80 mm/s", "cycle_time": "30-90 sec", "maintenance": "Lubricate large mold components weekly."},
                {"step": 3, "name": "Robotic Handling & Cooling", "temp": "Ambient", "pressure": "N/A", "speed": "N/A", "cycle_time": "Part of cycle", "maintenance": "Calibrate robot arm quarterly."}
            ],
            "Food Containers (Thin-Wall Molding)": [
                {"step": 1, "name": "High-Flow Injection Molding", "temp": "230-260°C (Melt)", "pressure": "15,000-25,000 psi", "speed": "100-300 mm/s (High Speed)", "cycle_time": "3-8 sec", "maintenance": "Inspect mold vents daily for clogging."},
                {"step": 2, "name": "In-Mold Labeling (IML)", "temp": "40-60°C (Mold)", "pressure": "N/A", "speed": "Robotic", "cycle_time": "Part of cycle", "maintenance": "Check static charge on labels."},
                {"step": 3, "name": "Stacking & Packing", "temp": "Ambient", "pressure": "N/A", "speed": "Automated", "cycle_time": "Continuous", "maintenance": "Check stacking mechanism daily."}
            ]
        }
    },
    "PS": {
        "name": "Polystyrene (PS)", "viscosity": "10-15 Pa·s",
        "product_processes": {
            "Disposable Cups (Thermoforming)": [
                {"step": 1, "name": "Sheet Extrusion", "temp": "190-230°C", "pressure": "1000-2000 psi", "speed": "30-60 rpm", "cycle_time": "Continuous", "maintenance": "Check roller gaps for uniform thickness."},
                {"step": 2, "name": "Heating Sheet", "temp": "130-160°C (Oven)", "pressure": "N/A", "speed": "N/A", "cycle_time": "5-10 sec", "maintenance": "Verify heater elements are all working."},
                {"step": 3, "name": "Thermoforming & Trimming", "temp": "40-70°C (Mold)", "pressure": "Vacuum / 30-60 psi Air", "speed": "N/A", "cycle_time": "2-5 sec", "maintenance": "Sharpen trim tooling every 100k cycles."}
            ],
            "Insulation Foam (EPS Molding)": [
                {"step": 1, "name": "Pre-expansion", "temp": "100°C (Steam)", "pressure": "Atmospheric", "speed": "Agitator", "cycle_time": "2-5 min", "maintenance": "Check steam nozzles for blockage."},
                {"step": 2, "name": "Block Molding", "temp": "110-120°C (Steam)", "pressure": "15-25 psi", "speed": "N/A", "cycle_time": "10-20 min", "maintenance": "Inspect mold seals for leaks."},
                {"step": 3, "name": "Hot-Wire Cutting", "temp": "200-300°C (Wire)", "pressure": "N/A", "speed": "Variable", "cycle_time": "N/A", "maintenance": "Replace cutting wires regularly."}
            ]
        }
    },
    "PC": {
        "name": "Polycarbonate (PC)", "viscosity": "30-35 Pa·s",
        "product_processes": {
            "Eyeglass Lenses (Precision Molding)": [
                {"step": 1, "name": "CRITICAL Drying", "temp": "120°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "4-5 hours", "maintenance": "Verify dew point is below -30°C daily."},
                {"step": 2, "name": "Injection Molding", "temp": "290-320°C", "pressure": "18,000-28,000 psi", "speed": "20-50 mm/s (Slow)", "cycle_time": "45-90 sec", "maintenance": "High-polish mold surfaces; handle with gloves."},
                {"step": 3, "name": "Annealing (Stress Relief)", "temp": "125°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "2-4 hours", "maintenance": "Calibrate oven temperature quarterly."}
            ],
            "Electronic Housings": [
                {"step": 1, "name": "Drying", "temp": "120°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "4 hours", "maintenance": "Check dryer filters weekly."},
                {"step": 2, "name": "Injection Molding", "temp": "280-310°C", "pressure": "15,000-25,000 psi", "speed": "40-80 mm/s", "cycle_time": "30-60 sec", "maintenance": "Clean mold vents every 500 cycles."},
                {"step": 3, "name": "Part Cooling & Handling", "temp": "80-120°C (Mold)", "pressure": "N/A", "speed": "Robotic", "cycle_time": "Part of cycle", "maintenance": "Inspect robotic grippers for wear."}
            ]
        }
    },
    "ABS": {
        "name": "Acrylonitrile Butadiene Styrene (ABS)", "viscosity": "22-28 Pa·s",
        "product_processes": {
            "LEGO Bricks (Precision Molding)": [
                {"step": 1, "name": "Pre-drying", "temp": "80°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "2-4 hours", "maintenance": "Check dryer performance weekly."},
                {"step": 2, "name": "Injection Molding", "temp": "230-250°C", "pressure": "15,000-22,000 psi", "speed": "30-60 mm/s", "cycle_time": "10-25 sec", "maintenance": "CRITICAL: Monitor mold dimensions daily."},
                {"step": 3, "name": "Quality Control", "temp": "Ambient", "pressure": "N/A", "speed": "Automated Vision", "cycle_time": "Continuous", "maintenance": "Calibrate vision system cameras weekly."}
            ],
            "Automotive Interior Trim": [
                {"step": 1, "name": "Drying", "temp": "80-90°C", "pressure": "Atmospheric", "speed": "N/A", "cycle_time": "3-4 hours", "maintenance": "Check air filters."},
                {"step": 2, "name": "Injection Molding", "temp": "220-260°C", "pressure": "12,000-20,000 psi", "speed": "Variable", "cycle_time": "40-120 sec", "maintenance": "Clean mold texture/grain surfaces."},
                {"step": 3, "name": "Post-Molding Assembly", "temp": "Ambient", "pressure": "N/A", "speed": "Manual/Robotic", "cycle_time": "Variable", "maintenance": "Check assembly jigs for alignment."}
            ]
        }
    },
}

def home(request):
    return render(request, 'predictor/base.html')

def predict_quality_view(request):
    params_config = [
        {'name': 'temperature', 'label': 'Temperature (°C)', 'default': ''},
        {'name': 'pressure', 'label': 'Pressure (psi)', 'default': ''},
        {'name': 'speed', 'label': 'Speed (rpm)', 'default': ''},
        {'name': 'viscosity', 'label': 'Viscosity (Pa·s)', 'default': ''},
        {'name': 'maintenance', 'label': 'Hours Since Maintenance', 'default': ''},
        {'name': 'cycle_time', 'label': 'Cycle Time (s)', 'default': ''},
    ]
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
    context = {'params_config': params_config}
    return render(request, 'predictor/predict_quality.html', context)


def find_best_parameters_view(request):
    params_config = [
        {'name': 'temperature', 'key': 'temperature_c', 'label': 'Temperature (°C)'},
        {'name': 'pressure', 'key': 'pressure_psi', 'label': 'Pressure (psi)'},
        {'name': 'speed', 'key': 'speed_rpm', 'label': 'Speed (rpm)'},
        {'name': 'viscosity', 'key': 'viscosity_pas', 'label': 'Viscosity (Pa·s)'},
        {'name': 'maintenance', 'key': 'hours_since_maintenance', 'label': 'Hours Since Maintenance'},
        {'name': 'cycle_time', 'key': 'cycle_time_s', 'label': 'Cycle Time (s)'},
    ]
    context = {}
    if request.method == 'POST':
        try:
            posted_values = request.POST
            target_quality = float(posted_values.get('target_quality') or '0')
            locked_params = {}
            for key in posted_values:
                if key.startswith('lock_'):
                    param_name = key.split('_', 1)[1]
                    locked_params[param_name] = posted_values.get(param_name)
            result_data = find_best_parameters(target_quality, locked_params)
            if result_data:
                formatted_results = []
                for config in params_config:
                    param_name = config['name']
                    formatted_results.append({
                        'label': config['label'],
                        'value': result_data['best_parameters'].get(param_name),
                        'is_locked': param_name in locked_params
                    })
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'target_quality': target_quality,
                        'achieved_quality': result_data.get('achieved_quality'),
                        'formatted_results': formatted_results
                    })
            else:
                 return JsonResponse({'success': False, 'error': 'Could not find a valid result.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    for param in params_config:
        param['value'] = ''
        param['is_locked'] = False
    context['params_config'] = params_config
    return render(request, 'predictor/find_best_parameters.html', context)


def visualize_view(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('plastic_image'):
        image_file = request.FILES['plastic_image']
        identified_type, confidence_score, gatekeeper_result = run_full_image_pipeline(image_file)
        image_file.seek(0)
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        context['uploaded_image'] = encoded_image
        if gatekeeper_result == "plastic":
            context['result'] = PLASTIC_DATABASE.get(identified_type, {
                "name": f"Unknown Plastic ({identified_type})", "viscosity": "N/A", "product_processes": {}
            })
            context['confidence'] = f"{confidence_score:.2%}"
        else:
            context['error'] = "This does not appear to be a plastic item. Please upload a different image."
    return render(request, 'predictor/visualize.html', context)