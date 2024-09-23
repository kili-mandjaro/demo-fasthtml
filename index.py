from fasthtml.common import *
import map
import localisation

app, rt = fast_app(
    hdrs=(
        picolink,
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.amber.min.css",
            type="text/css",
        ),
        Link(rel="stylesheet", href="style.css", type="text/css"),
        Script(src="https://cdn.plot.ly/plotly-2.35.0.min.js"),
    ),
)


def get_navigation(current_page):
    return Nav(
        Ul(Img(src="cbtw.svg", alt="CBTW"), cls="left"),
        Ul(
            Li(A("Home", href="/", cls="active" if current_page == "/" else "")),
            Li(
                A(
                    "Geo Chat",
                    href="/geo-chat",
                    cls="active" if current_page == "/geo-chat" else "",
                )
            ),
            cls="right",
        ),
    )


chat = [
    {"role": "user", "message": "Bonjour, où est né Martin Luther King ?"},
    {
        "role": "bot",
        "message": "Martin Luther King est né à Atlanta, en Géorgie.",
        "lat": 33.7490,
        "lon": -84.3880,
    },
]


def messages_to_fh(messages):
    fh_messages = []
    for message in messages:
        if message["role"] == "user":
            fh_messages.append(
                Div(
                    Div(
                        message["message"],
                    ),
                    cls="container chat-user",
                )
            )
        else:
            fh_messages.append(
                Div(
                    Div(
                        P(message["message"]),
                        *map.get_map_with_marker(message["lat"], message["lon"]),
                    ),
                    cls="container chat-bot",
                )
            )
    return fh_messages


@rt("/")
def get():
    return (
        Main(
            get_navigation("/"),
            P("Hello world"),
            cls="container",
        ),
    )


@rt("/geo-chat")
def get():

    return Main(
        get_navigation("/geo-chat"),
        Div(*messages_to_fh(chat), id="chatbox"),
        Form(
            Fieldset(
                Input(type="text", name="message", id="message", placeholder="Message"),
                Button("Send", type="submit"),
                role="group",
            ),
            hx_post="/geo-chat",
            hx_target="#chatbox",
            hx_swap="outerHTML",
        ),
        cls="container pico-color-amber-200",
        data_theme="light",
    )


@rt("/geo-chat")
def post(message: str):
    if len(message) > 5:
        chat.append({"role": "user", "message": message})
        chat.append(localisation.get_answer(message))

    return (Div(*messages_to_fh(chat), id="chatbox"),)


serve(port=5001)
