import json

def try_safe_json_parse(response_text):
    try:
        # tentative de parsing direct
        return json.loads(response_text), None
    except json.JSONDecodeError as e:
        # on tente de "fermer proprement"
        fixed = response_text.strip()
        if fixed.endswith(','):
            fixed = fixed[:-1]
        if not fixed.endswith(']'):
            fixed += '\n]'
        try:
            return json.loads(fixed), None
        except Exception as e2:
            return None, str(e2)
