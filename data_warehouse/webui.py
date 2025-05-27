from data_stack.web import webui
from data_warehouse import registration

registration.register_all()

webui.run()
