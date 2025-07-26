from fastapi import APIRouter
from app.schema.models import Links
from ..utils.email_utlis import EmailUtils, Portfolio
from app.schema.models import email_response

router = APIRouter()

emailutl = EmailUtils()
portfolio = Portfolio()
portfolio.load_portfolio()


@router.post("/link", response_model=email_response,response_model_exclude_unset=True)
def coldemail(request: Links):
    pagedata = emailutl.urldata(request.url)
    text = emailutl.cleantext(pagedata)
    job_details = emailutl.jobdetails(text)
    emails = []
    for job in job_details:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = emailutl.write_mail(job, links)
                emails.append(email)
    return {"emails": [email]}

    
