import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog
from policy_crawl.common.utils import get_cookie

def parse_detail(html,url):
    alllog.logger.info("湖北省教育厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".TRS_UEDITOR").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".TRS_UEDITOR a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="湖北省教育厅"
    data["url"]=url
    print(data)
    # save(data)

def parse_index(html,cookies):
    doc=pq(html)
    items=doc(".info-list li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://zizhan.mot.gov.cn/st/hebei/tongzhigonggao" + url.replace("./","/")
        try:
            html=get(url,cookies=cookies)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,8):
        print(i)
        if i==0:
            url="http://jyt.hubei.gov.cn/fbjd/xxgkml/zcwj/zcfg/index.shtml"
        else:
            url="http://jyt.hubei.gov.cn/fbjd/xxgkml/zcwj/zcfg/index_"+str(i)+".shtml"
        cookies=get_cookie(url,".info-list")
        html=get(url,cookies=cookies)
        parse_index(html,cookies)




if __name__ == '__main__':
    main()