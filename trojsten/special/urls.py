from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^ksp/32/1/1/', include('trojsten.special.plugin_ksp_32_1_1.urls',
        namespace='plugin_ksp_32_1_1', app_name='plugin_zwarte')),
    url(r'^ksp/32/2/1/', include('trojsten.special.plugin_ksp_32_2_1.urls',
        namespace='plugin_ksp_32_2_1', app_name='plugin_zwarte')),
    url(r'^ksp/32/3/1/', include('trojsten.special.plugin_ksp_32_3_1.urls')),
)
