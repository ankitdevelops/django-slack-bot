import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from pprint import pprint
import slacky
from .task import slack_message_task


@csrf_exempt
@require_POST
def slack_events_endpoint(request):
    json_data = {}
    try:
        json_data = json.loads(request.body.decode("utf-8"))
    except:
        pass

    data_type = json_data.get("type")
    allowed_data_type = ["url_verification", "event_callback"]
    if data_type not in allowed_data_type:
        return HttpResponse("not allowed", status=400)
    if data_type == "url_verification":
        challenge = json_data.get("challenge")
        if challenge is None:
            return HttpResponse("not allowed", status=400)
        return HttpResponse(challenge, status=200)
    elif data_type == "event_callback":
        event = json_data.get("event") or {}
        try:
            msg_text = event["blocks"][0]["elements"][0]["elements"][1]["text"]
        except:
            msg_text = event.get("text")
        user_id = event.get("user")
        channel_id = event.get("channel")
        msg_ts = event.get("ts")
        thread_ts = event.get("thread_ts") or msg_ts
        # r = slacky.send_message(
        #     msg_text,
        #     channel_id=channel_id,
        #     user_id=user_id,
        #     thread_ts=thread_ts,
        # )
        # slack_message_task.delay(
        #     msg_text,
        #     channel_id=channel_id,
        #     user_id=user_id,
        #     thread_ts=thread_ts,
        # )
        slack_message_task.apply_async(
            kwargs={
                "message": f"{msg_text}",
                "channel_id": channel_id,
                "user_id": user_id,
                "thread_ts": thread_ts,
            },
            countdown=30,
        )
        return HttpResponse("Success", status=200)
    return HttpResponse("success", status=200)
