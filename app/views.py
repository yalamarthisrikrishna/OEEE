# oee_app/views.py
import json
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
from .models import Machine, ProductionLog
from .utils import calculate_oee
from django.template import loader


def oee_data_all(request):
    if request.method == 'GET':
        machines = Machine.objects.all()
        oee_data = []
        for machine in machines:
            # Calculate OEE for each machine
            oee = calculate_oee_for_machine(machine)
            oee_data.append({
                'machine_name': machine.machine_name,
                'oee': oee
            })
        return oee_data
    else:
        return JsonResponse({"message": "Method not allowed"},status=404)


def oee_data_by_machine(request, machine_id):
    if request.method == 'GET':
        machine = get_object_or_404(Machine, pk=machine_id)
        oee = calculate_oee_for_machine(machine)
        return JsonResponse({'machine_name': machine.machine_name, 'oee': oee})
    else:
        return JsonResponse({"message": "Method not allowed"},status=404)


def filter_oee_data(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # Retrieve request parameters for filtering
        machine_id = body['machine']
        start_date = body['start_date']
        end_date = body['end_date']

        # Define initial queryset
        queryset = ProductionLog.objects.all()

        # Apply filters based on request parameters
        if machine_id:
            queryset = queryset.filter(machine_id=machine_id)
        if start_date:
            queryset = queryset.filter(start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_time__lte=end_date)

        # Calculate OEE for filtered data
        oee_data = []
        for production_log in queryset:
            machine = production_log.machine
            oee = calculate_oee_for_machine(machine)
            oee_data.append({
                'machine_name': machine.machine_name,
                'oee': oee
            })

        return JsonResponse(oee_data, safe=False)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=404)

def calculate_oee_for_machine(machine):
    # Retrieve relevant ProductionLog entries for the machine
    production_logs = ProductionLog.objects.filter(machine=machine)

    # Calculate Available Time per shift (assuming 3 shifts of 8 hours each)
    available_time_per_shift = 8  # in hours

    # Calculate Available Operating Time
    total_products = production_logs.count()
    ideal_cycle_time = 5  # in minutes
    available_operating_time = total_products * (ideal_cycle_time / 60)  # convert minutes to hours

    if available_operating_time == 0:
        return 0

    # Calculate Unplanned Downtime
    unplanned_downtime = available_time_per_shift - available_operating_time

    # Calculate Actual Output (No. of products produced)
    actual_output = total_products

    # Calculate Performance
    performance = (ideal_cycle_time / 60) * actual_output / available_operating_time * 100

    # Calculate Quality
    good_products = production_logs.filter(duration=ideal_cycle_time).count()
    quality = good_products / total_products * 100

    # Calculate Availability
    availability = (available_time_per_shift - unplanned_downtime) / available_time_per_shift * 100

    # Calculate OEE using the provided formula
    oee = calculate_oee(availability, performance, quality)

    return oee


def main(request):
    machinery_logs = oee_data_all(request)
    print(machinery_logs)
    machines = Machine.objects.all()
    print(machinery_logs)
    template = loader.get_template('main.html')
    context = {"machinery_logs": machinery_logs, "machines":machines}
    return HttpResponse(template.render(context,request))


def add_machine(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        machine_name = body['machine_name']
        machine_serial_no = body['machine_serial_no']

        # Create a new Machine object and save it to the database
        machine = Machine(machine_name=machine_name, machine_serial_no=machine_serial_no)
        machine.save()

        return JsonResponse({'message': 'Machine added successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def add_log(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        unique_id = body['unique_id']
        cycle_no = body['cycle_no']
        material_name = body['material_name']
        machine_id = body['machine']
        machine = get_object_or_404(Machine, pk=machine_id)
        start_time = body['start_time']
        end_time = body['end_time']
        duration = body['duration']

        # Create a new Machine object and save it to the database
        log = ProductionLog(unique_id=unique_id, cycle_no=cycle_no, material_name=material_name, machine=machine, start_time=start_time, end_time=end_time, duration=duration )
        log.save()

        return JsonResponse({'message': 'log added successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def machine_view(request):
    template = loader.get_template('machine.html')
    return HttpResponse(template.render())


def logs_view(request):
    template = loader.get_template('logs.html')
    machines = Machine.objects.all()
    context = {"machines": machines}
    return HttpResponse(template.render(context,request))
