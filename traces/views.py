import folium
from django.shortcuts import render, redirect
from geopy.distance import geodesic
from geopy.geocoders import BaiduV3
from .utils import get_center_coordinates, get_zoom

# Create your views here.
from goods.models import Order
from traces import models
from .form import WayForm
from rtree import index
import time


# def showTrace(request, order_id):
#     order = Order.objects.get(id=order_id)
#     print(order.id)
#     trace = models.Trace.objects.get(order_id=order_id)
#     print(trace.id)
#     l_lat = trace.start_latitude
#     l_lon = trace.start_longitude
#     point_A = (l_lat, l_lon)
#     # initial folium map
#     # m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8,
#     #                tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
#     #                attr='default')
#     # # location marker
#     # folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=order.city,
#     #               icon=folium.Icon(color='purple')).add_to(m)
#
#     d_lat = trace.end_latitude
#     d_lon = trace.end_longitude
#     print("tiqu:", d_lon.to_eng_string())
#     point_B = (d_lat, d_lon)
#
#     distance = round(geodesic(point_A, point_B).km, 2)
#     print(distance)
#     print("zoom_start", get_zoom(distance))
#     print("location", get_center_coordinates(l_lat, l_lon, d_lat, d_lon))
#     print("point_A:", point_A, ",point_B:", point_B)
#     # folium map modification
#     m = folium.Map(width='100%', height='100%', location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon),
#                    zoom_start=get_zoom(distance),
#                    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
#                    attr='default'
#                    )
#
#     # location marker
#     folium.Marker([l_lat, l_lon], tooltip='起点', popup='广州市',
#                   icon=folium.Icon(color='purple', icon='globe')).add_to(m)
#     # destination marker
#     folium.Marker([d_lat, d_lon], tooltip='终点', popup=order.city,
#                   icon=folium.Icon(color='red', icon='play')).add_to(m)
#
#     # draw the line
#     way = models.Way.objects.filter(trace_id=trace.id)
#     point = [point_A]
#     for i in way:
#         point.append((i.latitude, i.longitude))
#     point.append(point_B)
#     print("point:", point)
#     print([point_A, point_B])
#     line = folium.PolyLine(locations=point, weight=5, color='blue')
#     # line = folium.PolyLine(locations=[point_A, point_B], weight=5, color='blue')
#     m.add_child(line)
#     m = m._repr_html_()
#
#     return render(request, 'trace.html', locals())


def traceInfo(request, order_id):
    order_id = order_id
    order = Order.objects.get(id=order_id)
    trace = models.Trace.objects.get(order_id=order_id)
    print("trace.id", trace.id)
    way = models.Way.objects.filter(trace_id=trace.id)
    print("way:", way)
    travel = models.Travel.objects.filter(trace=trace.id)
    print("travel:", travel)
    return render(request, 'trace.html', locals())


def traceSport(request, order_id):
    # 调用数据库
    t0 = time.time()
    order = Order.objects.get(id=order_id)
    print(order.id)
    trace = models.Trace.objects.get(order_id=order_id)
    print(trace.id)
    l_lat = trace.start_latitude
    l_lon = trace.start_longitude
    point_A = {'lng': l_lon.to_eng_string(), 'lat': l_lat.to_eng_string()}
    d_lat = trace.end_latitude
    d_lon = trace.end_longitude
    point_B = {'lng': d_lon.to_eng_string(), 'lat': d_lat.to_eng_string()}
    print("point_A:", point_A, ",point_B:", point_B)
    way = models.Way.objects.filter(trace_id=trace.id)
    point = [point_A]
    for i in way:
        point.append({'lng': i.longitude.to_eng_string(), 'lat': i.latitude.to_eng_string()})
    point.append(point_B)
    print("point:", point)
    t1 = time.time()
    print("处理时间：", t1 - t0)
    return render(request, 'sport.html', locals())


