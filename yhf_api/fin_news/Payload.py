"""Stream payload configuration and utils"""

from enum import Enum
from typing import Optional

class Category(Enum):
    """Valid article stream categories to query"""
    crypto="LISTID:b1f0c990-db7a-11e7-a937-0d92c86f9da1"
    politics="LISTID:4e0c46d6-e0f4-45a4-b8e8-47abe5f382a1"
    latest_news="LISTID:912fa270-3f5c-11e9-aff7-753ecd51b83d"
    yahoo_finance_originals="LISTID:0897608a-7d79-47df-9377-b07bd22b0fde"
    stock_market_news="LISTID:db1d46e0-a969-11e9-bff5-6dfdb80d79cf"
    financials="LISTID:04d9350a-bbd1-4787-95be-740cc5ee8852"
    economic_news="LISTID:7ce2bfb8-c363-4498-930b-b6d86ae4dccf"
    personal_finance="LISTID:98a22a0b-749e-43e1-9407-06b8e60bedf0"

class AdsConfig(dict):
    """Config for including ads in responses"""
    def __init__(self, frequency:int=5, count:int=25, ad_policies:bool=False) -> None:
        """
        Defines Ads part of payload
        
        ## Params
        - frequency: `int`, the number of articles between ads, larger than 1
        - count: `int`, the total number of ads to include in response
        - ad_policies: `bool`, i have no idea what it does, assume some sort of policy for content etc"""
        assert frequency > 1
        super().__init__()
        self.update({
            "ad_polices": ad_policies,
            "contentType": "video/mp4,application/x-shockwave-flash,application/vnd.apple.mpegurl",
            "count": count,
            "enableFlashSale": True,
            "enableGeminiDealsWithoutBackground": True,
            "frequency": frequency,
            "geminiPromotionsEnabled": True,
            "generic_viewability": True,
            "inline_video": True,
            "partial_viewability": True,
            "pu": "finance.yahoo.com",
            "se": 4492794,
            "spaceid": 1183300073,
            "start_index": 1,
            "timeout": 0,
            "type": "STRM,STRM_CONTENT,STRM_VIDEO",
            "useHqImg": True,
            "useResizedImages": True
        })

class UiConfig(dict):
    """Config for the ui component of response"""
    def __init__(self, include_summary:bool=True, max_age_seconds:int=0) -> None:
        """
        UI component of payload,

        ## Params
        - include_summary: `bool`, to include a article summary or not
        - maxage_seconds: `int`, specify the maximum age of articles to return in seconds, 0 return all articles, if none are found matching requirement, articles without creation time are returned
        """
        super().__init__()
        self.update ({
            "comments_offnet": True,
            "link_out_allowed": True,
            "pubtime_maxage": max_age_seconds,
            "relative_links": False,
            "show_comment_count": True,
            "summary": include_summary
        })

class BatchConfig(dict):
    """Config for bach component of response"""
    def __init__(self, size:int=20, pagination:bool=False, total:int=1, timeout:int=1500) -> None:
        """
        Batching configuration
        
        ## Params
        - size: `int`, number of articles to return, between 1 and 160, over 160 is truncated to 160
        - total: `int`
        """
        super().__init__()
        self.update({
            "pagination": pagination, # Does nothing
            "size": size, 
            "timeout": timeout,
            "total": total # Does nothing
        })

class Payload(dict):
    """The payload sent to news endpoint"""
    def __init__(self, category:Category, num_articles:int=20, include_summary:bool=True, max_age_seconds:int=0, ads_config:Optional[AdsConfig]=None, ):
        """
        Create a payload for stream request
        
        ## Params
        - category: `Category`, target category to get articles from
        - num_articles: `int`, number of articles to get from stream, min 1 max 160
        - include_summary: `bool`, to include article summary or not in response
        - max_age_seconds: `int`, maximum age of articles to return in seconds
        """
        super().__init__()
        self.category = category
        batching = BatchConfig(size=num_articles)
        ui = UiConfig(include_summary, max_age_seconds)
        params = {}
        if ads_config is not None:
            params["ads"] = ads_config
        params["ui"] = ui
        params["batches"] = batching
        params["category"] = category.value
        params["useNCP"] = True,
        
        self.update({
            "requests": {
                "g0": {
                    "resource": "StreamService",
                    "operation": "read",
                    "params": params
                }
            }
        })