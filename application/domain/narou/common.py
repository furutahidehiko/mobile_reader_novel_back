from fake_useragent import UserAgent

class UserAgentManager:
    def __init__(self):
        self.ua = UserAgent()
    
    def get_random_user_headers(self):
        return {'User-Agent': self.ua.random}


class Genre:
    big_genre_dict = {
		1: "恋愛", 2: "ファンタジー", 3: "文芸", 4: "SF", 99: "その他", 98: "ノンジャンル",
	}
    genre_dict = {
				1: "恋愛",
				2: "ファンタジー",
				3: "文芸",
				4: "SF",
				99: "その他",
				98: "ノンジャンル",
				101: "異世界〔恋愛〕",
				102: "現実世界〔恋愛〕",
				201: "ハイファンタジー〔ファンタジー〕",
				202: "ローファンタジー〔ファンタジー〕",
				301: "純文学〔文芸〕",
				302: "ヒューマンドラマ〔文芸〕",
				303: "歴史〔文芸〕",
				304: "推理〔文芸〕",
				305: "ホラー〔文芸〕",
				306: "アクション〔文芸〕",
				307: "コメディー〔文芸〕",
				401: "VRゲーム〔SF〕",
				402: "宇宙〔SF〕",
				403: "空想科学〔SF〕",
				404: "パニック〔SF〕",
				9901: "童話〔その他〕",
				9902: "詩〔その他〕",
				9903: "エッセイ〔その他〕",
				9904: "リプレイ〔その他〕",
				9999: "その他〔その他〕",
				9801: "ノンジャンル〔ノンジャンル〕",
			}
    @classmethod
    def get_big_genre(cls, id):
        return cls.big_genre_dict.get(id, "不明なジャンル")

    @classmethod
    def get_genre(cls, id):
        return cls.genre_dict.get(id, "不明なサブジャンル")