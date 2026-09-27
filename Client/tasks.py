from celery import shared_task



@shared_task
def publish_order(Id,order):
    try:
        visit = order.objects.get(visit_id=Id)
    except order.DoesNotExist:
        return
    if visit.status == "waiting":
        visit.status = "published"
        visit.save()
