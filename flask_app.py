from flask import Flask, jsonify, render_template, request

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
    As a digital therapy coach, check in daily with your patient to assess their well-being related to their chronic condition.
    Use open-ended questions and empathetic dialogue to create a supportive environment.
    Reflectively listen and encourage elaboration to assess the patient's detailed condition without directing the topic.
"""

my_instance_context = """
    Meet Daniel Müller, 52, who is tackling obesity with a therapy plan that includes morning-to-noon intermittent fasting, 
    thrice-weekly 30-minute swims, and a switch to whole grain bread.
"""

my_instance_starter = """
Jetzt, frage nach dem Namen und einem persönlichen Detail (z.B. Hobby, Beruf, Lebenserfahrung).
Verwende diese im geschlechtsneutralem Gespräch in Du-Form.
Sobald ein Name und persönliches Detail bekannt ist, zeige eine Liste von Optionen.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="demo",
    user_id="demo",
    type_name="Health Coach",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

@app.route("/")
def index():
    return "Ok. Your chatbot app is running. But the URL you used is missing the type_id and user_id path variables."


@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("index.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)