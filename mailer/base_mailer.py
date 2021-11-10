import smtplib
from typing import Dict, List, Optional, Union
from pydantic import (BaseModel, Field, validator)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback as tb

import jinja2


class BaseMailer(BaseModel):
    host: str
    user: Optional[str]
    password: Optional[str]
    port: int = Field(..., gt=1000)


class Connection:

    def __init__(self, mailer_args: BaseMailer) -> None:
        self.mailer: BaseMailer = mailer_args

    def _connect(self) -> smtplib.SMTP:
        self.server = smtplib.SMTP(
            host=self.mailer.host,
            port=self.mailer.port,
        )

        self.server.login(user=self.mailer.user, password=self.mailer.password)
        return self.server
    def disconnect (self) -> None:

        self.server.quit()


class EngineTemplate:
    def __init__(self, searchpath="./mail_templates") -> None:

        template_loader = jinja2.FileSystemLoader(
            searchpath=searchpath)

        self.env = jinja2.Environment(loader=template_loader)

    def render(self, template: str, template_args: Dict[str, str]) -> str:

        loaded_template = self.env.get_template(name=template)
        rendered_template = loaded_template.render(template_args)

        return rendered_template


class MailerServer:

    def __init__(
        self,
        server_connection: Connection,
        template_engine: EngineTemplate
    ) -> None:
        self.connection: Connection = server_connection
        self.template_engine: EngineTemplate = template_engine

    def send_mail(self,
                  template: str,
                  template_args: Dict[str, str],
                  from_addr: str,
                  to_addr: Union[str, List[str]],
                  subject: str
                  ) -> None:

        rendered = self.template_engine.render(
            template=template,
            template_args=template_args
        )

        msg = MIMEMultipart("alternative")

        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject

        mail_message = MIMEText(rendered, "text")
        msg.attach(mail_message)
        try:

            self.connection.server.sendmail(
                from_addr=from_addr,
                to_addrs=to_addr,
                msg=msg.as_string(),
            )

        except Exception as ex:
            tb.print_exc()

            print(ex.args)
            raise ex

    def __enter__(self):
        self.connection._connect()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        print("CERRANDO")
        self.connection.disconnect()
