from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class CSSGenerator():
    """CSS Generator crew"""

    agents_config = 'config/agents/css_agent.yaml'
    tasks_config = 'config/tasks/css_task.yaml'

    @agent
    def css_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['css_generator'],
            verbose=True
        )

    @task
    def css_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['css_generation_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        ) 