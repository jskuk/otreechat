from otreechat.models import ChatMessage
from django.http import HttpResponse
import csv
import datetime
import vanilla

class Export(vanilla.View):

    url_name = 'otreechat_export'
    url_pattern = '^otreechat_export/$'
    display_name = 'oTree chat export'

    def get(request, *args, **kwargs):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            'Chat messages (accessed {}).csv'.format(
                datetime.date.today().isoformat()
            )
        )

        column_names = [
            'participant__session__code',
            'participant__session_id',
            'participant__id_in_session',
            'participant__code',
            'channel',
            'nickname',
            'body',
            'timestamp',
        ]

        rows = ChatMessage.objects.order_by('timestamp').values_list(*column_names)

        writer = csv.writer(response)
        writer.writerows([column_names])
        writer.writerows(rows)

        return response
