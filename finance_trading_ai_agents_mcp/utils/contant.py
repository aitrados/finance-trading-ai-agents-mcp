class SystemPromptLanguage:
    en="en"
    de="de"
    fr="fr"
    ja="ja"
    es="es"
    kr="kr"
    ru="ru"
    zh_cn="zh_cn"
    zh_tw="zh_tw"
    @classmethod
    def get_array(cls):
        return [cls.en,cls.de,cls.fr,cls.ja,cls.kr,cls.ru,cls.zh_cn,cls.zh_tw]