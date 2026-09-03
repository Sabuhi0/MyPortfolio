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
    from urllib import error as urllib_error
    from urllib import request as urllib_request

    token = app.config.get("TELEGRAM_BOT_TOKEN")
    chat_id = app.config.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        # A missing variable used to look exactly like a working form, so name the
        # half that is not configured.
        missing = [name for name, value in (("TELEGRAM_BOT_TOKEN", token),
                                            ("TELEGRAM_CHAT_ID", chat_id)) if not value]
        app.logger.warning("Telegram notification skipped: %s not set", " and ".join(missing))
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
    try:
        with urllib_request.urlopen(req, timeout=10) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib_error.HTTPError as error:
        # Telegram puts the real cause in the body: 401 for a wrong token, and
        # "chat not found" until the bot has been messaged from that chat once.
        app.logger.warning("Telegram rejected the message (HTTP %s): %s",
                           error.code, error.read().decode("utf-8", "replace"))
        return False

    if not body.get("ok"):
        app.logger.warning("Telegram returned an error: %s", body)
        return False
    return True


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
