from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection


# Create your views here.

class Toplist(APIView):
    def get(self, request):
        client = request.query_params.get('client_num', '')
        start = request.query_params.get('start')
        end = request.query_params.get('end')

        conn = get_redis_connection("default")
        rank_list = conn.zrevrange(name="test:rank:list", start=start - 1, end=end - 1, withscores=True)
        print(rank_list)
        data = list()
        for i in range(1, len(rank_list) + 1):
            data.append(
                {
                    "rank": i,
                    "client_mun": rank_list[i - 1][0],
                    "score": int(rank_list[i - 1][1])
                }
            )
        rank = conn.zrevrank(name="test:rank:list", value=client) + 1
        score = int(conn.zscore(name="test:rank:list", value=client))
        data.append({'rank': rank, 'client_num': client, 'score': score})
        return Response({'msg': '成功', 'data': data, 'code': 1})

    def post(self, request):
        client_num = request.data.get('client_num', None)
        score = int(request.data.get('score', ''))
        if score < 1 or score > 9999999 or client_num is None:
            return Response({'status': False, 'msg': '上传失败'}, content_type='application/json')
        conn = get_redis_connection('default')
        conn.zadd(name='test:rank:list', mapping={client_num: score})
        rank = conn.zrevrank(name='test:rank:list', value=client_num) + 1

        return Response({'data': {'client_id': client_num, 'score': score, 'rank': rank}, 'code': 1},
                        content_type='application/json')
