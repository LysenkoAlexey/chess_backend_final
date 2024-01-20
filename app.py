# импорт объекта для создания приложения
from flask import Flask, session

# создание экземпляра объекта приложения
app = Flask(__name__)

import controllers.index
import controllers.about
import controllers.draw
import controllers.judges