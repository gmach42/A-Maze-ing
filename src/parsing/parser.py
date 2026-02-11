from pydantic import (
        BaseModel,
        Field,
        StrictBool,
        ValidationError,
        field_validator)
from .errors import (
    FormatError,
    MissingKey,
    ConfigError,
    TooManyVar
    )


class EnvVariables(BaseModel):
    width: int = Field(ge=7)
    height: int = Field(ge=7)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: StrictBool
    animation: bool = False
    cell_size: int = 50
    wall_width: int = 10
    speed_animation: str = 'medium'

    @field_validator('entry', 'exit', mode='before')
    @classmethod
    def check_tuple(cls, value: str):
        clean_value: str = value.replace(")", "").replace('(', "").strip()
        values: list = clean_value.split(',')
        if len(values) != 2:
            raise ValueError("Wrong format tuple. Must be"
                             " '(number,number)")
        try:
            val_1: int = int(values[0])
            val_2: int = int(values[1])
            return (val_2, val_1)
        except ValueError:
            raise ValueError("Entry an exit must be integers!")


def parsing(file_name: str) -> EnvVariables:
    results = {
        'width': None,
        'height': None,
        'entry': None,
        'exit': None,
        'output_file': None,
        'perfect': None,
    }
    try:
        with open(file_name, 'r') as file:
            line: str = file.readline()
            while line:
                if line[0] != "#":
                    string_split: list = line.split('=')
                    if len(string_split) == 2:
                        string_split[1] = string_split[1].strip('\n')
                        if string_split[0].lower() in ['perfect', 'animation']:
                            if string_split[1].lower() == 'true':
                                string_split[1] = True
                            elif string_split[1].lower() == 'false':
                                string_split[1] = False
                        results[string_split[0].lower()] =\
                            string_split[1]
                    else:
                        raise FormatError("You need to use <key>=<value>"
                                          " format")
                line = file.readline()
        if len(results) > 10:
            raise TooManyVar("Too much variables in configuration file!")
        for key, value in results.items():
            if not value and key in ["width", "height", "entry", "exit",
                                     "output_file", "perfect", ]:
                raise MissingKey(f"Missing a value for {key} variable!")
    except ConfigError as e:
        print(e)
    try:
        return EnvVariables(**results)
    except ValidationError as e:
        for error in e.errors():
            loc: str = f"{error['loc'][0]}: "
            print(f"{loc}{error['msg']}")
