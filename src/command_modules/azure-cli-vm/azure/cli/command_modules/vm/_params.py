# pylint: disable=line-too-long
import argparse
import getpass
import os

from argcomplete.completers import FilesCompleter

from azure.mgmt.compute.models import VirtualHardDisk

from azure.cli.command_modules.vm._validators import MinMaxValue
from azure.cli.command_modules.vm._actions import (VMImageFieldAction,
                                                   VMSSHFieldAction,
                                                   VMDNSNameAction,
                                                   load_images_from_aliases_doc,
                                                   get_vm_sizes)
from azure.cli.commands.parameters import (location_type,
                                           get_location_completion_list,
                                           get_one_of_subscription_locations,
                                           get_resource_name_completion_list)
from azure.cli.commands import register_cli_argument, CliArgumentType, register_extra_cli_argument

def get_urn_aliases_completion_list(prefix, **kwargs):#pylint: disable=unused-argument
    images = load_images_from_aliases_doc()
    return [i['urn alias'] for i in images]

def get_vm_size_completion_list(prefix, action, parsed_args, **kwargs):#pylint: disable=unused-argument
    location = parsed_args.location if parsed_args.location else get_one_of_subscription_locations()
    result = get_vm_sizes(location)
    return [r.name for r in result]

# BASIC PARAMETER CONFIGURATION
name_arg_type = CliArgumentType(options_list=('--name', '-n'), metavar='NAME')
multi_ids_type = CliArgumentType(
    nargs='+'
)

admin_username_type = CliArgumentType(options_list=('--admin-username',), default=getpass.getuser(), required=False)
existing_vm_name = CliArgumentType(overrides=name_arg_type, help='The name of the virtual machine', completer=get_resource_name_completion_list('Microsoft.Compute/virtualMachines'))
register_cli_argument('vm', 'vm_name', existing_vm_name)
register_cli_argument('vm', 'size', CliArgumentType(completer=get_vm_size_completion_list))

register_cli_argument('vm scaleset', 'vm_scale_set_name', name_arg_type, completer=get_resource_name_completion_list('Microsoft.Compute/virtualMachineScaleSets'))
register_cli_argument('vm scaleset', 'virtual_machine_scale_set_name', name_arg_type)
register_cli_argument('vm scaleset', 'instance_ids', multi_ids_type)
register_cli_argument('vm', 'diskname', CliArgumentType(options_list=('--name', '-n')))
register_cli_argument('vm', 'disksize', CliArgumentType(help='Size of disk (Gb)', default=1023, type=MinMaxValue(1, 1023)))
register_cli_argument('vm', 'lun', CliArgumentType(
    type=int, help='0-based logical unit number (LUN). Max value depends on the Virtual Machine size.'))
register_cli_argument('vm', 'vhd', CliArgumentType(type=VirtualHardDisk))

register_cli_argument('vm availability-set', 'availability_set_name', name_arg_type, completer=get_resource_name_completion_list('Microsoft.Compute/availabilitySets'))

register_cli_argument('vm access', 'username', CliArgumentType(options_list=('--username', '-u'), help='The user name'))
register_cli_argument('vm access', 'password', CliArgumentType(options_list=('--password', '-p'), help='The user password'))

register_cli_argument('vm container', 'orchestrator_type', CliArgumentType(choices=['docs', 'swarm']))
register_cli_argument('vm container', 'admin_username', admin_username_type)
register_cli_argument(
    'vm container', 'ssh_key_value', CliArgumentType(
        required=False,
        help='SSH key file value or key file path.',
        default=os.path.join(os.path.expanduser('~'), '.ssh', 'id_rsa.pub'),
        completer=FilesCompleter()
    )
)
register_cli_argument('vm container create', 'agent_vm_size', CliArgumentType(completer=get_vm_size_completion_list))

register_cli_argument('vm capture', 'overwrite', CliArgumentType(action='store_true'))
register_cli_argument('vm disk', 'vm_name', arg_type=existing_vm_name, options_list=('--vm-name',))
register_cli_argument('vm nic', 'nic_ids', multi_ids_type)
register_cli_argument('vm nic', 'nic_names', multi_ids_type)
register_cli_argument('vm diagnostics', 'vm_name', arg_type=existing_vm_name, options_list=('--vm-name',))
register_cli_argument('vm diagnostics set', 'storage_account', completer=get_resource_name_completion_list('Microsoft.Storage/storageAccounts'))

