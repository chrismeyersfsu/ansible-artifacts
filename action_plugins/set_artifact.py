__metaclass__ = type

import json
import yaml
import os

from ansible.compat.six import string_types
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleUndefinedVariable
from ansible.parsing.yaml.dumper import AnsibleDumper

FACT_KEY = 'artifact_data'

class ActionModule(ActionBase):

    # Ensure this task runs on one host, the first host. Similar logic 
    # in add_host
    BYPASS_HOST_LOOP = True

    # We don't plan on executing this module on the remote host, so don't
    # put this module on the "remote" host
    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if self._play_context.check_mode:
            result['skipped'] = True
            result['msg'] = 'check mode not (yet) supported for this module'
            return result

        param_data = self._task.args.get('data', {})
        param_dest = self._task.args.get('dest', None)

        try:
            artifacts_previous = self._templar.template("{{" + FACT_KEY + "}}", convert_bare=False, fail_on_undefined=True)
        except AnsibleUndefinedVariable:
            artifacts_previous = dict()

        artifacts_new = dict(artifacts_previous)
        artifacts_new.update(param_data)
        is_diff = bool(cmp(artifacts_previous, artifacts_new))

        artifacts_wrapped = dict()
        artifacts_wrapped[FACT_KEY] = artifacts_new

        result['changed'] = is_diff
        result['ansible_facts'] = artifacts_wrapped
        result[FACT_KEY] = artifacts_new

        if param_dest:
            try:
                real_dest = os.path.expanduser(param_dest)
                with open(real_dest, 'w') as f:
                    f.truncate(0)
                    f.write(yaml.dump(artifacts_new, Dumper=AnsibleDumper, indent=4, allow_unicode=True, default_flow_style=False))
            except IOError as e:
                return dict(failed=True, msg=str(e))
            
        return result

