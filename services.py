from django.http import HttpResponse

def django_soap_app(request):
    return HttpResponse("SOAP Service is working!")

def wsdl_view(request):
    return HttpResponse("WSDL is available!")
