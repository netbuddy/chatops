import yaml

# domain_data = None
# with open('domain.yml', 'r', encoding='utf-8') as domain_file:
#     # domain_data = yaml.load(domain_file,Loader=yaml.FullLoader)#读取yaml文件
#     domain_data_list = list(yaml.safe_load_all(domain_file))
#     domain_data = domain_data_list[0]

# with open('domain.yml', 'w', encoding='utf-8') as domain_file:
#     if(domain_data['intents'] is None):
#         domain_data['intents'] = []
#     domain_data['intents'].append('upload_file')
#     yaml.safe_dump_all(domain_data_list, domain_file, sort_keys=False,  allow_unicode=True)

# nlu_data = None
# with open('data/nlu.yml', 'r', encoding='utf-8') as nlu_file:
#     nlu_data_list = list(yaml.safe_load_all(nlu_file))
#     nlu_data = nlu_data_list[0]

# with open('data/nlu.yml', 'w', encoding='utf-8') as nlu_file:
#     if(nlu_data['nlu'] is None):
#         nlu_data['nlu'] = []
#     nlu_data['nlu'].append({'intent': 'upload_file', 'examples': '- 上传文件\n- 拷贝文件\n'})
#     yaml.safe_dump_all(nlu_data_list, nlu_file, sort_keys=False,  allow_unicode=True)

def set_slot(domain_data, name, type, form_name):
    if(domain_data['slots'] is None):
        domain_data['slots'] = {}
    domain_data['slots'][name] = {'type': type, 'influence_conversation': True, 'mappings': [{'type': 'from_text', 'conditions': [{'active_loop': form_name, 'requested_slot': name}]}]}

def set_form(domain_data, name, slots):
    if(domain_data['forms'] is None):
        domain_data['forms'] = {}
    domain_data['forms'][name] = {'required_slots': slots}

domain_data_list = None
domain_data = None
with open('domain.yml', 'r', encoding='utf-8') as domain_file:
    domain_data_list = list(yaml.safe_load_all(domain_file))
    domain_data = domain_data_list[0]

set_slot(domain_data, 'dest_ip', 'text', 'upload_file_form')
set_slot(domain_data, 'username', 'text', 'upload_file_form')
set_slot(domain_data, 'password', 'text', 'upload_file_form')
set_form(domain_data, 'upload_file_form', ['dest_ip', 'username', 'password'])

with open('domain.yml', 'w', encoding='utf-8') as domain_file:
    yaml.safe_dump_all(domain_data_list, domain_file, sort_keys=False,  allow_unicode=True)