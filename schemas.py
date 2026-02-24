from pydantic import BaseModel ,ConfigDict ,Field

class postbase(BaseModel):
    title: str = Field(min_length=1 , max_length=100)
    content: str = Field(min_length=1 )
    author : str = Field(min_length=1 , max_length=50)


class postcreate(postbase):
    pass

class postresponse(postbase):
    model_config = ConfigDict(from_attributes=True)

    id : int
    date_posted: str

