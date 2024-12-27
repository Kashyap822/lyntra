from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class JSGenerator():
    """JavaScript Generator crew"""

    agents_config = 'config/agents/js_agent.yaml'
    tasks_config = 'config/tasks/js_task.yaml'

    @agent
    def javascript_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['javascript_generator'],
            verbose=True
        )

    @task
    def javascript_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['javascript_generation_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        ) 