from pydantic import BaseSettings

from app import database


#Class to perform the validations for the environment variable
#while fething the emvironment variables, the return type is always going to be string
class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    #Name of the database under postgres to which we are connected to
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    ACCESSS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"



settings = Settings()