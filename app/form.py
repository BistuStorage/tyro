# coding=utf-8

from web import form
from models import datatype

namerules=form.regexp(ur'^[a-zA-Z0-9_\u4e00-\u9fa5]*$',u'非空：中文、英文、数字、下划线')
colnumrules=form.regexp(r'^[1-9][0-9]?$',u'必须是数字，且为1-99')
pkrules=form.regexp(ur'^[a-zA-Z0-9_,\u4e00-\u9fa5]*$',u'非空：中文、英文、数字、下划线、逗号')
filetype = ['xls','csv']

table_form = form.Form(
    form.Textbox("tablename",namerules,description=u"表名"),
    form.Textbox("columns",colnumrules,description=u"列数"),
)

uploadfile_form = form.Form(
    form.Textbox("tablename",namerules,description=u"表名"),
    form.Dropdown('filetype',filetype,description=u"文件类型"),
    form.File("datafile",form.notnull,description=u"文件"),
)

search_form=form.Form(
    form.Textbox("content",form.notnull,description=""),
)

class DynamicForm(form.Form):
    def add_input(self, new_input):
        list_inputs = list(self.inputs)
        list_inputs.append(new_input)
        self.inputs = tuple(list_inputs)


def custom_form(f,num):
    for idx in range(num):
        f.add_input(form.Textbox('name' + str(idx),namerules,description=u"列名"+str(idx)))
        f.add_input(form.Dropdown('attr' + str(idx),datatype,description=u"属性"+str(idx)))
    f.add_input(form.Textbox("primarykey",pkrules,description=u"主键"))
    return f

def custom_master(f,fields):
    for fn in fields:
        f.add_input(form.Checkbox(fn))
    return f
