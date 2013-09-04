#GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
_log = logging.getLogger(__name__)

from mediagoblin.media_types import MediaManagerBase
from mediagoblin.media_types.blog.models import Blog, BlogPostData

from mediagoblin.tools import pluginapi

PLUGIN_DIR = os.path.dirname(__file__)
MEDIA_TYPE = 'mediagoblin.media_types.blogpost'

def setup_plugin():
    config = pluginapi.get_config(MEDIA_TYPE)
    _log.info("setting up blog media type plugin.")
    
    routes = [  
        #blog_create
        ('mediagoblin.media_types.blog.create',                         
        '/u/<string:user>/b/create/',
        'mediagoblin.media_types.blog.views:blog_edit'
        ), 
         #blog_edit        
        ('mediagoblin.media_types.blog.edit',                          
        '/u/<string:user>/b/<string:blog_slug>/edit/',          
        'mediagoblin.media_types.blog.views:blog_edit'
        ),
        #blog post create
        ('mediagoblin.media_types.blog.blogpost.create',                
        '/u/<string:user>/b/<string:blog_slug>/p/create/',
        'mediagoblin.media_types.blog.views:blogpost_create'
        ),
        #blog post edit
        ('mediagoblin.media_types.blog.blogpost.edit',                  
        '/u/<string:user>/b/<string:blog_slug>/p/<string:blog_post_slug>/edit/',
        'mediagoblin.media_types.blog.views:blogpost_edit'
        ),
        #blog admin dashboard
        ('mediagoblin.media_types.blog.blog-dashboard',
        '/u/<string:user>/b/<string:blog_slug>/blog_dashboard/',
        'mediagoblin.media_types.blog.views:blog_dashboard'
        ),
        #blog post listing view
        ('mediagoblin.media_types.blog.blog_post_listing',
        '/u/<string:user>/b/<string:blog_slug>/',
        'mediagoblin.media_types.blog.views:blog_post_listing'
        ),
        #blog post draft view
        ('mediagoblin.media_types.blog.blogpost_draft_view', 
        '/u/<string:user>/b/<string:blog_slug>/p/<string:blog_post_slug>/draft/',
        'mediagoblin.media_types.blog.views:draft_view')
        ]
            
            
    pluginapi.register_routes(routes)
    pluginapi.register_template_path(os.path.join(PLUGIN_DIR, 'templates'))

    # Register the links to a user's blog
    pluginapi.register_template_hooks({
            "user_profile": "mediagoblin/blog/url_to_blog.html"
            })
    
    
class BlogPostMediaManager(MediaManagerBase):
    human_readable = "Blog Post"
    display_template = "mediagoblin/media_displays/blogpost.html"
    default_thumb = "images/media_thumbs/blogpost.jpg"
    
    def get_blog_by_blogpost(self):
        blog_post_data = BlogPostData.query.filter_by(media_entry=self.entry.id).first()
        blog = Blog.query.filter_by(id=blog_post_data.blog).first()
        return blog
        
def get_media_type_and_manager():

        return MEDIA_TYPE, BlogPostMediaManager

def add_to_user_home_context(context):
    blog = context['request'].db.Blog.query.filter_by(author=context['user'].id).first()
    if blog:
        context['blog'] = blog
    else:
        context['blog'] = None
    return context

hooks = {
    'setup': setup_plugin,
    'get_media_type_and_manager': get_media_type_and_manager,
    ('media_manager', MEDIA_TYPE): lambda: BlogPostMediaManager,
    # Inject blog context on user profile page
    ("mediagoblin.user_pages.user_home",
     "mediagoblin/user_pages/user.html"): add_to_user_home_context

}


    
    
    