def traceSport1(request, order_id):
    # 调用3DR-tree
    t0 = time.time()
    print(order_id)
    trace = models.Trace.objects.get(order_id=order_id)
    p = index.Property()
    p.dimension = 3
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    idx3d = index.Index('History', properties=p)
    hits = list(idx3d.intersection((0, 0, 416, 120, 90, 420), objects=True))
    points = [item.bbox for item in hits if item.id == trace.id]
    point = []
    for i in points:
        point.append({'lng': i[0], 'lat': i[1]})
    print(point)
    t1 = time.time()
    print("处理时间：", t1 - t0)
    return render(request, 'sport.html', locals())


def updateWay(request, id):

    print(id)
    trace = models.Trace.objects.get(order_id=id)

    print(trace)
    if request.method == "POST":
        way_form = WayForm(request.POST)
        message = "请检查填写的内容！"
        if way_form.is_valid():
            longitude = way_form.cleaned_data['longitude']
            latitude = way_form.cleaned_data['latitude']
            time = way_form.cleaned_data['time']
            # 更新way
            print("time:", time)
            print("type:", type(time))
            pre_ways = models.Way.objects.filter(trace_id=trace).order_by("-w_time")
            point = (latitude, longitude)
            point_A = (trace.end_latitude, trace.end_longitude)  # 终点

            print("point", point)
            print("point_A", point_A)
            print("pre_ways.count():", pre_ways.count())
            if pre_ways.count() == 0:
                distance_to_pre = 0
            else:
                # 计算距离
                pre_way = pre_ways[0]
                point_B = (pre_way.latitude, pre_way.longitude)  # way的上一个点
                distance_to_pre = geodesic(point_B, point)
                print("distance_to_pre", distance_to_pre)
                print("point_B", point_B)

            distance_to_end = geodesic(point_A, point)
            print("distance_to_end", distance_to_end)

            new = models.Way.objects.create()
            new.trace_id = trace
            new.latitude = latitude
            new.longitude = longitude
            new.w_time = time
            new.save()

            if distance_to_end < distance_to_pre:
                print("trace.order_id", trace.order_id)
                order = models.Order.objects.get(id=trace.order_id_id)
                order.status = '2'
                order.save()
                print("order change")
                new_travel = models.Travel.objects.create()
                new_travel.trace_id = trace.id
                new_travel.t_time = time
                addr = order.province + order.city + order.district + " [已到达]"
                new_travel.now_add = addr
                new_travel.save()
                return redirect('/sale/')
            else:
                # 更新travel
                print("更新travel")
                travel = models.Travel.objects.filter(trace_id=trace).order_by("-t_time")[0]
                print(travel.id)
                p = index.Property()
                p.dimension = 2
                p.dat_extension = 'data'
                p.idx_extension = 'index'
                idx = index.Index('2d_city', properties=p)
                print(list(idx.nearest((113.296664, 23.086912), 1, objects="raw")))
                a = idx.nearest((longitude, latitude), 1, objects="coordinates")
                for i in a:
                    print("i.object", i.object)
                    if i.object != travel.now_add:
                        new_travel = models.Travel.objects.create()
                        new_travel.trace_id = trace.id
                        new_travel.t_time = time
                        new_travel.now_add = i.object
                        new_travel.save()
                        print("已更新")
                return redirect('/sale/')
    way_form = WayForm()
    return render(request, 'update.html', locals())

# >>> from rtree import index
# >>> idx = index.Index()
# >>> idx.insert(4321,
# ...            (34.3776829412, 26.7375853734, 49.3776829412,
# ...             41.7375853734),
# ...            obj=42)
#
# >>> hits = list(idx.intersection((0, 0, 60, 60), objects=True))
# >>> [(item.object, item.bbox) for item in hits if item.id == 4321]
# ...
# [(42, [34.37768294..., 26.73758537..., 49.37768294...,
#        41.73758537...])]