register_cli_argument('vm extension', 'vm_extension_name', name_arg_type, completer=get_resource_name_completion_list('Microsoft.Compute/virtualMachines/extensions'))
register_cli_argument('vm extension', 'vm_name', arg_type=existing_vm_name, options_list=('--vm-name',))
register_cli_argument('vm extension', 'auto_upgrade_minor_version', CliArgumentType(action='store_true'))

register_cli_argument('vm extension image', 'image_location', CliArgumentType(options_list=('--location', '-l')))
register_cli_argument('vm extension image', 'publisher_name', CliArgumentType(options_list=('--publisher',)))
register_cli_argument('vm extension image', 'type', CliArgumentType(options_list=('--name', '-n')))
register_cli_argument('vm extension image', 'latest', CliArgumentType(action='store_true'))

register_cli_argument('vm image list', 'image_location', location_type)

# VM CREATE PARAMETER CONFIGURATION

authentication_type = CliArgumentType(
    choices=['ssh', 'password'], default=None,
    help='Password or SSH public key authentication. Defaults to password for Windows and SSH public key for Linux.'
)

nsg_rule_type = CliArgumentType(
    choices=['RDP', 'SSH'], default=None,
    help='Network security group rule to create. Defaults to RDP for Windows and SSH for Linux'
)

for scope in ['vm create', 'vm scaleset create']:
    register_cli_argument(scope, 'name', name_arg_type)
    register_cli_argument(scope, 'location', CliArgumentType(completer=get_location_completion_list))
    register_cli_argument(scope, 'custom_os_disk_uri', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'custom_os_disk_type', CliArgumentType(choices=['windows', 'linux']))
    register_cli_argument(scope, 'os_disk_type', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'overprovision', CliArgumentType(action='store_false', default=None, options_list=('--disable-overprovision',)))
    register_cli_argument(scope, 'load_balancer_type', CliArgumentType(choices=['new', 'existing', 'none']))
    register_cli_argument(scope, 'storage_caching', CliArgumentType(choices=['ReadOnly', 'ReadWrite']))
    register_cli_argument(scope, 'upgrade_policy_mode', CliArgumentType(choices=['manual', 'automatic'], default='manual', help=None))
    register_cli_argument(scope, 'nat_backend_port', CliArgumentType(help='Backend NAT port to map.  Defaults to 22 for Linux and 3389 for Windows.', default=None))
    register_cli_argument(scope, 'os_disk_uri', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'os_offer', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'os_publisher', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'os_sku', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'os_type', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'os_version', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'dns_name_type', CliArgumentType(help=argparse.SUPPRESS))
    register_cli_argument(scope, 'admin_username', admin_username_type)
    register_cli_argument(scope, 'ssh_key_value', CliArgumentType(action=VMSSHFieldAction))
    register_cli_argument(scope, 'ssh_dest_key_path', completer=FilesCompleter())
    register_cli_argument(scope, 'dns_name_for_public_ip', CliArgumentType(action=VMDNSNameAction))
    register_cli_argument(scope, 'authentication_type', authentication_type)
    register_cli_argument(scope, 'availability_set_type', CliArgumentType(choices=['none', 'existing'], help='', default='none'))
    register_cli_argument(scope, 'private_ip_address_allocation', CliArgumentType(choices=['dynamic', 'static'], help='', default='dynamic'))
    register_cli_argument(scope, 'public_ip_address_allocation', CliArgumentType(choices=['dynamic', 'static'], help='', default='dynamic'))
    register_cli_argument(scope, 'public_ip_address_type', CliArgumentType(choices=['none', 'new', 'existing'], help='', default='new'))
    register_cli_argument(scope, 'storage_account_type', CliArgumentType(choices=['new', 'existing'], help='', default='new'))
    register_cli_argument(scope, 'virtual_network_type', CliArgumentType(choices=['new', 'existing'], help='', default='new'))
    register_cli_argument(scope, 'network_security_group_rule', nsg_rule_type)
    register_cli_argument(scope, 'network_security_group_type', CliArgumentType(choices=['new', 'existing', 'none'], help='', default='new'))
    register_extra_cli_argument(scope, 'image', options_list=('--image',), action=VMImageFieldAction, completer=get_urn_aliases_completion_list, default='Win2012R2Datacenter')
