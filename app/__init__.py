import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from .momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
app.jinja_env.globals['momentjs'] = momentjs

# Necessary to get administration error emails sent?!??!!
# http://stackoverflow.com/questions/30770981/logging-handlers-smtphandler-raises-smtplib-smtpauthenticationerror
# http://stackoverflow.com/questions/8616617/how-to-make-smtphandler-not-block
# http://mynthon.net/howto/-/python/python%20-%20logging.SMTPHandler-how-to-use-gmail-smtp-server.txt
def emit(self, record):
    """
    Overwrite the logging.handlers.SMTPHandler.emit function with SMTP_SSL.
    Emit a record.
    Format the record and send it to the specified addressees.
    """
    try:
        import smtplib
        from email.utils import formatdate
        port = self.mailport
        if not port:
            port = smtplib.SMTP_PORT
        smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self._timeout)
        msg = self.format(record)
        msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (self.fromaddr, ", ".join(self.toaddrs), self.getSubject(record), formatdate(), msg)
        if self.username:
            smtp.ehlo()
            smtp.login(self.username, self.password)
        smtp.sendmail(self.fromaddr, self.toaddrs, msg)
        smtp.quit()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        self.handleError(record)

#Email errors

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    logging.handlers.SMTPHandler.emit = emit # apply above fix
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), ADMINS[0], 
    							ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    
#File logging
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')
    
from app import views, models