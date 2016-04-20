{% if 'IN_CREATE' in data['data']['change'] %}
slack_alert:
  local.slack.post_message:
    - tgt: {{ data['data']['id'] }}
    - kwarg:
        channel: "#channel"
        message: "file: `{{ data['data']['path'] }}` CREATED on `{{ data['data']['id'] }}`."
        from_name: "bot_user"
        api_key: xxxx-xxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
{% endif %}

{% if 'IN_MODIFY' in data['data']['change'] %}
slack_alert:
  local.slack.post_message:
    - tgt: {{ data['data']['id'] }}
    - kwarg:
        channel: "#channel"
        message: "file: `{{ data['data']['path'] }}` MODIFIED on `{{ data['data']['id'] }}`."
        from_name: "bot_user"
        api_key: xxxx-xxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
{% endif %}

{% if 'IN_DELETE' in data['data']['change'] %}
slack_alert:
  local.slack.post_message:
    - tgt: {{ data['data']['id'] }}
    - kwarg:
        channel: "#channel"
        message: "file: `{{ data['data']['path'] }}` DELETED on `{{ data['data']['id'] }}`."
        from_name: "bot_user"
        api_key: xxxx-xxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
{% endif %}
