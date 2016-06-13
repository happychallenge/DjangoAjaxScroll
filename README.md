장고/파이선를 배우기 시작한지 이제 5개월….

거의 15년만에 하는 프로그램이 재미있고 생활에 활력을 준다.

그동안 많은 사람들에게 도움을 받으면서 배웠는데, 이제부터는 다른 사람들에게 도움이 되는 사람이 되고자 한다.

이번 글은 Django에서 jQuery 를 이용한 무한 스크롤(Facebook 이나 다른 사이트에서 많은 구현)을 공유해 본다.

우선 models.py 를 구현한다.

    class Post(models.Model):
    “””docstring for Post”””
    “”” Post “””
        title = models.CharField(max_length=30)
        content = models.TextField()
        read = models.IntegerField(default=0)
        likes = models.IntegerField(default=0)
        updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
        created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

views.py 에 다음과 같이 두개의 view function을 구현한다.

    def post_list(request):
        post_list = Post.objects.all().order_by(‘-created_date’)
        paginator = Paginator(post_list, 10)
        page = request.POST.get(‘page’)

        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)

        context = {‘post_list’:post_list}
        return render(request, ‘post/post_list.html’, context)

    def post_list_ajax(request): #Ajax 로 호출하는 함수
        post_list = Post.objects.all().order_by(‘-created_date’)
        paginator = Paginator(post_list, 10)
        page = request.POST.get(‘page’)

        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)

        context = {‘post_list’:post_list}
        return render(request, ‘post/post_list_ajax.html’, context) #Ajax 로 호출하는 템플릿은 _ajax로 표시.

post/post_list.html 은 다음과 같이 구현을 한다.

    {% extends “base.html” %}

    {% comment %} Title {% endcomment %}
    {% block title %} POST’s List {% endblock title %}

    {% comment %} Search {% endcomment %}
    {% block search %}
    <div class=”col-sm-10″>
    {% csrf_token %}
    <input type=”text” class=”form-control input-md” id=”searchID” placeholder=”검색어를 입력하시요.” autofocus>
    </div>
    <div class=”col-sm-2″>
    <button type=”button” class=”btn btn-primary btn-md btn-block”>Search
    </div>
    <br />
    <url id=”search_result_ajax”>
    </url>
    <br />

    <script type=”text/javascript”>
        var token = $(‘input[name=”csrfmiddlewaretoken”]’).prop(‘value’);
        $(function() {
            $(‘#searchID’).keyup(function(){
            $.ajax( {
                type : ‘POST’,
                url: “{% url ‘post_search’ %}”,
                data: {
                ‘search_text’: $(‘#searchID’).val(),
                ‘csrfmiddlewaretoken’: token
            },
            success: searchSuccess,
            dataType: ‘html’
            });
            });
        });

        function searchSuccess(data, textStatus, jqXHR) {
            $(‘#search_result_ajax’).html(data);
        }
    </script>
    {% endblock search %}

    {% comment %} Main {% endcomment %}
    {% block main %}
    <div class=”row”>

    {% if post_list %}

    {% for post in post_list %}
    <div class=”col-xs-12 col-sm-6″>
    <h2>{{ post.title }}</h2>
    <p>{{ post.content | truncatewords:”50″ }}

    <p><a class=”btn btn-default” href=”{% url ‘post_detail’ post.id %}” role=”button”>View details »</a></p>
    </div>
    {% endfor %}

    {% else %}
    <p>No Data</p>
    {% endif %}

    </div>
    <div id=”post_list_ajax”></div> **Ajax 결과물을 추가할 곳
    <input id=”page” type=”hidden” value=”2″> **페이지 정보를 입력할 곳
    <button id=”callmorepost” type=”button” class=”btn btn-primary btn-block”>More Post</button> **페이지 스크롤 이벤트가 작동하지 않을 경우 클릭함.

    <script>
        //scroll event
        $(‘#callmorepost’).click(function(){
            var page = $(“#page”).val();
            callMorePostAjax(page);
            $(“#page”).val(parseInt(page)+1);
        });

        $(window).scroll(function(){
            var scrollHeight = $(window).scrollTop() + $(window).height();
            var documentHeight = $(document).height();
            
            if (scrollHeight + 300 >= documentHeight){
                var page = $(“#page”).val();
                callMorePostAjax(page);
                $(“#page”).val(parseInt(page)+1);
            }
        });

        function callMorePostAjax(page) {
            $.ajax( {
            type : ‘POST’,
            url: “{% url ‘post_list_ajax’ %}”,
            data: {
            ‘page’: page,
            ‘csrfmiddlewaretoken’: token
            },
            success: addMorePostAjax,
            dataType: ‘html’
            });
        }

        function addMorePostAjax(data, textStatus, jqXHR) {
            $(‘#post_list_ajax’).append(data);
        } 
    </script>
    {% endblock main %}

마지막으로 무한 스크롤을 구현할 때
if ($(window).scrollTop() == $(document).height() – $(window).height()){
를 사용하지 않았는데, 크롬 등에서 해당 Event 를 정확히 인식하지 못하는 경우가 있기 때문입니다.

그래서
var scrollHeight = $(window).scrollTop() + $(window).height();
var documentHeight = $(document).height();
if (scrollHeight + 300 >= documentHeight){

를 사용하였습니다.

그리고 페이지는 <input id=”page” type=”hidden” value=”2″> 에 값을 넣어 두고, 다음 페이지를 읽어볼 때 해당 값을 증가 시켜 주었습니다.
var page = $(“#page”).val();
callMorePostAjax(page);
$(“#page”).val(parseInt(page)+1);

post/post_list_ajax.html 은 다음과 같이 구현을 한다.
그냥 post/post_list.html 에서 Data Query 를 뿌려 주는 부분을 저장하면 된다.

    {% if post_list %}

    {% for post in post_list %}
    <div class=”col-xs-12 col-sm-6″>
    <h2>{{ post.title }}</h2>
    <p>{{ post.content | truncatewords:”50″ }}</p>
    <p><a class=”btn btn-default” href=”{% url ‘post_detail’ post.id %}” role=”button”>View details »</a></p>
    </div>
    {% endfor %}

    {% else %}
    <p>No Data</p>
    {% endif %}

urls.py 가 빠져서 추가를 합니다.

    urlpatterns = [
        url(r'^list/$', views.post_list, name='post_list'),
        url(r'^create/$', views.post_create, name='post_create'),
        url(r'^detail/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
        url(r'^update/(?P<post_id>[0-9]+)/$', views.post_update, name='post_update'),
        url(r'^delete/(?P<post_id>[0-9]+)/$', views.post_delete, name='post_delete'),
        url(r'^search/$', views.post_search, name='post_search'),                       #Ajax 
        url(r'^likes/(?P<post_id>[0-9]+)/$', views.post_likes, name='post_likes'),      #Ajax 
        url(r'^list/ajax/$', views.post_list_ajax, name='post_list_ajax'),              #Ajax 
    ]

해당 소스는 https://github.com/happychallenge/DjangoAjaxScroll 에서 다운로드가 가능합니다.
감사합니다.
