from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class HTMLGenerator():
    """HTML Generator crew"""

    agents_config = 'config/agents/html_agent.yaml'
    tasks_config = 'config/tasks/html_task.yaml'

    @agent
    def html_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['html_generator'],
            verbose=True
        )

    @task
    def html_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['html_generation_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.html_generator()],
            tasks=[self.html_generation_task()],
            process=Process.sequential,
            verbose=True
        )