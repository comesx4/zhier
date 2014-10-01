# -*- coding: utf-8 -*-

from django.template import Library, Node
from app.models import Post, Tag, Category
register = Library()


class ZhierNode(Node):

    def __init__(self, code):
        self._code = code

    def render(self, context):
        return self._code

def zhier_footer(parser, token):
    last3Posts = Post.objects.all().order_by("-publish_time")[0:3]
    lasPostCode = ''
    for item in last3Posts:
        lasPostCode += "<li><a href=%s.html>%s</a></li>" % (item.link, item.title)
    code = u'''
<footer>
    <div class="container">
        <div class="row">
            <div class="col-lg-3">
                <div class="widget">
                    <h5 class="widgetheading">Get in touch with Me</h5>
                    <address>
                    <strong></strong>
                    <br>
                     Modernbuilding suite V124, AB 01<br>
                     Someplace 16425 Earth </address>
                    <p>
                        <i class="fa fa-phone"></i> (123) 456-7890 - (123) 555-7891 <br>
                        <i class="fa fa-envelope-alt"></i> email@domainname.com
                    </p>
                </div>
            </div>
            <div class="col-lg-3">
                <div class="widget">
                    <h5 class="widgetheading">Pages</h5>
                    <ul class="link-list">
                        <li><a href="#">Press release</a></li>
                        <li><a href="#">Terms and conditions</a></li>
                        <li><a href="#">Privacy policy</a></li>
                        <li><a href="#">Career center</a></li>
                        <li><a href="#">Contact us</a></li>
                    </ul>
                </div>
            </div>
            <div class="col-lg-3">
                <div class="widget">
                    <h5 class="widgetheading">Latest posts</h5>
                    <ul class="link-list">
                        {0:s}
                    </ul>
                </div>
            </div>
            <div class="col-lg-3">
                <div class="widget">
                    <h5 class="widgetheading">Flickr photostream</h5>
                    <div class="flickr_badge"></div>
                    <div class="clear">
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div id="sub-footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-6">
                    <div class="copyright">
                        <p>
                            <span>&copy; <a href="/about">Zhier</a> 2014 All right reserved. </span>
                        </p>
                    </div>
                </div>
                <div class="col-lg-6">
                    <ul class="social-network">
                        <li><a href="#" data-placement="top" title="Facebook"><i class="fa fa-facebook"></i></a></li>
                        <li><a href="#" data-placement="top" title="Twitter"><i class="fa fa-twitter"></i></a></li>
                        <li><a href="#" data-placement="top" title="Linkedin"><i class="fa fa-linkedin"></i></a></li>
                        <li><a href="#" data-placement="top" title="Pinterest"><i class="fa fa-pinterest"></i></a></li>
                        <li><a href="#" data-placement="top" title="Google plus"><i class="fa fa-google-plus"></i></a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</footer>
    '''.format(lasPostCode)
    return ZhierNode(code)

zhier_footer = register.tag(zhier_footer)
