from django.test import TestCase, Client
from django.urls import reverse
from .models import Machine, ProductionLog
import json


class ViewsTestCase(TestCase):

    def setUp(self):
        # Create sample data for testing
        self.machine = Machine.objects.create(machine_name='Test Machine', machine_serial_no='12345')
        self.log = ProductionLog.objects.create(unique_id='ABC123', cycle_no=1, material_name='Test Material',
                                                machine=self.machine, start_time='2024-04-01T08:00:00Z',
                                                end_time='2024-04-01T09:00:00Z', duration=60)

    def test_main_view(self):
        client = Client()
        response = client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_machine_view(self):
        client = Client()
        response = client.get(reverse('machine_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'machine.html')

    def test_logs_view(self):
        client = Client()
        response = client.get(reverse('logs_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logs.html')

    def test_add_machine_view(self):
        client = Client()
        data = {'machine_name': 'New Machine', 'machine_serial_no': '67890'}
        response = client.post(reverse('add_machine'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Machine.objects.count(), 2)  # Check if machine was added

    def test_add_log_view(self):
        client = Client()
        data = {'unique_id': 'XYZ456', 'cycle_no': 2, 'material_name': 'New Material',
                'machine': self.machine.id, 'start_time': '2024-04-02T08:00:00Z',
                'end_time': '2024-04-02T09:00:00Z', 'duration': 60}
        response = client.post(reverse('add_log'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ProductionLog.objects.count(), 2)  # Check if log was added

    # def test_oee_data_all_view(self):
    #     client = Client()
    #     response = client.get(reverse('oee_data_all'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.json()), 1)  # Check if correct number of data entries are returned

    def test_oee_data_by_machine_view(self):
        client = Client()
        response = client.get(reverse('oee_data_by_machine', kwargs={'machine_id': self.machine.id}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['machine_name'], 'Test Machine')
        # You may need to adjust this assertion depending on the expected behavior of your oee_data_by_machine view

    def test_filter_oee_data_view(self):
        client = Client()
        data = {'machine': self.machine.id, 'start_date': '2024-04-01', 'end_date': '2024-04-01'}
        response = client.post(reverse('filter_oee_data'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
