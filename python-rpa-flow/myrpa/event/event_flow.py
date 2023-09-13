import ast, time, sys
from async_retrying import retry
import yaml
from jinja2 import Template

from . import test, click_element 

def event_test():
    test()

async def yaml2dict(yamlFileName):
    with open(yamlFileName,encoding='utf-8' ) as f:
        return yaml.safe_load(f)
        
def get_element_actions(pages, data):
    action_map = {
        'a': get_link_xpath,
        'link': get_link_xpath,
        'input': get_input_xpath,
        'div': get_div_xpath,
        'dd': get_dd_xpath,
    }
    action_list = []
    _text = ''
    _check = False
    for page in pages:
        frame = page['title']
        for element in page['elements']:
            action_func = action_map.get(element['type'], None)
            if action_func:
                res = action_func(element, data)

                action_func_name = str(action_func.__name__)

                if action_func_name == 'get_input_xpath':
                    _xpath ,_text = res
                if action_func_name == 'get_div_xpath':
                    _xpath,_check,_text = res
                else:
                    _xpath,_check = res

                action_list.append({'type': element['type'], 'xpath': _xpath, 'text': _text ,'frame': frame, 'name':element['name'] ,'check':_check, 'mark': element['mark'], 'before_delay':element['before_delay'], 'after_delay':element['after_delay'], 'offset':element['offset'],'descript':element['descript']})
    return action_list

def get_link_xpath(element,data):
    if element['xpath']:
        return [element['xpath'], element['check']]
    elif 'id' in element and element['id'] is not None:
        return [f"//*[@id='{element['id']}']", element['check']]
    elif 'title' in element and element['title'] is not None:
        return [f"//*[@title='{element['title']}']", element['check']]

def get_input_xpath(element,data):

    if element['xpath']:
        template = element["xpath"]
        xpath = Template(template).render(data)
        return [xpath, element['text']]
    elif 'name' in element  and element['name']  is not None:
        return [f"input[name='{element['name']}']",{element['text']}]
    else:
        return [element['xpath'], element['text']]

def get_div_xpath(element,data):
    myData = data
    text = ''
    #TODO
    if element['text']:
        templateText = element["text"]
        
        text = Template(templateText).render(myData)
    if element['xpath']:
        templateXpath = element["xpath"]
        
        xpath = Template(templateXpath).render(myData)

    return [xpath, element['check'], text]
    '''
    if 'id' in element and element['id'] is not None:
        return [f"//*[@id='{element['id']}']", element['check']]
    elif 'class' in element  and element['class'] is not None:
        return [f"//div[@class={element['class']}]", element['check']]
    '''

def get_dd_xpath(element,data):
    if 'text' in element  and element['text']  is not None:
        text = element['text']
        if 'f"{' in str(text) or "f'{" in str(text):
            text = str(element['text'])[3:-2]
            text = eval(text.replace('\\',''))

        return [f"//dd[contains(text(), '{text}')]",element['check']]
    else:
        return [element['xpath'], element['check']]

@retry(attempts=3,kwargs=True)
async def run_action_on_page_element(page, action, element_info, _check=False, _offset=0, _descript='', _mark='', _data={}):
    click = True
    res = False
    if 'input' in action:
        click = False
    _xpath, _frame, _delays = element_info[0], element_info[1], element_info[2] 
    if click:
        if element_info[3]:
            res = await click_element(page=page, xpath=_xpath, text=element_info[3],frame=_frame, check=_check, before_delay=_delays[0], after_delay=_delays[1], offset=_offset, descript=_descript, mark=_mark, data=_data)
        else:
            res = await click_element(page=page, xpath=_xpath, text=None,frame=_frame, check=_check, before_delay=_delays[0], after_delay=_delays[1], offset=_offset, descript=_descript, mark=_mark, data=_data)
    else:
        _text = element_info[3]
        res = await type_text(page, xpath=_xpath, text=_text ,frame=_frame)

    return res

async def event_go(obj,data,action):
    dicts = await yaml2dict(f'./event/yml/{action}.yaml')
    dictList = get_element_actions(dicts['pages'],data)
    myData = data
    swich_line = False
    skip_offset= 0
    res = [False,None,0]  
    j = 0
    for i in dictList:
        right_obj = obj
        if j>1:
            i['frame'] = None
            right_obj = res[1]

        if i['check']:
            skip_offset = i['offset']
            
        
        if skip_offset:
            if i['offset'] == skip_offset or i['offset'] == int(skip_offset.__str__()[0:2])*11:
                swich_line = False
            else:
                continue
        if swich_line == False:
            if i['type'] != 'input':

                if 'check' in i and i['check'] == True:
                    res = await run_action_on_page_element(right_obj, i['type'], [i['xpath'],i['frame'],(i['before_delay'],i['after_delay']),i['text']],i['check'],i['offset'],i['descript'],i['mark'],data)
                else:
                    res = await run_action_on_page_element(right_obj, i['type'], [i['xpath'],i['frame'],(i['before_delay'],i['after_delay']),i['text']],0,i['offset'],i['descript'],i['mark'],data)
            else:
                template = i['text']
                text = Template(template).render(myData)
                res = await run_action_on_page_element(right_obj, i['type'], [i['xpath'],i['frame'],(i['before_delay'],i['after_delay']),text],data)

            if res[0]:

                skip_offset = res[2]
                if i['offset'] == -3:
                    break

            else:
                swich_line = False

                if res[2] not in [-1, -2, -3]:

                    skip_offset = res[2]
            j = j+1
        '''
        else:
            swich_line = False
            continue
        '''
    return res[0]