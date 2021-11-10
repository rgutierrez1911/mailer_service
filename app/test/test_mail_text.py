import smtplib

from mailer.base_mailer import (BaseMailer,
                                Connection,
                                EngineTemplate,
                                MailerServer)

from test.fixtures import (render_engine,
                           mail_server_connection,
                           mail_server,
                           connection_params)

def test_render_engine(render_engine: EngineTemplate):

    template_args = {
        "param1": "param_1",
        "param2": "param_2"
    }
    rendered = render_engine.render(
        template="test.html",
        template_args=template_args
    )
    response_rendered = f"{template_args['param1']}_{template_args['param2']}"

    assert response_rendered == rendered , "ERROR : THE RENDERED FUNCTION FAILED AT EVALUATING EQUALITY"
    return True


def test_connection(connection_params: BaseMailer):

    base_params = connection_params
    conection_mailer = Connection(mailer_args=base_params)

    server = conection_mailer._connect()

    assert type(server) == smtplib.SMTP, "ERROR , CONNECTION TO THE SERVER FAILED"
    conection_mailer.disconnect()

    return True


def test_mail_send(mail_server: MailerServer, ):

    mail_server.connection._connect()

    template_args = {
        "param1": "param_1",
        "param2": "param_2"
    }
    
    from_addr = "rodrigoga_799@outlook.com"
    to_addr = "rgutierrez.arana@gmail.com"
    subject = "test_subject"

    mail_server.send_mail(template="test.html",
                          template_args=template_args,
                          from_addr=from_addr,
                          to_addr=to_addr,
                          subject=subject)
    return True
