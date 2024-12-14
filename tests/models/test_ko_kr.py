from embedded_voice_kkutu.models.ko_kr import KoKrSupport


def test_init_law():
    assert KoKrSupport.init_law("력") == "역"
    assert KoKrSupport.init_law("뇨") == "요"
    assert KoKrSupport.init_law("뉴") == "유"
    assert KoKrSupport.init_law("니") == "이"
    assert KoKrSupport.init_law("랴") == "야"
    assert KoKrSupport.init_law("려") == "여"
    assert KoKrSupport.init_law("례") == "예"
    assert KoKrSupport.init_law("료") == "요"
    assert KoKrSupport.init_law("류") == "유"
    assert KoKrSupport.init_law("리") == "이"
    assert KoKrSupport.init_law("라") == "나"
    assert KoKrSupport.init_law("래") == "내"
    assert KoKrSupport.init_law("로") == "노"
    assert KoKrSupport.init_law("뢰") == "뇌"
    assert KoKrSupport.init_law("루") == "누"
    assert KoKrSupport.init_law("르") == "느"
    assert KoKrSupport.init_law("가") == "가"
    assert KoKrSupport.init_law("각") == "각"
    assert KoKrSupport.init_law("간") == "간"
    assert KoKrSupport.init_law("갇") == "갇"
    assert KoKrSupport.init_law("갈") == "갈"
    assert KoKrSupport.init_law("갉") == "갉"
    assert KoKrSupport.init_law("갊") == "갊"
    assert KoKrSupport.init_law("감") == "감"
    assert KoKrSupport.init_law("갑") == "갑"
    assert KoKrSupport.init_law("값") == "값"
    assert KoKrSupport.init_law("갓") == "갓"
    assert KoKrSupport.init_law("갔") == "갔"
    assert KoKrSupport.init_law("강") == "강"
    assert KoKrSupport.init_law("갖") == "갖"
    assert KoKrSupport.init_law("갗") == "갗"
    assert KoKrSupport.init_law("같") == "같"
    assert KoKrSupport.init_law("갚") == "갚"
    assert KoKrSupport.init_law("갛") == "갛"
    assert KoKrSupport.init_law("개") == "개"
    assert KoKrSupport.init_law("객") == "객"
    assert KoKrSupport.init_law("갠") == "갠"
    assert KoKrSupport.init_law("갤") == "갤"
    assert KoKrSupport.init_law("갬") == "갬"
    assert KoKrSupport.init_law("갭") == "갭"
    assert KoKrSupport.init_law("갯") == "갯"
    assert KoKrSupport.init_law("갰") == "갰"
    assert KoKrSupport.init_law("갱") == "갱"
    assert KoKrSupport.init_law("갳") == "갳"


def main():
    test_init_law()


if __name__ == "__main__":
    main()
