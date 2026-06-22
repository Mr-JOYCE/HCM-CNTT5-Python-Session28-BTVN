from abc import ABC, abstractmethod

class BaseLesson(ABC):
    platform_name = "Rikkei Academy LMS"
    base_completion_points = 10

    def __init__(self, lesson_code, title, duration_minutes=0):
        if not isinstance(lesson_code, str) or not self.validate_lesson_code(lesson_code):
            raise ValueError("Lesson code is not valid. It must start with LMS and be exactly 10 characters.")

        self.lesson_code = lesson_code
        self.title = title
        self.__duration_minutes = 0

        if duration_minutes < 0:
            raise ValueError("Duration must not be negative.")

        if duration_minutes > 0:
            self._set_duration(duration_minutes)

    @property
    def duration_minutes(self):
        return self.__duration_minutes

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        if not isinstance(new_title, str):
            raise TypeError("Lesson title must be a string.")

        normalized_title = " ".join(new_title.strip().split()).upper()
        self.__title = normalized_title

    def _set_duration(self, duration_minutes):
        if duration_minutes <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")

        self.__duration_minutes = duration_minutes

    @abstractmethod
    def calculate_completion_score(self):
        pass

    @abstractmethod
    def update_content(self, new_data):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes + other.duration_minutes

    def __lt__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes < other.duration_minutes

    @staticmethod
    def validate_lesson_code(lesson_code):
        return isinstance(lesson_code, str) and lesson_code.startswith("LMS") and len(lesson_code) == 10

    @classmethod
    def update_base_points(cls, new_points):
        if not isinstance(new_points, (int, float)) or new_points <= 0:
            raise ValueError("Base completion points must be a positive number.")
        cls.base_completion_points = new_points


class VideoLesson(BaseLesson):
    def __init__(self, lesson_code, title, duration_minutes=0, video_quality="1080p", view_count=0):
        self.video_quality = video_quality
        self.view_count = view_count
        super().__init__(lesson_code=lesson_code, title=title, duration_minutes=duration_minutes)

    def calculate_completion_score(self):
        return self.base_completion_points + (self.duration_minutes * 0.5)

    def update_content(self, new_data):
        if not isinstance(new_data, dict):
            raise TypeError("update_content requires a dictionary of update values.")

        if "video_quality" in new_data:
            self.video_quality = new_data["video_quality"]

        if "title" in new_data:
            self.title = new_data["title"]

    def play_video(self):
        self.view_count += 1


class CodingChallenge(BaseLesson):
    def __init__(self, lesson_code, title, duration_minutes=0, number_of_testcases=1, difficulty_multiplier=1.0):
        if number_of_testcases <= 0 or difficulty_multiplier <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")

        self.number_of_testcases = number_of_testcases
        self.difficulty_multiplier = difficulty_multiplier
        super().__init__(lesson_code=lesson_code, title=title, duration_minutes=duration_minutes)

    def calculate_completion_score(self):
        return self.base_completion_points * self.number_of_testcases * self.difficulty_multiplier

    def update_content(self, new_data):
        if not isinstance(new_data, dict):
            raise TypeError("update_content requires a dictionary of update values.")

        if "number_of_testcases" in new_data:
            if not isinstance(new_data["number_of_testcases"], int) or new_data["number_of_testcases"] <= 0:
                raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
            self.number_of_testcases = new_data["number_of_testcases"]

        if "difficulty_multiplier" in new_data:
            if not isinstance(new_data["difficulty_multiplier"], (int, float)) or new_data["difficulty_multiplier"] <= 0:
                raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")
            self.difficulty_multiplier = new_data["difficulty_multiplier"]


class HybridAssessment(VideoLesson, CodingChallenge):
    def __init__(
        self,
        lesson_code,
        title,
        duration_minutes=0,
        video_quality="1080p",
        view_count=0,
        number_of_testcases=1,
        difficulty_multiplier=1.0,
    ):
        if number_of_testcases <= 0 or difficulty_multiplier <= 0:
            raise ValueError("Thời lượng bài học và thông số kiểm thử không được nhỏ hơn hoặc bằng 0")

        self.number_of_testcases = number_of_testcases
        self.difficulty_multiplier = difficulty_multiplier
        VideoLesson.__init__(
            self,
            lesson_code=lesson_code,
            title=title,
            duration_minutes=duration_minutes,
            video_quality=video_quality,
            view_count=view_count,
        )

    def calculate_completion_score(self):
        video_score = self.base_completion_points + (self.duration_minutes * 0.5)
        coding_score = self.base_completion_points * self.number_of_testcases * self.difficulty_multiplier
        return video_score + coding_score

    def update_content(self, new_data):
        VideoLesson.update_content(self, new_data)
        CodingChallenge.update_content(self, new_data)


