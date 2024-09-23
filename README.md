# Building a Geo Chat Application with FastHTML

## Step 1: Setting Up the Project

First, we need to set up our FastHTML application. Create a new Python file called `index.py` and start with the following code:

```python
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
```

This code sets up our FastHTML application and includes necessary CSS and JavaScript resources including Pico CSS for styling, a custom `style.css` file, and Plotly for generating interactivate maps. The `fast_app()` function initializes our app and provides a routing decorator `rt`.

## Step 2: Creating the Navigation

Next, let's create a function to generate our navigation bar:

```python
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
```

This function creates a navigation bar with links to the home page and the Geo Chat page. It uses FastHTML's HTML-like syntax to define the structure where HTML tags are represented as Python objects, making it easy to create complex layouts.

## Step 3: Setting Up the Chat Data Structure

We'll use a simple list to store our chat messages:

```python
chat = [
    {"role": "user", "message": "Bonjour, où est né Martin Luther King ?"},
    {
        "role": "bot",
        "message": "Martin Luther King est né à Atlanta, en Géorgie.",
        "lat": 33.7490,
        "lon": -84.3880,
    },
]
```

## Step 4: Creating HTML from Chat Messages

Now, let's create a function to convert our chat messages into FastHTML components:

```python
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
```

## Step 5: Creating the Home Page

Let's create a simple home page:

```python
@rt("/")
def get():
    return (
        Main(
            get_navigation("/"),
            P("Hello world"),
            cls="container",
        ),
    )
```

This route returns a main container with our navigation and a simple greeting.

## Step 6: Creating the Geo Chat Page

Now, let's create the main Geo Chat page:

```python
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
```

This route creates the chat interface, including the chat history and a form for sending new messages. Note the use of HTMX attributes (`hx_post`, `hx_target`, `hx_swap`) for handling form submission without page reloads.

## Step 7: Handling Chat Messages

Let's create a route to handle new chat messages:

```python
@rt("/geo-chat")
def post(message: str):
    if len(message) > 5:
        chat.append({"role": "user", "message": message})
        chat.append(localisation.get_answer(message))

    return (Div(*messages_to_fh(chat), id="chatbox"),)
```

This route adds the user's message to the chat, gets a response from our localization service, and returns the updated chat history.

## Step 8: Creating the Localization Service

In a separate file called `localisation.py`, let's create our localization service:

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

anthropic_model = "claude-3-5-sonnet-20240620"

class LocalisationAnswer(BaseModel):
    answer: str = Field(description="The answer to the question.")
    lat: float = Field(description="The latitude of the location.")
    lon: float = Field(description="The longitude of the location.")

parser = PydanticOutputParser(pydantic_object=LocalisationAnswer)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an helpful assistant for geography questions.\n{format_instructions}\n"),
    ("human", "{question}"),
])

llm = ChatAnthropic(model=anthropic_model)
chain = prompt | llm | parser

def get_answer(question):
    localisation = chain.invoke(
        {"question": question, "format_instructions": parser.get_format_instructions()}
    )
    return {
        "role": "bot",
        "message": localisation.answer,
        "lat": localisation.lat,
        "lon": localisation.lon,
    }
```

This service uses LangChain and Anthropic's Claude model to generate responses to geography questions, including latitude and longitude information.

## Step 9: Creating the Map Generation Function

In another file called `map.py`, let's create a function to generate maps:

```python
from fasthtml.common import *
from uuid import uuid4
import json

def get_map_with_marker(lat, lon):
    data = [
        {
            "type": "scattermap",
            "lat": [lat],
            "lon": [lon],
            "mode": "markers",
            "marker": {
                "size": 20,
                "color": "#EE4823",
            },
            "text": ["Location"],
        }
    ]

    layout = {
        "autosize": True,
        "hovermode": "closest",
        "margin": {"r": 0, "t": 0, "b": 0, "l": 0},
        "map": {
            "center": {
                "lat": lat,
                "lon": lon,
            },
            "bearing": 0,
            "zoom": 2,
            "pitch": 0,
        },
    }

    id_div = str(uuid4()).replace("-", "_")
    return Div(
        Div(id=id_div, cls="map"),
        Script(f"Plotly.newPlot('{id_div}', {json.dumps(data)}, {json.dumps(layout)})"),
    )
```

This function generates both the map data and the Plotly JavaScript code to render the map with a marker at the specified latitude and longitude.
The map is rendered as a `Div` element with a unique ID, and the Plotly code is included as a `Script` element.

## Step 10: Running the Application

Finally, add this line at the end of your `index.py` file to run the application:

```python
serve(port=5001)
```

This starts the FastHTML server on port 5001.

## Conclusion

We've now built a fairly simple Geo Chat application using FastHTML. This application demonstrates several key features of FastHTML:

1. Easy setup and configuration of the application.
2. Declarative HTML-like syntax for creating web pages.
3. Simple routing with the `@rt` decorator.
4. Integration with HTMX for dynamic updates without full page reloads.
5. Easy integration of javascript libraries like Plotly.
6. Easy customization of styles.

To run the application, simply execute the `index.py` file. Users can then navigate to `http://localhost:5001`.