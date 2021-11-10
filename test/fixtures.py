import os
from pytest import fixture
from mailer.base_mailer import (BaseMailer,
                                Connection,
                                EngineTemplate,
                                MailerServer)
@fixture
def render_engine()->EngineTemplate:
    render_engine = EngineTemplate()
    return render_engine


@fixture
def mail_server_connection(connection_params: BaseMailer)-> Connection:
    return Connection(mailer_args=connection_params)


@fixture
def mail_server(mail_server_connection: Connection,
                render_engine: EngineTemplate) -> MailerServer:

    mail_server = MailerServer(server_connection=mail_server_connection,
                               template_engine=render_engine)
    return mail_server
@fixture
def connection_params()->BaseMailer:
    base_params = BaseMailer(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        port=int(os.getenv("port"))
    )
    return base_params