class AWSS3StorageService:
    def upload_lesson(self, lesson):
        print("[Hệ thống AWS S3]: Đang khởi tạo luồng băng thông kết nối tới LMS...")
        print(f"Hệ thống lưu trữ đám mây đã upload toàn bộ tài nguyên của bài học {lesson.lesson_code} lên cụm máy chủ an toàn.")


class GoogleCloudStorageService:
    def upload_lesson(self, lesson):
        print("[Hệ thống Google Cloud]: Kết nối tới Google Cloud Storage thành công...")
        print(f"Hệ thống lưu trữ đám mây đã upload toàn bộ tài nguyên của bài học {lesson.lesson_code} lên cụm máy chủ an toàn.")


def sync_to_cloud(cloud_service, lesson):
    try:
        cloud_service.upload_lesson(lesson)
        print("Xác thực dịch vụ bằng Duck Typing thành công!")
    except AttributeError:
        print("Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa ký kết chứng chỉ API liên thông")


def get_positive_int(prompt_text):
    while True:
        try:
            value = int(input(prompt_text).strip())
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")
            continue

        if value <= 0:
            print("Giá trị phải lớn hơn 0.")
            continue

        return value


def get_positive_float(prompt_text):
    while True:
        try:
            value = float(input(prompt_text).strip())
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")
            continue

        if value <= 0:
            print("Giá trị phải lớn hơn 0.")
            continue

        return value


def select_other_lesson(lessons, current_lesson):
    available = [lesson for lesson in lessons if lesson is not current_lesson]
    if not available:
        print("Không có bài học khác để so sánh hoặc gộp thời lượng.")
        return None

    print("Danh sách bài học hiện có:")
    for lesson in available:
        print(f"- {lesson.lesson_code}: {lesson.title} ({lesson.duration_minutes} phút)")

    selected_code = input("Nhập mã bài học đối ứng: ").strip()
    for lesson in available:
        if lesson.lesson_code == selected_code:
            return lesson

    print("Không tìm thấy bài học với mã đã nhập.")
    return None


