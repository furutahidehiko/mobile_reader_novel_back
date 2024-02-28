from enum import Enum

class BigGenre(Enum):
    UNCLASSIFIED = (0,"未分類")
    ROMANCE = (1, "恋愛")
    FANTASY = (2, "ファンタジー")
    LITERATURE = (3, "文芸")
    SCIFI = (4, "SF")
    OTHER = (99, "その他")
    NON_GENRE = (98, "ノンジャンル")

    @property
    def id(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]
    
    @classmethod
    def get_label_by_id(cls, id):
        for genre in cls:
            if genre.id == id:
                return genre.label
        return None

class Genre(Enum):
    UNCLASSIFIED = (0,"未分類")
    ROMANCE = (1, "恋愛")
    FANTASY = (2, "ファンタジー")
    LITERATURE = (3, "文芸")
    SCIFI = (4, "SF")
    OTHER = (99, "その他")
    NON_GENRE = (98, "ノンジャンル")
    ISEKAI_ROMANCE = (101, "異世界〔恋愛〕")
    REALITY_ROMANCE = (102, "現実世界〔恋愛〕")
    HIGH_FANTASY = (201, "ハイファンタジー〔ファンタジー〕")
    LOW_FANTASY = (202, "ローファンタジー〔ファンタジー〕")
    PURE_LITERATURE = (301, "純文学〔文芸〕")
    HUMAN_DRAMA = (302, "ヒューマンドラマ〔文芸〕")
    HISTORY = (303, "歴史〔文芸〕")
    MYSTERY = (304, "推理〔文芸〕")
    HORROR = (305, "ホラー〔文芸〕")
    ACTION = (306, "アクション〔文芸〕")
    COMEDY = (307, "コメディー〔文芸〕")
    VR_GAME = (401, "VRゲーム〔SF〕")
    SPACE = (402, "宇宙〔SF〕")
    SCI_FI = (403, "空想科学〔SF〕")
    PANIC = (404, "パニック〔SF〕")
    FAIRY_TALE = (9901, "童話〔その他〕")
    POETRY = (9902, "詩〔その他〕")
    ESSAY = (9903, "エッセイ〔その他〕")
    REPLAY = (9904, "リプレイ〔その他〕")
    OTHERS = (9999, "その他〔その他〕")
    NON_GENRE_SPECIFIC = (9801, "ノンジャンル〔ノンジャンル〕")

    @property
    def id(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]
    
    @classmethod
    def get_label_by_id(cls, id):
        for genre in cls:
            if genre.id == id:
                return genre.label
        return None