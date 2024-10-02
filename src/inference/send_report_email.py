receiver = "todo: get_this_from_config_file"


def send_report_email(subject, content):
    print(
        f"Email sent to {receiver} with subject: {subject} \
        and content: {content}"
    )
