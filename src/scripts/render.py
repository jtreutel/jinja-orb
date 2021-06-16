#!/usr/bin/python3

import re, os, glob, yaml, sys
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(''))

def get_templates_in_dir(path):
  file_list = []
  for extension in ["j2", "jinja"]:
    file_list += glob.glob(f'{path}/*.{extension}')
  return file_list 

#Use the path and output directory supplied by the orb arguments
supplied_path = os.environ['PARAM_PATH'].rstrip("/")
output_dir = os.environ['PARAM_OUTPUTDIR'].rstrip("/")


templates_to_render = []
if os.path.isfile(supplied_path):
  templates_to_render.append(supplied_path)
# If supplied path is a directory, scan it for .j2 and .jinja files
elif os.path.isdir(supplied_path):
  print("It's a directory!") #DEBUG
  templates_to_render = get_templates_in_dir(supplied_path)
  print(templates_to_render)
else:
  print("No file/directory found at path \"%s\"!" % (supplied_path))
  sys.exit(1)


#Create the output directory if it doesn't already exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Render the templates
for template_path in templates_to_render:
    template = env.get_template(template_path)

    parsed_template = template.render(os.environ) #templatevars)

    #Write rendered template to output_dir
    #group(0) gets the filepath minus jinja extension; group(2) gets just the filename
    filename = re.search(r"(.*\/)(.*?)(?=(\.jinja)|(\.j2))", template_path).group(2)
    with open('/'.join([output_dir, filename]), "w") as fh:
        fh.write(parsed_template)