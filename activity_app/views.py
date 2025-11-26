from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_POST

def index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, activity, action, schedular FROM activity_table")
        rows = cursor.fetchall()

    # Convert tuple result to dictionary list
    records = [
        {"id": r[0], "activity": r[1], "action": r[2], "schedular": r[3]}
        for r in rows
    ]

    return render(request, 'activity_app/index.html', {"records": records})


@require_POST
def do_action(request):
    activity_name = request.POST.get("activity")

    return JsonResponse({
        "status": "success",
        "message": f"Received action for: {activity_name}"
    })
import subprocess
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def do_action1(request):
    activity_name = request.POST.get("activity")

    
    playbook_path = "/home/ansible/playbooks/run_task.yml"

    
    cmd = [
        "ansible-playbook",
        playbook_path,
        "-e", f"activity={activity_name}"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        return JsonResponse({
            "status": "success",
            "activity": activity_name,
            "stdout": result.stdout,
            "stderr": result.stderr if result.stderr else "",
            "message": f"Ansible executed for {activity_name}"
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
