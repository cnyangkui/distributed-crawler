from django.conf.urls import include, url
from django.contrib import admin

from crawlermanage import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'geowind_crawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^crawlermanage/$',views.login, name='login'),
    url(r'^crawlermanage/login/$',views.login, name='login'),
    url(r'^crawlermanage/index/$',views.index, name='index'),
    url(r'^crawlermanage/tasks/$',views.tasks, name='tasks'),
    url(r'^crawlermanage/edittask/$',views.edittask, name='edittask'),
    url(r'^crawlermanage/newsdata/$',views.newsdata, name='newsdata'),
    #url(r'^crawlermanage/newsdetail/$',views.newsdetail, name='newsdetail'),
    url(r'^crawlermanage/ecommercedata/$',views.ecommercedata, name='ecommercedata'),
    url(r'^crawlermanage/layout/$',views.layout, name='layout'),
    url(r'^crawlermanage/taskdetail/$',views.taskdetail, name='taskdetail'),
    url(r'^crawlermanage/testarticles/$',views.testarticles, name='testarticles'),
    url(r'^crawlermanage/testlist/$',views.testlist, name='testlist'),
    url(r'^crawlermanage/extractarticle/$',views.extractarticle, name='extractarticle'),
    url(r'^crawlermanage/processlist/$',views.processlist, name='processlist'),
    url(r'^crawlermanage/machinelist/$', views.machinelist, name='machinelist'),
    url(r'^crawlermanage/deleteip/$', views.deleteip, name='deleteip'),
    url(r'^crawlermanage/addip/$', views.addip, name='addip'),
    url(r'^crawlermanage/charts/$', views.charts, name='charts'),
    url(r'^crawlermanage/testsingle/$', views.testsingle, name='testsingle'),
    url(r'^crawlermanage/introduce/$', views.introduce, name='introduce'),
    url(r'^crawlermanage/ecommercedata/$', views.ecommercedata, name='ecommercedata'),
    url(r'^crawlermanage/blogdata/$', views.blogdata, name='blogdata'),
    #url(r'^crawlermanage/blogdetail/$', views.blogdetail, name='blogdetail'),
    url(r'^crawlermanage/extractsinger/$', views.extractsinger, name='extractsinger'),
    url(r'^crawlermanage/extractmultiple/$', views.extractmultiple, name='extractmultiple'),
    url(r'^crawlermanage/temparticle/$', views.temparticle, name='temparticle'),
    url(r'^crawlermanage/editprocess/$', views.editprocess, name='editprocess'),
    url(r'^crawlermanage/settings/$', views.settings, name='settings'),

    url(r'^crawlermanage/domainautocomplete/$', views.domain_autocomplete, name='domainautocomplete'),
    url(r'^crawlermanage/debug/$', views.debug, name='debug'),
    url(r'^crawlermanage/export/$', views.export, name='export'),


    # url(r'^crawlermanage/$','crawlermanage.views.login'),
    # url(r'^crawlermanage/login/$','crawlermanage.views.login'),
    # url(r'^crawlermanage/index/$','crawlermanage.views.index'),
    # url(r'^crawlermanage/tasks/$','crawlermanage.views.tasks'),
    # url(r'^crawlermanage/taskdata/$','crawlermanage.views.taskdata'),
    # url(r'^crawlermanage/layout/$','crawlermanage.views.layout'),
]
