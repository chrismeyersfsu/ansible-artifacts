DOCUMENTATION = '''
---
module: set_artifact
short_description: Save Ansible variables for use across playbook invocations
description:
    - Saves a user-specified JSON dictionary of variables from a playbook
      for later use. Operates similar to set_fact with variable merge and 
      overwrite behavior. Operates similar to add_host in this module is an 
      action plugin and only runs once, on the first host, for which it sets 
      facts for.
version_added: "2.2"
options:
requirements: [ ]
author: Alan Rominger and Chris Meyers
'''

EXAMPLES = '''
# Example fact output:
# Simple specifying of an artifact dictionary, will be passed on callback
- set_artifact:
    data:
        one_artifact: "{{ local_var * 2 }}"
        another_artifact: "{{ some_registered_var.results | map(attribute='ansible_facts.some_fact') | list }}"

# Init
- set_artifact:
    data:
        a: 7

# Overwrite a with 8 and add b, with a value of 9, to the artifact dictionary
- set_artifact:
    data:
        a: 8
        b: 9

# Specifying a local path to save the artifacts to
# TODO
- set_artifact:
    data:
        one_artifact: "{{ local_var * 2 }}"
        another_artifact: "{{ some_registered_var.results | map(attribute='ansible_facts.some_fact') | list }}"
    dest=/tmp/prefix-{{ inventory_hostname }}
host | success >> {
    "artifact_data": {}
}
'''
