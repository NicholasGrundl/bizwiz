import json
from datetime import datetime, timedelta

def generate_mermaid_gantt(json_file):
    with open(json_file, 'r') as file:
        roadmap_data = json.load(file)
    
    title = roadmap_data.get("title", "Gantt Chart")
    sections = roadmap_data.get("sections", {})
    
    mermaid_lines = []
    mermaid_lines.append("gantt")
    mermaid_lines.append(f"    title {title}")
    mermaid_lines.append("    dateFormat  YYYY-MM-DD")
    
    for section, tasks in sections.items():
        mermaid_lines.append(f"\n    section {section.capitalize()}")
        for task in tasks:
            title = task.get("title", "")
            start_date = task.get("start_date", "")
            duration = task.get("duration", "")
            mermaid_lines.append(f"    {title} : {start_date}, {duration}")
    
    return "\n".join(mermaid_lines)

# # Generate the Gantt chart syntax from the JSON file
# mermaid_gantt = generate_mermaid_gantt('/mnt/data/roadmap.json')
# mermaid_gantt
