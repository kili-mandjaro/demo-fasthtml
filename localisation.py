from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, model_validator
from dotenv import load_dotenv

load_dotenv()

anthropic_model = "claude-3-5-sonnet-20240620"


class LocalisationAnswer(BaseModel):
    answer: str = Field(description="The answer to the question.")
    lat: float = Field(description="The latitude of the location.")
    lon: float = Field(description="The longitude of the location.")


parser = PydanticOutputParser(pydantic_object=LocalisationAnswer)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an helpful assistant for geography questions.\n{format_instructions}\n",
        ),
        ("human", "{question}"),
    ]
)

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
