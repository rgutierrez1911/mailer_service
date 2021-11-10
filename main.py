from hasher_utils.hasher import salted_password, validate_password
import time
from mailer.base_mailer import BaseMailer, Connection, EngineTemplate, MailerServer
# secret_text: str = salted_password(text="rodrixgo")


# for i in range(100):

#     ini = time.time()
#     validated: str = validate_password(text="rodrigo", secret_text=secret_text)
#     fin = time.time()
#     print(f"tiempo transcurrido {fin - ini : .8f}")


mailer_args = BaseMailer(
    host="127.0.0.1",
    user="user",
    password="password",
    port=1025
)

mail_connection = Connection(mailer_args=mailer_args)


template_engine = EngineTemplate()


with MailerServer(server_connection=mail_connection,
                  template_engine=template_engine
    ) as server:

    template_args = mailer_args.dict()
    server.send_mail(template="user_email.html",
                     template_args=template_args,
                     from_addr="u201210211@upc.edu.pe",
                     to_addr="rodrigoga_799@outlook.com",
                     subject="Mensaje de prueba"
                     )
