from django.shortcuts import render
from .mixins import HttpResponseMixin, SerializeMixin
from .utils import is_json
from .models import Student
from .forms import StudentForm
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class StudentCRUDCBV(HttpResponseMixin, SerializeMixin, View):

    def get_object_by_id(self, name):
        try:
            #s = Student.objects.get(name__icontains=name)
            #s = Student.objects.filter(name__contains=name)
            s = Student.objects.filter(name__icontains=name).first()
            print(s)
        except Student.DoesNotExist:
            s = None
        return s

    def get(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            return self.render_to_http_response(json.dumps({'msg': 'please provide valid jason data'}), status=400)
        pyData = json.loads(data)
        id = pyData.get('name', None)
        if id is not None:
            std = self.get_object_by_id(id)
            if std is None:
                return self.render_to_http_response(json.dumps({'msg': 'no matched data with corresponding id'}),
                                                    status=400)
            json_data = self.serialize([std], )
            return self.render_to_http_response(json_data)
        qs = Student.objects.all()
        json_data = self.serialize(qs)
        return self.render_to_http_response(json_data)

    def post(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            return self.render_to_http_response(json.dumps({'msg': 'Please provide valid jason data only'}), status=400)
        std_data = json.loads(data)
        form = StudentForm(std_data)
        if form.is_valid():
            form.save()
            return self.render_to_http_response(json.dumps({'nsg': 'Resource inserted successfully'}))
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=400)

    def put(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            return self.render_to_http_response(json.dumps({'msg': 'Please provide valid jason data only'}), status=400)
        provided_data = json.loads(data)
        id = provided_data.get('id', None)
        if id is None:
            return self.render_to_http_response(json.dumps({'msg': 'Please provide valid data'}),
                                                status=400)
        std_data = self.get_object_by_id(id)
        if std_data is None:
            return self.render_to_http_response(json.dumps({'msg': 'Data is not updated due to invalid id'}),
                                                status=400)
        original_data = {
            'name': std_data.name,
            'rollNo': std_data.rollNo,
            'marks': std_data.marks,
            'subjects': std_data.subjects,
        }
        original_data.update(provided_data)
        form = StudentForm(original_data, instance=std_data)
        if form.is_valid():
            form.save()
            return self.render_to_http_response(json.dumps({'msg': 'Data updated successfully'}))
        if form.errors:
            error_data = json.dumps(form.errors)
            return self.render_to_http_response(error_data, status=400)

    def delete(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            return self.render_to_http_response(json.dumps({'msg': 'Please provide valid jason data only'}), status=400)
        provided_data = json.loads(data)
        id = provided_data.get('id', None)
        if id is None:
            return self.render_to_http_response(json.dumps({'msg': 'Please provide valid id to delete'}),
                                                status=400)
        std_data = self.get_object_by_id(id)
        if std_data is None:
            return self.render_to_http_response(json.dumps({'msg': 'Data is not deleted due to invalid id'}),
                                                status=400)
        status, deleted_item = std_data.delete()
        if status == 1:
            json_data = json.dumps({'msg': 'Resource deleted successfully'})
            return self.render_to_http_response(json_data)
        json_data = json.dumps({'msg': 'Unable to  delete resource'})
        return self.render_to_http_response(json_data, status=500)