def display_current_lesson(current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được chọn hoặc tạo.")
        return

    print("--- THÔNG TIN BÀI HỌC HIỆN TẠI ---")
    print(f"Loại bài học: {type(current_lesson).__name__}")
    print(f"Nền tảng: {current_lesson.platform_name}")
    print(f"Mã bài học: {current_lesson.lesson_code}")
    print(f"Tiêu đề bài học: {current_lesson.title}")
    print(f"Thời lượng bài học: {current_lesson.duration_minutes} phút")

    if isinstance(current_lesson, VideoLesson):
        print(f"Chất lượng video: {current_lesson.video_quality}")
        print(f"Số lượt xem: {current_lesson.view_count}")

    if isinstance(current_lesson, CodingChallenge):
        print(f"Số lượng testcase lập trình: {current_lesson.number_of_testcases} bài")
        print(f"Hệ số độ khó: {current_lesson.difficulty_multiplier}")

    mro_list = [cls.__name__ for cls in type(current_lesson).__mro__]
    print("MRO (Method Resolution Order):", " -> ".join(mro_list))


def create_lesson():
    print("--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---")
    print("1. Video Lesson (Bài học Video Lý Thuyết)")
    print("2. Coding Challenge (Bài tập Thực Hành Code)")
    print("3. Hybrid Assessment (Bài Kiểm Tra Tổng Hợp)")

    choice = input("Chọn loại bài học (1-3): ").strip()
    if choice not in {"1", "2", "3"}:
        print("Lựa chọn không hợp lệ.")
        return None

    lesson_code = input("Nhập mã bài học 10 ký tự: ").strip()
    if not BaseLesson.validate_lesson_code(lesson_code):
        print("Mã bài học không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng LMS.")
        return None

    title = input("Nhập tiêu đề bài học: ").strip()
    duration = 0
    while True:
        try:
            duration_input = input("Nhập thời lượng bài học (phút), có thể để 0 nếu chưa xác định: ").strip()
            duration = float(duration_input)
            if duration < 0:
                print("Thời lượng không được nhỏ hơn 0.")
                continue
            break
        except ValueError:
            print("Vui lòng nhập giá trị số hợp lệ.")

    try:
        if choice == "1":
            quality = input("Nhập độ phân giải video (ví dụ: 1080p): ").strip() or "1080p"
            lesson = VideoLesson(
                lesson_code=lesson_code,
                title=title,
                duration_minutes=duration,
                video_quality=quality,
            )
            print("Khởi tạo bài học Video thành công!")
        elif choice == "2":
            testcases = get_positive_int("Nhập số lượng testcase kiểm thử: ")
            difficulty = get_positive_float("Nhập hệ số độ khó (ví dụ: 1.5): ")
            lesson = CodingChallenge(
                lesson_code=lesson_code,
                title=title,
                duration_minutes=duration,
                number_of_testcases=testcases,
                difficulty_multiplier=difficulty,
            )
            print("Khởi tạo bài học Coding Challenge thành công!")
        else:
            quality = input("Nhập độ phân giải video cho Hybrid (ví dụ: 1080p): ").strip() or "1080p"
            testcases = get_positive_int("Nhập số lượng testcase kiểm thử: ")
            difficulty = get_positive_float("Nhập hệ số độ khó (ví dụ: 1.5): ")
            lesson = HybridAssessment(
                lesson_code=lesson_code,
                title=title,
                duration_minutes=duration,
                video_quality=quality,
                number_of_testcases=testcases,
                difficulty_multiplier=difficulty,
            )
            print("Khởi tạo bài học Hybrid Assessment thành công!")

        print(f"Tiêu đề bài học: {lesson.title}")
        return lesson
    except (ValueError, TypeError) as error:
        print(f"Lỗi khi khởi tạo bài học: {error}")
        return None


def update_current_lesson(current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được chọn hoặc tạo.")
        return

    print("--- CẬP NHẬT NỘI DUNG & THỜI LƯỢNG ---")
    print("1. Giả lập học viên tăng lượt xem video (Chỉ dành cho Video/Hybrid)")
    print("2. Cập nhật thông số bài học (Thời lượng, testcase...)")
    action = input("Chọn tác vụ (1-2): ").strip()

    if action == "1":
        if isinstance(current_lesson, VideoLesson):
            current_lesson.play_video()
            print("Ghi nhận thành công! Học viên đã xem video bài học.")
            print(f"Tổng số lượt xem hiện tại: {current_lesson.view_count} lượt.")
        else:
            print("Tác vụ này chỉ áp dụng với VideoLesson hoặc HybridAssessment.")
        return

    if action != "2":
        print("Lựa chọn không hợp lệ.")
        return

    try:
        update_duration = input("Bạn có muốn cập nhật thời lượng bài học không? (y/n): ").strip().lower() == "y"
        if update_duration:
            new_duration = get_positive_float("Nhập thời lượng mới (phút): ")
            current_lesson._set_duration(new_duration)
            print(f"Thời lượng bài học đã được cập nhật thành {current_lesson.duration_minutes} phút.")

        updates = {}
        if isinstance(current_lesson, VideoLesson):
            quality = input("Nhập độ phân giải video mới (để trống nếu không đổi): ").strip()
            if quality:
                updates["video_quality"] = quality
            title = input("Nhập tiêu đề bài học mới (để trống nếu không đổi): ").strip()
            if title:
                updates["title"] = title

        if isinstance(current_lesson, CodingChallenge):
            testcases = input("Nhập số lượng testcase kiểm thử mới bổ sung (để trống nếu không đổi): ").strip()
            if testcases:
                updates["number_of_testcases"] = int(testcases)
            difficulty = input("Nhập hệ số độ khó mới (để trống nếu không đổi): ").strip()
            if difficulty:
                updates["difficulty_multiplier"] = float(difficulty)

        if updates:
            current_lesson.update_content(updates)
            print("Cập nhật thông số thành công!")
            if isinstance(current_lesson, CodingChallenge):
                print(f"Số lượng testcase hiện tại trên hệ thống: {current_lesson.number_of_testcases} testcases.")
            if isinstance(current_lesson, VideoLesson):
                print(f"Chất lượng video hiện tại: {current_lesson.video_quality}")
        elif not update_duration:
            print("Không có thông tin nào để cập nhật.")
    except (ValueError, TypeError) as error:
        print(error)


def show_completion_score(current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được chọn hoặc tạo.")
        return

    print("--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH ---")
    print(f"Bài học: {current_lesson.title} (Loại: {type(current_lesson).__name__})")
    print(f"Điểm cơ sở hệ thống: {current_lesson.base_completion_points} XP")
    print(f"Thời lượng tích lũy: {current_lesson.duration_minutes} phút")

    if isinstance(current_lesson, CodingChallenge):
        print(f"Số lượng testcase cấu hình: {current_lesson.number_of_testcases} bài")

    print(f"Tổng điểm kinh nghiệm (XP) nhận được khi hoàn thành: {current_lesson.calculate_completion_score()} XP")


def sync_lesson(current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được chọn hoặc tạo.")
        return

    print("--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---")
    print("1. Đồng bộ lên máy chủ AWS S3 Storage")
    print("2. Đồng bộ lên máy chủ Google Cloud Storage")
    choice = input("Chọn dịch vụ lưu trữ (1-2): ").strip()

    service = None
    if choice == "1":
        service = AWSS3StorageService()
    elif choice == "2":
        service = GoogleCloudStorageService()
    else:
        print("Lựa chọn dịch vụ không hợp lệ.")
        return

    sync_to_cloud(service, current_lesson)


def compare_and_sum_lessons(lessons, current_lesson):
    if current_lesson is None:
        print("Chưa có bài học nào được chọn hoặc tạo.")
        return

    other = select_other_lesson(lessons, current_lesson)
    if other is None:
        return

    print("--- ĐỒNG BỘ & SO SÁNH THỜI LƯỢNG (OPERATOR OVERLOADING) ---")
    print(f"Bài học hiện tại (A): {current_lesson.title} (Thời lượng: {current_lesson.duration_minutes} phút)")
    print(f"Bài học đối ứng (B): {other.lesson_code} ({other.title} - Thời lượng: {other.duration_minutes} phút)")

    comparison = current_lesson < other
    if comparison is NotImplemented:
        print("Không thể so sánh hai đối tượng không phải bài học.")
    elif comparison:
        print("[Kết quả So sánh (__lt__)]: Thời lượng bài học A NGẮN HƠN thời lượng bài học B.")
    else:
        print("[Kết quả So sánh (__lt__)]: Thời lượng bài học A KHÔNG NGẮN HƠN thời lượng bài học B.")

    total_duration = current_lesson + other
    if total_duration is NotImplemented:
        print("Không thể gộp thời lượng với đối tượng không phải bài học.")
    else:
        print(f"[Kết quả Tổng hợp (__add__)]: Tổng thời lượng học tập của cả 2 bài học là: {total_duration} phút.")


def main():
    lessons = []
    current_lesson = None

    while True:
        print("===== RIKKEI ACADEMY LMS SIMULATOR PRO =====")
        print("1. Khởi tạo bài học mới (Chọn loại bài học nội dung)")
        print("2. Xem thông tin bài học & Kiểm tra thứ tự kế thừa (MRO)")
        print("3. Cập nhật thời lượng & Nội dung bài học (Tính đa hình)")
        print("4. Xem chi tiết điểm thưởng hoàn thành bài học")
        print("5. Kiểm tra gộp thời lượng & So sánh độ dài bài học (Overloading)")
        print("6. Đồng bộ bài giảng lên Nền tảng Đám mây (Duck Typing)")
        print("7. Thoát chương trình")
        print("============================================")

        choice = input("Chọn chức năng (1-7): ").strip()
        print()

        if choice == "1":
            lesson = create_lesson()
            if lesson is not None:
                lessons.append(lesson)
                current_lesson = lesson
        elif choice == "2":
            display_current_lesson(current_lesson)
        elif choice == "3":
            update_current_lesson(current_lesson)
        elif choice == "4":
            show_completion_score(current_lesson)
        elif choice == "5":
            compare_and_sum_lessons(lessons, current_lesson)
        elif choice == "6":
            sync_lesson(current_lesson)
        elif choice == "7":
            print("Cảm ơn bạn đã trải nghiệm hệ thống Quản lý Bài học Rikkei Academy LMS Pro!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 7.")

        print()


if __name__ == "__main__":
    main()
