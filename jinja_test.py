from jinja2 import Template

def isis_config(NET):
    config_template = Template(open('xr_isis_base.xml').read())
    config_render = config_template.render(
        NET='49.0000.0000.0001.00', 
    )
    return(config_render)

