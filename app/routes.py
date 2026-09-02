#app/routes

from flask import render_template,redirect,url_for,request
from admin.routes import blog,feedback,skills,project,contact
from run import app



@app.route("/")
def portfolio():
    from models import Blogs
    from models import Profile
    from models import Skills
    from models import Projects
    from models import Feedbacks
    from models import Contact
    prof= Profile.query.get(1)
    blogs = Blogs.query.all()
    skills = Skills.query.all()
    projects = Projects.query.all()
    feedbacks = Feedbacks.query.all()
    messages = Contact.query.all()
    return render_template("app/index.html",blogs=blogs,prof=prof,skills=skills,projects=projects,feedbacks=feedbacks,messages=messages)


def notify_telegram(contact_name, contact_email, contact_message):
    """Send the contact message to Telegram. Returns True when it was delivered."""
    import json
    from urllib import request as urllib_request

    token = app.config.get("TELEGRAM_BOT_TOKEN")
    chat_id = app.config.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False

    text = "\n".join([
        "New message from your portfolio",
        "",
        "Name: %s" % contact_name,
        "Email: %s" % contact_email,
        "",
        contact_message,
    ])
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    }).encode("utf-8")

    req = urllib_request.Request(
        "https://api.telegram.org/bot%s/sendMessage" % token,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib_request.urlopen(req, timeout=10) as response:
        return response.status == 200


# Public contact form (no login required)
@app.route("/contact", methods=["POST"])
def contact_send():
    from models import Contact
    from run import db

    contact_name = request.form.get("contact_name", "").strip()
    contact_email = request.form.get("contact_email", "").strip()
    contact_message = request.form.get("contact_message", "").strip()

    if not contact_name or not contact_email or not contact_message:
        return redirect("/#contact")

    message = Contact(
        contact_name=contact_name,
        contact_email=contact_email,
        contact_message=contact_message,
    )
    db.session.add(message)
    db.session.commit()

    # The message is already saved, so a failing notification must not break the page.
    try:
        notify_telegram(contact_name, contact_email, contact_message)
    except Exception as error:
        app.logger.warning("notify_telegram failed: %s", error)

    return redirect("/#contact")
