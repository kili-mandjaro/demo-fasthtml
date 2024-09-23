# FastHTML vs. Streamlit

1. Greater flexibility and control:
FastHTML is built on top of Starlette, a lightweight ASGI framework. This allows developers to have more fine-grained control over the application structure, routing, and HTTP interactions. Streamlit, while easy to use, has a more opinionated and constrained approach that can limit flexibility for complex applications.

2. Better performance for web applications:
FastHTML is designed as a web framework, leveraging HTMX for efficient partial page updates. This can result in faster, more responsive applications compared to Streamlit's full page reloads for many interactions.

3. More natural web development paradigm:
FastHTML allows developers to work with HTML-like syntax directly in Python, making it easier for web developers to transfer their existing skills. Streamlit's approach is more widget-based and may feel less natural for complex web layouts.

4. Seamless integration with modern web technologies:
The example shows easy integration with libraries like Plotly for mapping and HTMX for dynamic updates. This allows developers to leverage a wide range of web technologies and JavaScript libraries more easily than in Streamlit.

5. Better support for complex routing and API design:
FastHTML inherits Starlette's powerful routing capabilities, making it easier to create complex application structures with multiple pages and API endpoints. Streamlit's routing is more limited and less suited for complex multi-page applications.

6. More control over the frontend:
While Streamlit abstracts away much of the frontend, FastHTML allows developers to have precise control over HTML, CSS, and JavaScript. This is crucial for creating highly customized and branded user interfaces.

7. Built-in support for authentication and sessions:
The example demonstrates built-in support for user sessions and authentication, which is more challenging to implement in Streamlit.

8. Better suited for production-ready applications:
FastHTML's architecture is closer to traditional web applications, making it easier to transition from a PoC to a production-ready application. Streamlit is primarily designed for data science prototyping and may require significant rework for production use.

11. Better support for asynchronous operations:
FastHTML leverages Python's async capabilities, allowing for more efficient handling of I/O-bound operations, which is particularly useful for complex applications dealing with multiple data sources or APIs.

While Streamlit excels in quickly prototyping data science applications with minimal code, FastHTML provides a more robust, flexible, and web-native approach that is better suited for building complex, personalized, and production-ready web applications. It offers a better balance between ease of use and the power needed for more sophisticated PoCs that may evolve into full-fledged applications.

# FastHTML vs. FastAPI

FastHTML and FastAPI share several similarities in their approach to building web applications, particularly for developers familiar with Python. Here's how FastHTML is like FastAPI for web-based applications:

1. Python-based frameworks:
Both FastHTML and FastAPI are Python-based frameworks designed to simplify and speed up web application development.

2. Built on Starlette:
Both frameworks are built on top of Starlette, a lightweight ASGI framework. This provides a solid foundation for high-performance asynchronous code.

3. Type hinting and data validation:
Both frameworks leverage Python's type hinting system. In FastAPI, this is used for automatic request parsing and validation. FastHTML similarly uses type annotations for form data parsing, as seen in the example:

```python
@rt("/geo-chat")
def post(message: str):
    # ...
```

4. Decorator-based routing:
Both frameworks use decorators for routing. In FastAPI, you might see `@app.get("/")`, while in FastHTML it's `@rt("/")`. This makes defining endpoints intuitive and similar to FastAPI:

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

7. Support for asynchronous programming:
Both frameworks support asynchronous programming out of the box, allowing for efficient handling of concurrent requests.

8. Easy integration with Pydantic:
Both frameworks work well with Pydantic for data modeling and validation. 

9. WebSocket support:
Both frameworks provide built-in support for WebSockets, allowing real-time bidirectional communication.

10. Middleware support:
Both FastAPI and FastHTML allow the use of middleware for processing requests and responses. In FastHTML, this is seen with the `Beforeware` class.

11. Static file serving:
Both frameworks provide easy ways to serve static files, which is crucial for web applications.

The key difference is that while FastAPI is primarily designed for building APIs, FastHTML is more focused on building full-stack web applications with integrated frontend capabilities. FastHTML provides tools for generating HTML directly from Python code, which is not a focus of FastAPI. FastHTML can be seen as an extension of the FastAPI philosophy into the realm of full-stack web development.

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