class KoKrSupport:
    KOR_UNICODE_START = 0xAC00
    KOR_UNICODE_END = 0xD7A3

    def init_law(content: str) -> str:
        if len(content) == 0:
            return
        if len(content) == 1:
            return KoKrSupport.init_law_char(content)
        return KoKrSupport.init_law_char(content[0]) + content[1:]

    def init_law_char(content: str) -> str:
        """
        source: https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/%ED%95%9C%EA%B8%80%20%EB%A7%9E%EC%B6%A4%EB%B2%95/(2017-12,20170328)
        * 한자음 여부는 파악하지 않음
        """
        if len(content) != 1:
            raise ValueError("content must be a single character")

        target = ord(content)
        if (
            target < KoKrSupport.KOR_UNICODE_START
            or target > KoKrSupport.KOR_UNICODE_END
        ):
            return target

        init_law_map = {
            "녀": "여",
            "뇨": "요",
            "뉴": "유",
            "니": "이",
            "랴": "야",
            "려": "여",
            "례": "예",
            "료": "요",
            "류": "유",
            "리": "이",
            "라": "나",
            "래": "내",
            "로": "노",
            "뢰": "뇌",
            "루": "누",
            "르": "느",
        }

        target_first = (target - KoKrSupport.KOR_UNICODE_START) // 588
        target_second = ((target - KoKrSupport.KOR_UNICODE_START) % 588) // 28
        target_third = ((target - KoKrSupport.KOR_UNICODE_START) % 588) % 28

        merged_character = chr(
            KoKrSupport.KOR_UNICODE_START + target_first * 588 + target_second * 28
        )
        if merged_character not in init_law_map:
            return content

        merged_character = chr(ord(init_law_map[merged_character]) + target_third)

        return merged_character


if __name__ == "__main__":
    print(KoKrSupport.init_law_char("력"))
