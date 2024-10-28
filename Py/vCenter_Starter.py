#starter
from pyVim.connect import SmartConnect
import ssl
import getpass
import pyVmomi
from pyVmomi import vim


def vm_details(vm):
    summary = vm.summary
    config = summary.config
    runtime = summary.runtime
    guest = summary.guest


    vm_deets = {
        'VM Name': config.name,
        'State': runtime.powerState,
        'CPUs': config.numCpu,
        'Memory GB': config.memorySizeMB / 1024,
        'IP Address': guest.ipAddress if guest.toolsStatus == 'toolsOK' and guest.ipAddress else 'Not Available'
    }
    return vm_deets

def search_vms(content, name_filter=None, limit=1000):
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

    vms = container.view
    container.Destroy()

    print(f"total VMs were found: {len(vms)}")

    filtered_vms = []
    for vm in vms:    
        print(f"Checking VM: {vm.name}")
        vm_deets = vm_details(vm)

        print(f"Adding VM Info: {vm_deets['VM Name']}")
        filtered_vms.append(vm_deets)
    print(f"total VMS after filter: {len(vms)}")
        
    return filtered_vms


context = ssl._create_unverified_context()

passw = getpass.getpass()
si=SmartConnect(host="vcenter01-ainsley.ainsley.local", user="administrator@vsphere.local", pwd=passw, sslContext=context)

aboutInfo =si.content.about

s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode=ssl.CERT_NONE

content = si.content

limit = 1000
vm_name_filter = ("")
vms = search_vms(content,vm_name_filter, limit)
print(f"total VMs printed: {len(vms)}")

for vm in vms:
    print(f"VM Name: {vm['VM Name']}")
    print(f"State: {vm['State']}")
    print(f"CPUs: {vm['CPUs']}")
    print(f"Memory GB: {vm['Memory GB']}")
    print(f"IP Address: {vm['IP Address']}")
    print("-" * 40)
   
    


