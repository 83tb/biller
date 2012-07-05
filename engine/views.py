from django.template import loader, Context,RequestContext
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from biller.engine.models import *

from django.contrib.auth.decorators import login_required

@login_required
def connections(request):

        t = loader.get_template("connections.html")
        user=User.objects.filter(id=request.user.id)
        owner_id = Company.objects.filter(userid=user)[0].client_id

        c = RequestContext(request,{
            'connections': Connection.objects.filter(owner=owner_id).order_by('-end'),
            })
        return HttpResponse(t.render(c))
    
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse

# Create a Dispatcher; this handles the calls and translates info to function maps
#dispatcher = SimpleXMLRPCDispatcher() # Python 2.4
dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None) # Python 2.5


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def rpc_handler(request):
        """
        the actual handler:
        if you setup your urls.py properly, all calls to the xml-rpc service
        should be routed through here.
        If post data is defined, it assumes it's XML-RPC and tries to process as such
        Empty post assumes you're viewing from a browser and tells you about the service.
        """

        if len(request.POST):
                response = HttpResponse(mimetype="application/xml")
                response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
        else:
                response = HttpResponse()
                response.write("<b>Welcome to Biller. This is an XML-RPC Service.</b><br>")
                response.write("You need to invoke it using an XML-RPC Client!<br>")
                response.write("The following methods are available:<ul>")
                methods = dispatcher.system_listMethods()

                for method in methods:
                        # right now, my version of SimpleXMLRPCDispatcher always
                        # returns "signatures not supported"... :(
                        # but, in an ideal world it will tell users what args are expected
                        sig = dispatcher.system_methodSignature(method)

                        # this just reads your docblock, so fill it in!
                        help =  dispatcher.system_methodHelp(method)

                        response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))

                response.write("</ul>")
                response.write('<a href="http://www.djangoproject.com/"> <img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')

        response['Content-length'] = str(len(response.content))
        return response






def bill(source,destination,duration, start, end, operator, uniqueid, type, host):
#def bill():

        """
        Billing is fun. Takes 8 arguments,
        1) source of the call ex. 227383060
        2) destination, ex 600026904
        3) duration of the call like "124" seconds
        4) exact datetime of the beginning of the call,
        5) exact datetime of the end of the call,
        6) operator - trunk in which connection was originated
        7) uniqueid of the connection
        8) type ( INCOMING, OUTGOING )
        9) owner

        """
        from biller.engine.models import Connection, Number

        #add a billing checking for source number to bill it
        numbers_1 = Number.objects.filter(full_number=source)
        numbers_2 = Number.objects.filter(full_number="22738"+source)

        # ensure only one hit
        if len(numbers_1)>1 or len(numbers_2)>1 or len(numbers_1) == 0 and len(numbers_2)==0:
            return False
        else:


            if len(numbers_1)!= 0:
                owner = numbers_1[0].client_id

            if len(numbers_2)!= 0:
                source = "22738"+source
                owner = numbers_2[0].client_id





            Connection.objects.create(source=source,destination=destination,
                                  duration=duration,start=start,
                                  end=end, operator=operator,
                                  uniqueid=uniqueid,host=host,type=type,
                                  owner=owner)



            return True


        #return source



dispatcher.register_function(bill, 'bill')


