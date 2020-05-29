import jinja2
import pdfkit
from .models import *
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def post_acc_checklist_pdf(pk):
    template_loader = jinja2.FileSystemLoader(searchpath="/home/wskublewski/Desktop/"
                                                         "PythonCodersLab/ProjektKoncowy/coderslab/brc_db/"
                                                         "templates/brc_db/Checklist")
    print(template_loader)
    template_env = jinja2.Environment(loader=template_loader)
    TEMPLATE_FILE = "post_acceptance_checklist.html"
    template = template_env.get_template(TEMPLATE_FILE)
    post = POSTReview.objects.get(id=pk)
    out_put_text = template.render(cim_number=post.cim_number, maker=post.maker,
                                   open_date=post.cim_number.open_date, funded_amount=post.cim_number.funded_amount,
                                   funded_date=post.cim_number.funded_date,
                                   fees=CHECKLIST_VALUES[(int(post.fees_checked)-1)][1],
                                   letter_sent=CHECKLIST_VALUES[(int(post.letter_sent)-1)][1],
                                   cr_client_restriction=CHECKLIST_VALUES[(int(post.cr_client_restriction)-1)][1],
                                   cr_aa_bg_system=CHECKLIST_VALUES[(int(post.cr_aa_bg_system)-1)][1],
                                   cr_sa=CHECKLIST_VALUES[(int(post.cr_sa)-1)][1],
                                   comment=post.comment,
                                   maser=post.maker,
                                   post_maker_date=post.post_maker_date,
                                   post_checker_date=post.post_checker_date,
                                   post_checker=post.post_checker,
                                   )
    html_file_name = f'post_acceptance_checklist {post.cim_number}.html'
    pdf_file_name = f'post_acceptance_checklist {post.cim_number}.pdf'
    html_file = open(html_file_name,'w')
    html_file.write(out_put_text)
    html_file.close()
    pdfkit.from_file(html_file_name, pdf_file_name)


def send_mail(maker_mail, mail_subject, mail_message):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "wojciech.skublewski@gmail.com"
    receiver_email = maker_mail
    password = input("Type your password and press enter: ")
    message = MIMEMultipart()
    message['Subject'] = mail_subject
    message.attach(MIMEText(mail_message, 'plain'))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


post_acc_checklist_pdf(12)

