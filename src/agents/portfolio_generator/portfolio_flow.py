from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from src.agents.portfolio_generator.crews.html_generator import HTMLGenerator
from src.agents.portfolio_generator.crews.css_generator import CSSGenerator
from src.agents.portfolio_generator.crews.js_generator import JSGenerator
import os
from pathlib import Path

class PortfolioState(BaseModel):
    website_content: str = ""


class PortfolioFlow(Flow[PortfolioState]):

    def __init__(self, inputs=None):
        super().__init__()
        self.inputs = inputs or {}

    @start()
    def generate_html(self):
        print("Starting HTML generation task")
        html_output = HTMLGenerator().crew().kickoff(inputs=self.inputs)
        self.state.website_content = html_output.raw
        return self.state.website_content

    @listen(generate_html)
    def generate_css(self):
        print("Starting CSS generation task")
        css_output = CSSGenerator().crew().kickoff(inputs={"file_content": self.state.website_content, **self.inputs})
        self.state.website_content = css_output.raw
        return self.state.website_content

    @listen(generate_css)
    def generate_js(self):
        print("Starting JavaScript generation task")
        js_output = JSGenerator().crew().kickoff(inputs={"file_content": self.state.website_content, **self.inputs})
        self.state.website_content = js_output.raw.strip('```html').strip('```').strip()
        return self.state.website_content

    @listen(generate_js)
    def save_output(self):
        print("Saving final output to HTML file")
        
        # Create the path to the website directory
        website_dir = Path('src/templates/website')
        website_file = website_dir / 'website.html'

        # Create directories if they don't exist
        website_dir.mkdir(parents=True, exist_ok=True)

        # Write the file
        with open(website_file, 'w') as f:
            f.write(self.state.website_content)
        return "Output saved successfully"
