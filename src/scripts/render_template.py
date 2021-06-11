import re, os, glob, yaml
from sys import exit
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('')) #default dir is ./templates

def get_templates_in_dir(path):
  file_list = []
  stripped_path = path.rstrip("/")
  for extension in ["j2", "jinja"]:
    file_list += glob.glob(f'%{stripped_path}/*.{extension}')
  return file_list 

#Use the path and outpute directory supplied by the orb arguments
templates_to_render = [sys.argv[0]]
output_dir = sys.argv[1]

#Check if the supplied path exists
if not os.path.isfile(templates_to_render[0]):
  print("No file/directory found at path %s!" % (templates_to_render[0]))
  sys.exit(1)

# If supplied path is a directory, scan it for .j2 and .jinja files
if os.path.isdir(templates_to_render):
  templates_to_render = get_templates_in_dir(templates_to_render)

# Get all env vars in the machine/container for use in Jinja template rendering
# Convert the os.environ object to a dict, then format each env var assignment like so: FOO="bar"
templatevars = ', '.join(f'{k}="{v}"' for k, v in dict(os.environ).items())

#Create the output directory if it doesn't already exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Render the templates
for template_path in templates_to_render:
    template = env.get_template(template_path)

    parsed_template = template.render(templatevars)

    #Write rendered template to ./rendered/foo.tf
    #TODO: figure out regex
    filename = re.search(r"(?<=\.\/templates\/).*?(?=\.j2)", template_path).group(0)
    with open(''.join(["./rendered/", filename]), "w") as fh:
        fh.write(parsed_template)