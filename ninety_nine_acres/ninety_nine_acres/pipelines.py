# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from PIL import Image
from cStringIO import StringIO
import re

class NinetyNineAcresImagesPipeline(ImagesPipeline):

    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict
    """def get_media_requests(self, item, info):
    	for name, img in zip(item['image_names'], item['images']):
        	img['path'] = 'full/' + name + '.jpg'
        print "!!!!\n\n\n\nget_media_requests"
        print item
        print "\n\n\n\n!!!!"
        print info.downloaded
        print info.downloading
        print info.waiting

        image_urls = item['image_urls']
        image_names = item['image_names']
        return [Request(image_urls[i]) for i in range(len(image_urls))]"""

    def item_completed(self, results, item, info):
        print "\n\n\n\n"
        print results
        print "\n\n\n\n\n"
        print info.downloading
        print info.downloaded
        print info.waiting
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths

        for name, img in zip(item['image_names'], item['images']):
        	img['path'] = 'full/' + name + '.jpg'
        return item

    """# this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        print "!!!!\n\n\n\nget_images\n\n\n\n!!!!"
        path = 'full/%s' % request.meta['image_name']
        
        orig_image = Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.min_width, self.min_height))

        image, buf = self.convert_image(orig_image)
        yield path, image, buf

    def image_downloaded(self, response, request, info):
        print "!!!!\n\n\n\nimage_downlaoded\n\n\n\n!!!!"
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            self.store.persist_file(
                path, buf, info,
                meta={'width': width, 'height': height},
                headers={'Content-Type': 'image/jpeg'})
        return checksum

    def file_downloaded(self, response, request, info):
        return self.image_downloaded(response, request, info)"""

    """def file_path(self, request, response=None, info=None):
        print "!!!!\n\n\n\nInside file_path\n\n\n\n!!!!"
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        #image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        #return 'full/%s.jpg' % (image_guid)
        print request.meta['image_name']
        image_guid = request.meta['image_name']
        print request.meta['image_name']
        return 'full/%s.jpg' % request.meta['image_name']"""



class NinetyNineAcresPipeline(object):
    def process_item(self, item, spider):
        return item


