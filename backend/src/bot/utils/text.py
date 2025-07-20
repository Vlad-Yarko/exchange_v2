from jinja2 import Template


class Text:
    def __init__(self, text):
        self.text = text

    def render(self, **kwargs) -> str:
        return Template(self.text).render(**kwargs)
