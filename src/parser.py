from pydantic import (
        BaseModel,
        Field,
        ValidationError,
        model_validator)

class EnvVariables(BaseModel):
    width: int = Field(strict=True)
    height: int = Field(strict=True)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(strict=True)
    perfect: int = Field(strict=True)

def parsing(file_name: str):
    results = {
        'WIDTH': None,
        'HEIGHT': None,
        'ENTRY': None,
        'EXIT': None,
        'OUTPUT_FILE': None,
        'PERFECT': None,
    }
    with open(file_name, 'r') as file:
        line: str = file.readline()
        while line:
            if line[0] != "#":
