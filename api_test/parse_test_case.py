import re

from api_test import exception


class TestCaseParser():
    def __init__(self, bind_variables={}):
        self.bind_variables = bind_variables

    def parse(self, test_case_template):
        """ parse test_case_template, replace all variables with bind value.
                variables marker: ${variable}.
                @param test_case_template
                    "request": {
                        "url": "http://127.0.0.1:5000/api/users/${uid}/",
                        "method": "POST",
                        "headers": {
                            "Content-Type": "application/json",
                            "authorization": "${authorization}",
                            "random": "${random}"
                        },
                        "body": "${json}"
                    },
                    "response": {
                        "status_code": "${expected_status}",
                        "headers": {
                            "Content-Type": "application/json"
                        },
                        "body": {
                            "success": True,
                            "msg": "user created successfully."
                        }
                    }
        """
        return self.substitute(test_case_template)

    def substitute(self, content):
        """ substitute content recursively, each variable will be replaced with bind value.
            variables marker: ${variable}.
        """
        if isinstance(content, str):
            matched = re.match(r'(.*)\$\{(.*)\}(.*)', content)
            if matched:
                variable_name = matched.group(2)
                value = self.bind_variables.get(variable_name)
                if value is None:
                    raise exception.ParamsError('%s is not defined in bind variables!' % variable_name)
                if matched.group(1) or matched.group(3):
                    return re.sub(r'\$\{.*\}', value, content)
                return value
            return content

        if isinstance(content, list):
            return [self.substitute(item) for item in content]

        if isinstance(content, dict):
            parsed_content = {}
            for key, value in content.items():
                parsed_content[key] = self.substitute(value)
            return parsed_content
        return content
