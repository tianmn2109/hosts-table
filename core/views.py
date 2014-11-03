import os
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import dmidecode

from core.models import Raw, Host,Update

import xlwt
from datetime import datetime

SERVER = 'http://tianmn2109-OptiPlex-755.bj.intel.com:8000'
DELIMITER = 'a_123454321_a'
CODE_VERSION = '0.2'
CODE = open(os.path.join(os.path.dirname(__file__), 'collect.sh')).read()


def version(request):
    return HttpResponse(CODE_VERSION, content_type='text/plain')


def collect(request):
    code = CODE % {
        'version': CODE_VERSION,
        'collect_url': SERVER + reverse('collect'),
        'version_url': SERVER + reverse('version'),
        'upload_url': SERVER + reverse('upload'),
        'delimiter': DELIMITER,
        }
    return HttpResponse(code, content_type="text/plain")


@require_POST
@csrf_exempt
def upload(request):
    try:
        ip = request.META['REMOTE_ADDR']

        data = {}
        for sec in request.body.strip().split(DELIMITER):
            typ, content = sec.strip().split('\n', 1)
            data[typ] = content.strip()
            print data[typ]
            print content.strip()

        raw, _ = Raw.objects.get_or_create(ip=ip)
        raw.data = json.dumps(data)
        raw.save()

        # TODO: async
        update_host(ip, data)
    except Exception as err:
        import traceback
        traceback.print_exc()
    return HttpResponse('Done', content_type='text/plain')

def parse_args(data):
    content = data['args']
    #print content
    arglist = content.strip().split(';')
    #print arglist
    item = iter(arglist)
    while True:
        try:
            each = item.next()
        except StopIteration:
            break
     #   print each.strip()
      #  print each.strip().split('=')[0]
       # print each.strip().split('=')[1]
        data[each.strip().split('=')[0]] = each.strip().split('=')[1]
    

def download(request):
    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.num_format_str = 'D-MMM-YY'
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    column = ['Host','Mac Address','Memory','Disk','CPU','UUID / SN','OS infomation','Maintainer','Badge number','Machine postion','Update']
    col = 0
    for item in column:
        ws.write(0,col,item)
        col += 1

    hosts = Host.objects.all()
    row,col = 1,0
    for h in hosts:
        ws.write(row,0,h.hostname + "(" + h.ip + ")")
        ws.write(row,1,h.mac)
        ws.write(row,2,h.memory)
        ws.write(row,3,h.disk)
        ws.write(row,4,h.cpus)
        ws.write(row,5,h.uuid + "/" + h.sn)
        ws.write(row,6,h.osinfo)
        ws.write(row,7,h.maintainer)
        ws.write(row,8,h.badgenumber)
        ws.write(row,9,h.machinepos)
        ws.write(row,10,h.updated.strftime( '%-Y-%-m-%-d %H:%M'))
        row += 1
 
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mymodel.xls"'
    wb.save(response)
    return response

def parse_df(content):
    '''
Filesystem     Type 1G-blocks  Used Available Use% Mounted on
/dev/sda1      ext4      910G  230G      634G  27% /
    '''
    lines = content.strip().splitlines()
    total = 0
    for line in lines[1:]:
        size = line.split()[2]
        total += int(size.rstrip('G'))
    return '%dG' % total 
#def parse_mac(content):
#    list = []
#    lines = content.strip().splitlines()
#    for line in lines:
#        if ((pos = line.find("HWaddr")) != -1) #error
#             list.append(line[pos+6:])
#    return "%s" % str(list)
            

def update_host(ip, data):
    hostname = data['hostname']
    disk_size = parse_df(data['df'])
    dmi = dmidecode.humanize(dmidecode.parse_dmi(data['dmidecode']))
    
    operation = "update"
    try:
        Host.objects.get(uuid=dmi['uuid'])
    except Exception:
        operation = "new"
    
    host, _ = Host.objects.get_or_create(uuid=dmi['uuid'])
    host.sn = dmi['sn']
    host.mac = data['mac']
    host.osinfo = data['osinfo']
    host.hostname = hostname
    host.ip = ip
    #host.model = parse_mac(data['mac'])
    host.cpus = dmi['cpus']
    host.memory = dmi['memory']
    host.disk = disk_size
    host.slots = dmi['slots']
    #host.maintainer = "for test"
    #host.machinepos = 'for test'
    #host.badgenumber = 'for test'
    parse_args(data)
    if (data.has_key('position') and data['position'] != ""):
        host.machinepos = data['position']
    if (data.has_key('name') and data['name'] != ""):
        host.maintainer = data['name']
    if (data.has_key('badge') and data['badge'] != ""):
        host.badgenumber = data['badge']
    host.save()
        
    update,_ = Update.objects.get_or_create(uuid="sss")
    update.uuid = dmi['uuid']
    update.hostname = hostname
    update.operation = operation
    update.save()

def index(request):
    hosts = Host.objects.all()
    return render(request, 'core/index.html', {
            'hosts': hosts,
            })

def updaterecord(request):
    updates = Update.objects.all()
    return render(request, 'core/update.html', {
            'updates': updates,
            })

def example(request):
    return render(request, 'core/example.html')

def raw(request, ip):
    try:
        raw = Raw.objects.get(ip=ip)
    except Raw.DoesNotExist:
        return "Not found"
    return render(request, 'core/raw.html', {
            'data': json.loads(raw.data),
            })
