from os import path, pardir, getcwd


MY_IP = '0.0.0.0'
CONTROL_PORT = 8776
MONITOR_PORT = 8777
MODAL_NAME = 'model.pkl'

IDASHBOARD_IP = "0.0.0.0"
IDASHBOARD_PORT = 8000


BASE_PATH = path.normpath(path.join(getcwd(), "network_files"))
LOG_PATH = '/Users/Claude/'
SAMPLE_LOG = 'sample.log'

GUEST_OS_ADMIN = "idbadmin"
GUEST_OS_PASSWD = "thutnsidb"


# === NETWORK OPERATION TYPE ===
CREATE_INTNET = "create_intnet"
DELETE_INTNET = "delete_intnet"
ADD_VM_TO_INTNET = "add_vm_to_intnet"

CREATE_HOSTONLY = "create_hostonly"
DELETE_HOSTONLY = "delete_hostonly"
ADD_VM_TO_HOSTONLY = "add_vm_to_hostonly"

REMOVE_VM_FROM_NETWORK = "remove_vm_from_network"


# === REQUEST RESULT ===
EXECUTION_ERROR = "execution_error"
RESULT_SUCCESS = "success"
REQUEST_ERROR = "request_error"


# === REQUEST TYPE ===

