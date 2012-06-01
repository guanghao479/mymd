# coding: utf-8

from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import simplejson as json

def home(request):
    """
    View for pins index data. AJAX only.

    """
    result = {}
    if not request.is_ajax():
        return Http404

    pins = [
        {'img':'images/254312710177581204_gtTzVsms_b.jpg',
         'description':'I love squirrels. Especially with my parent.',
         'likes':11,
         'comments':23,
        },
        {
         'title':'我的照料日记',
         'description':'我是家中的长女，父亲走得早，留下母亲和我们兄妹五人，而如今我们都长大了，各自有自己的家庭，只有我和母亲同住一起，母亲岁数大了，由于父亲的去世，母亲一直忧郁，有一天突然摔跤，就一病不起。经医生抢救，母亲脑梗塞，非常严重，不能行走，只能躺在床上，而语言也受到障碍，口齿不清，每天的吃喝拉撒都得有人照顾。由于长期不动，母亲又患上了便秘，几天不拉屎，小肚子很难受，我就先用开塞露帮她通大便，实在不行，我就用水将它挖出来。母亲总是心里觉得过意不去，留着眼泪，口齿不清的讲“小凤，你苦了，妈不中用了，叫你受苦了。”我听了心里一酸，流着泪说：“当初你将我们兄妹几个抚养大，也是这样照顾我们的，现在是我们子女报答你的时候。”目前我母亲躺在床上已经有八年了，她身上没有一点褥疮，我感动，也很欣慰。 通过这几年的照料，使我懂得，对失智老人的照顾，不但是生理的照顾，更要的是心理上的照顾，平时有空多陪她聊天，讲讲小时候的故事等等，让他们能幸福地度过晚年。',
         'likes':11,
         'comments':23,
        },
        {'img':'images/b1ae730fe39f4eafbd75e5e25870ea32.jpg',
         'description':'母亲在这一家老院非常开心，护士照顾的体贴周道，他们还会给妈妈讲发生在自己身上的趣闻趣事',
         'likes':11,
         'comments':23,
        },
        {
         'description':'@baba_wyt：  来陪奶奶聊天了 ，同样的话她可以说上六遍，我就回答她六遍一点也不烦说那么多变…就怕严重起来都不认识我了 老年痴呆没的治！！！为什么！！！',
         'likes':11,
         'comments':23,
        },
        {
         'title':'老妈如何计量她的幸福',
         'description':'听了老妈给出的幸福分数，我心里喜忧参半。高兴的是，她能给自己的一生打这么高的分，应该还是好的吧，至少她没有觉得一生白过。但她的幸福三条也让我为她感觉到遗憾，因为在里面看不到亲情、爱情和友情。让她的幸福加分的，是智力（通过他人评价）和事功（参加解放大西南），减分的是关系。想到阿德勒曾说，追求优越感并非克服自卑的正道，消除自卑的唯一健康途径是培养社会情感。（许又新大夫认为，阿德勒使用的德语“gemeinschaftsgefühl”翻译为英语的“social feeling”并不确切。阿德勒的意思指的主要是和周围的人忧乐与共、休戚相关的情感。）而老妈，其实走的是前一条路，这也许是她虽然给自己打出了高分，但在日常生活中却很少表现出快乐的原因吧',
         'likes':11,
         'comments':23,
        },
        {'img':'images/e05f38e6e888424a90d0579b6bae9b1f.jpg',
         'description':'I love squirrels. Especially with my parent.',
         'likes':11,
         'comments':23,
        },
    ]
    result = { "success":True, "pins":pins, }

    return HttpResponse(json.dumps(result), content_type="application/json")