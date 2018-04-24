from django.core.files.storage import FileSystemStorage
from fdfs_client.client import Fdfs_client


class FdfsStorage(FileSystemStorage):
    """当用户通过django管理后台上传文件时,
        django会调用此方法来保存用户上传的文件,
        我们可以重写此方法， 把文件上传到FastDFS服务器"""

    def _save(self, name, content):
        #继承父类的存储方式
        # path = super()._save(name,content)

        #启动fdfs客户端
        client = Fdfs_client('utils/fdfs/client.conf')

        try:
            datas = content.read()
            """{'Remote file_id': 'group1/M00/00/00/wKiwgVrepgaACzcSAAA2pLUeB60274.jpg',
                     'Group name': 'group1',
                     'Local file name': './static/image/adv01.jpg', 'Uploaded size': '13.00KB',
                     'Storage IP': '192.168.176.129',
                     'Status': 'Upload successed.'}"""
            dict_data = client.upload_by_buffer(datas)  # type:dict
            status = dict_data.get('Status')
            if status != 'Upload successed.':
                raise Exception("上传文件到FastDFS失败, Status不正确.")
            path = dict_data.get('Remote file_id')
        except Exception as e:
            raise e
        return path

    def url(self, name):
        '''返回完整的存储的地址'''
        path = super().url(name)
        return "http://127.0.0.1:8888/" + path
