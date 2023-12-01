import json,time
from openai import OpenAI

def show_json(obj):
    print(json.loads(obj.model_dump_json()))

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

client = OpenAI()
# Upload the file
file = client.files.create(
    file=open(
        "data/8.md",
        "rb",
    ),
    purpose="assistants",
)
show_json(file)
# Create Assistant
assistant = client.beta.assistants.create(
    name="周报生成器",
    instructions="你是一个周报生成助手，帮我总结md文档中的内容，按每个周一到周五输出总结我这周的工作内容",
    model="gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id],
)

thread = client.beta.threads.create()
show_json(thread)
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="输出八月份的周报",
)
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
show_json(run)

messages = client.beta.threads.messages.list(thread_id=thread.id)

show_json(messages)

