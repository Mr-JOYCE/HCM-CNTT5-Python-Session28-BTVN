from __future__ import annotations
from abc import ABC, abstractmethod

class BaseEmployee(ABC):
    company_name = "Rikkei Education"
    base_salary_rate = 3_000_000

    def __init__(self, emp_code: str, full_name: str):
        if not self.validate_employee_code(emp_code):
            raise ValueError(f"Mã nhân viên không hợp lệ: {emp_code}")
        self.emp_code = emp_code
        self.full_name = full_name
        self.__working_hours = 0

    @property
    def working_hours(self):
        return self.__working_hours

    def _add_working_hours(self, hours: float):
        if hours < 0:
            raise ValueError("Thời gian làm việc không hợp lệ")
        self.__working_hours += hours

    @abstractmethod
    def calculate_salary(self):
        pass

    @abstractmethod
    def update_kpi(self, progress):
        pass

    def __add__(self, other: BaseEmployee):
        if not isinstance(other, BaseEmployee):
            return NotImplemented
        return self.working_hours + other.working_hours

    def __lt__(self, other: BaseEmployee):
        if not isinstance(other, BaseEmployee):
            return NotImplemented
        return self.working_hours < other.working_hours

    @staticmethod
    def validate_employee_code(emp_code: str) -> bool:
        return isinstance(emp_code, str) and emp_code.startswith("RIKE") and len(emp_code) == 10

    @classmethod
    def update_base_salary_rate(cls, new_rate: float):
        if new_rate <= 0:
            raise ValueError("new_rate phải là số dương")
        cls.base_salary_rate = new_rate

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.emp_code} {self.full_name} hours={self.working_hours}>"


class Lecturer(BaseEmployee):
    def __init__(self, emp_code: str, full_name: str, teaching_slots: int = 0):
        super().__init__(emp_code, full_name)
        self.teaching_slots = int(teaching_slots)
        self.kpi = None

    def calculate_salary(self):
        return (self.working_hours * self.base_salary_rate) + (self.teaching_slots * 500_000)

    def update_kpi(self, progress):
        self.kpi = progress
        return f"KPI được cập nhật: {progress}"

    def conduct_class(self):
        self.teaching_slots += 1
        self._add_working_hours(2)


class AdmissionStaff(BaseEmployee):
    def __init__(self, emp_code: str, full_name: str, revenue_generated: float = 0.0, kpi_target: float = 100_000_000):
        super().__init__(emp_code, full_name)
        self.revenue_generated = float(revenue_generated)
        self.kpi_target = float(kpi_target)

    def calculate_salary(self):
        return (self.working_hours * self.base_salary_rate) + (self.revenue_generated * 0.05)

    def update_kpi(self, progress):
        try:
            added = float(progress)
        except Exception:
            raise ValueError("Tiến độ phải là một con số thể hiện doanh thu mới.")
        if added < 0:
            raise ValueError("Doanh thu tăng thêm phải không âm.")
        self.revenue_generated += added
        return f"Doanh thu tăng lên bởi {added}, tổng cộng {self.revenue_generated}"


class HybridManager(Lecturer, AdmissionStaff):
    def __init__(self, emp_code: str, full_name: str, teaching_slots: int = 0, revenue_generated: float = 0.0, kpi_target: float = 100_000_000):
        super().__init__(emp_code, full_name, teaching_slots)
        self.revenue_generated = float(revenue_generated)
        self.kpi_target = float(kpi_target)

    def calculate_salary(self):
        base_pay = (self.working_hours * self.base_salary_rate)
        teaching_bonus = (self.teaching_slots * 500_000)
        commission = (self.revenue_generated * 0.05)
        return base_pay + teaching_bonus + commission

    def update_kpi(self, progress):
        if isinstance(progress, dict):
            if 'revenue' in progress:
                self.revenue_generated += float(progress['revenue'])
            if 'teaching' in progress:
                inc = int(progress['teaching'])
                self.teaching_slots += inc
                self._add_working_hours(2 * inc)
            if 'kpi' in progress:
                self.kpi = progress['kpi']
            return f"KPI được cập nhật: {progress}"
        else:
            return AdmissionStaff.update_kpi(self, progress)

class VietcombankCorporateService:
    def __init__(self):
        self.service_name = "VCB Corporate"
    
    def transfer_salary(self, employee: BaseEmployee, amount: float):
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        return f"[{self.service_name}] Đã chuyển {amount:,.0f} VND cho nhân sự {employee.emp_code}"


class TechcombankCorporateService:
    def __init__(self):
        self.service_name = "Techcombank Corporate"
    
    def transfer_salary(self, employee: BaseEmployee, amount: float):
        """Thực hiện chuyển khoản lương"""
        if amount <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        return f"[{self.service_name}] Đã chuyển {amount:,.0f} VND cho nhân sự {employee.emp_code}"


def execute_payroll(payment_service, employee: BaseEmployee, amount: float):
    """
    Duck Typing: Hàm không quan tâm loại payment_service là gì, 
    chỉ cần nó có phương thức transfer_salary()
    """
    try:
        if not hasattr(payment_service, 'transfer_salary'):
            raise AttributeError(
                "Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ hoặc chưa được liên kết liên thông kỹ thuật"
            )
        result = payment_service.transfer_salary(employee, amount)
        return result
    except AttributeError as e:
        raise AttributeError(str(e))

def normalize_name(name: str) -> str:
    """Chuẩn hóa tên: in hoa, xóa khoảng trắng thừa"""
    return ' '.join(name.strip().split()).upper()


def print_menu():
    print("\n===== RIKKEI EDUCATION HR SIMULATOR PRO =====")
    print("1. Tuyển dụng nhân sự mới (Chọn loại hợp đồng nhân sự)")
    print("2. Xem thông tin & Kiểm tra thứ tự kế thừa (MRO)")
    print("3. Ghi nhận công nhật & Cập nhật KPI (Tính đa hình)")
    print("4. Tổng hợp quỹ lương và ngân sách chi trả")
    print("5. Kiểm tra gộp giờ làm việc & So sánh hiệu suất (Overloading)")
    print("6. Giải ngân lương qua Cổng thanh toán đối tác (Duck Typing)")
    print("7. Thoát chương trình")
    print("==============================================")


def function_1_recruit(employees: list, current_employee: list):
    """Chức năng 1: Tuyển dụng nhân sự mới"""
    print("\n--- CHỌN LOẠI NHÂN SỰ KHỞI TẠO ---")
    print("1. Lecturer (Giảng viên chuyên trách)")
    print("2. Admission Staff (Nhân viên Tuyển sinh)")
    print("3. Hybrid Manager (Quản lý kiêm Giảng dạy)")
    
    try:
        choice = input("Chọn loại nhân sự (1-3): ").strip()
        
        if choice not in ['1', '2', '3']:
            print("Lựa chọn không hợp lệ!")
            return
        
        emp_code = input("Nhập mã nhân sự 10 ký tự: ").strip()
        
        # Kiểm tra mã nhân sự hợp lệ
        if not BaseEmployee.validate_employee_code(emp_code):
            print("Mã nhân sự không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng RIKE.")
            return
        
        # Kiểm tra mã nhân sự đã tồn tại
        if any(e.emp_code == emp_code for e in employees):
            print("Mã nhân sự đã tồn tại trong hệ thống!")
            return
        
        full_name = input("Nhập họ và tên: ").strip()
        if not full_name:
            print("Họ tên không được để trống!")
            return
        
        full_name = normalize_name(full_name)
        
        if choice == '1':
            new_emp = Lecturer(emp_code, full_name)
            type_name = "Giảng viên"
        elif choice == '2':
            new_emp = AdmissionStaff(emp_code, full_name)
            type_name = "Nhân viên Tuyển sinh"
        else:
            new_emp = HybridManager(emp_code, full_name)
            type_name = "Quản lý"
        
        employees.append(new_emp)
        current_employee[0] = new_emp
        print(f"Tuyển dụng {type_name} thành công!")
        print(f"Tên nhân sự: {full_name}")
    
    except ValueError as e:
        print(f"Lỗi: {e}")
    except TypeError as e:
        print(f"Lỗi kiểu dữ liệu: {e}")


def function_2_view_info(current_employee: list):
    """Chức năng 2: Xem thông tin & Kiểm tra MRO"""
    if not current_employee[0]:
        print("Lỗi: Chưa chọn nhân sự nào. Vui lòng tuyển dụng trước.")
        return
    
    emp = current_employee[0]
    emp_type = type(emp).__name__
    
    print("\n--- THÔNG TIN NHÂN SỰ HIỆN TẠI ---")
    print(f"Loại nhân sự: {emp_type}")
    print(f"Tổ chức: {emp.company_name}")
    print(f"Mã nhân sự: {emp.emp_code}")
    print(f"Họ và tên: {emp.full_name}")
    print(f"Số giờ làm việc: {emp.working_hours} giờ")
    
    if isinstance(emp, Lecturer):
        print(f"Số ca đã dạy: {emp.teaching_slots} ca")
    
    if isinstance(emp, AdmissionStaff):
        print(f"Doanh số mang về: {emp.revenue_generated:,.0f} VND")

def function_3_update_kpi(current_employee: list):
    """Chức năng 3: Ghi nhận công nhật & Cập nhật KPI (Tính đa hình)"""
    if not current_employee[0]:
        print("Lỗi: Chưa chọn nhân sự nào.")
        return
    
    emp = current_employee[0]
    emp_type = type(emp).__name__
    
    print("\n--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---")
    
    if isinstance(emp, Lecturer):
        print("1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)")
    print("2. Cập nhật tiến độ KPI / Doanh số")
    
    try:
        choice = input("Chọn tác vụ (1-2): ").strip()
        
        if choice == '1':
            if not isinstance(emp, Lecturer):
                print("Lỗi: Tác vụ này chỉ dành cho Giảng viên hoặc Hybrid Manager!")
                return
            
            emp.conduct_class()
            print("Ghi nhận thành công! Thầy/Cô đã hoàn thành thêm 1 ca dạy.")
            print(f"Số ca dạy hiện tại: {emp.teaching_slots} ca.")
            print(f"Số giờ làm việc tích lũy: +2 giờ.")
        
        elif choice == '2':
            if isinstance(emp, HybridManager):
                print("Nhập doanh số hợp đồng mới mang về (hoặc 0 nếu không có):")
                revenue_input = input("Doanh số (VND): ").strip()
                try:
                    revenue = float(revenue_input) if revenue_input else 0
                    if revenue < 0:
                        print("Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0")
                        return
                    result = emp.update_kpi({'revenue': revenue})
                    print(f"Cập nhật KPI thành công!")
                    print(f"Doanh số tích lũy mới: {emp.revenue_generated:,.0f} VND.")
                except ValueError:
                    print("Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0")
            
            elif isinstance(emp, AdmissionStaff):
                revenue_input = input("Nhập giá trị doanh số hợp đồng mới mang về: ").strip()
                try:
                    revenue = float(revenue_input)
                    if revenue <= 0:
                        print("Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0")
                        return
                    result = emp.update_kpi(revenue)
                    print("Cập nhật KPI thành công!")
                    print(f"Doanh số tích lũy mới: {emp.revenue_generated:,.0f} VND.")
                except ValueError:
                    print("Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0")
            
            elif isinstance(emp, Lecturer):
                kpi_input = input("Nhập tỷ lệ hoàn thành khung chương trình (% hoặc mô tả): ").strip()
                result = emp.update_kpi(kpi_input)
                print(f"Cập nhật KPI thành công! {result}")
        else:
            print("Lựa chọn không hợp lệ!")
    
    except Exception as e:
        print(f"Lỗi: {e}")


def function_4_salary_summary(current_employee: list):
    """Chức năng 4: Tổng hợp quỹ lương và ngân sách chi trả"""
    if not current_employee[0]:
        print("Lỗi: Chưa chọn nhân sự nào.")
        return
    
    emp = current_employee[0]
    emp_type = type(emp).__name__
    
    try:
        total_salary = emp.calculate_salary()
        
        print("\n--- CHI TIẾT QUỸ LƯƠNG NHÂN SỰ ---")
        print(f"Nhân sự: {emp.full_name} (Loại: {emp_type})")
        print(f"Mức lương cơ sở hệ thống: {BaseEmployee.base_salary_rate:,.0f} VND")
        print(f"Số giờ làm việc tích lũy: {emp.working_hours} giờ")
        
        base_pay = emp.working_hours * BaseEmployee.base_salary_rate
        print(f"Lương cứng tính theo giờ: {base_pay:,.0f} VND")
        
        if isinstance(emp, HybridManager):
            teaching_bonus = emp.teaching_slots * 500_000
            commission = emp.revenue_generated * 0.05
            print(f"Phụ cấp ca dạy + Hoa hồng tuyển sinh tích hợp: {teaching_bonus + commission:,.0f} VND")
        elif isinstance(emp, Lecturer):
            teaching_bonus = emp.teaching_slots * 500_000
            print(f"Phụ cấp ca dạy: {teaching_bonus:,.0f} VND")
        elif isinstance(emp, AdmissionStaff):
            commission = emp.revenue_generated * 0.05
            print(f"Hoa hồng tuyển sinh: {commission:,.0f} VND")
        
        print(f"Tổng lương thực nhận tháng này: {total_salary:,.0f} VND")
    
    except Exception as e:
        print(f"Lỗi tính toán lương: {e}")


def function_5_working_hours_comparison(employees: list, current_employee: list):
    """Chức năng 5: Kiểm tra gộp giờ làm việc & So sánh hiệu suất (Overloading)"""
    if not current_employee[0]:
        print("Lỗi: Chưa chọn nhân sự nào.")
        return
    
    if len(employees) < 2:
        print("Lỗi: Cần ít nhất 2 nhân sự để thực hiện so sánh.")
        return
    
    emp_a = current_employee[0]
    
    print("\n--- ĐỒNG BỘ & SO SÁNH GIỜ CÔNG (OPERATOR OVERLOADING) ---")
    print(f"Nhân sự hiện tại (A): {emp_a.full_name} (Giờ công: {emp_a.working_hours} giờ)")
    print("\nDanh sách nhân sự khác:")
    
    other_employees = [e for e in employees if e.emp_code != emp_a.emp_code]
    for i, e in enumerate(other_employees, 1):
        print(f"  {i}. {e.emp_code} ({e.full_name} - Giờ công: {e.working_hours} giờ)")
    
    try:
        idx = int(input("Chọn nhân sự đối ứng (B) từ danh sách (số thứ tự): ").strip()) - 1
        
        if idx < 0 or idx >= len(other_employees):
            print("Lựa chọn không hợp lệ!")
            return
        
        emp_b = other_employees[idx]
        
        # So sánh __lt__
        is_less = emp_a < emp_b
        comparison = "ÍT HƠN" if is_less else "KHÔNG ÍT HƠN"
        print(f"\n[Kết quả So sánh (__lt__)]: Giờ công cống hiến của nhân sự A {comparison} nhân sự B.")
        
        # Tổng hợp __add__
        total_hours = emp_a + emp_b
        print(f"[Kết quả Tổng hợp (__add__)]: Tổng số giờ làm việc của cả 2 nhân sự là: {total_hours} giờ.")
    
    except ValueError:
        print("Lỗi: Vui lòng nhập một số hợp lệ!")
    except TypeError as e:
        print(f"Lỗi kiểu dữ liệu: {e}")


def function_6_payroll_disbursement(current_employee: list):
    """Chức năng 6: Giải ngân lương qua Cổng thanh toán đối tác (Duck Typing)"""
    if not current_employee[0]:
        print("Lỗi: Chưa chọn nhân sự nào.")
        return
    
    emp = current_employee[0]
    
    print("\n--- CHI TRẢ LƯƠNG QUA CỔNG ĐỐI TÁC TRUNG GIAN ---")
    print("1. Chi trả qua tài khoản Doanh nghiệp Vietcombank")
    print("2. Chi trả qua tài khoản Doanh nghiệp Techcombank")
    
    try:
        bank_choice = input("Chọn cổng ngân hàng (1-2): ").strip()
        
        if bank_choice == '1':
            payment_service = VietcombankCorporateService()
            bank_name = "Vietcombank"
        elif bank_choice == '2':
            payment_service = TechcombankCorporateService()
            bank_name = "Techcombank"
        else:
            print("Lựa chọn không hợp lệ!")
            return
        
        amount_input = input("Nhập số tiền giải ngân: ").strip()
        try:
            amount = float(amount_input)
        except ValueError:
            print("Số tiền phải là một con số hợp lệ!")
            return
        
        if amount <= 0:
            print("Số tiền phải lớn hơn 0!")
            return
        
        print(f"[Hệ thống {bank_name} Corporate]: Đang kết nối tới cổng chi trả Rikkei...")
        
        # Duck Typing: gọi execute_payroll
        try:
            result = execute_payroll(payment_service, emp, amount)
            print("Xác thực đối tác bằng Duck Typing thành công!")
            print(f"Ngân hàng đối tác đã giải ngân thành công số tiền: {amount:,.0f} VND tới nhân sự {emp.emp_code}.")
        except AttributeError as e:
            print(f"Lỗi: {e}")
    
    except Exception as e:
        print(f"Lỗi: {e}")


def main():
    """Chương trình chính"""
    employees = []
    current_employee = [None]
    
    while True:
        print_menu()
        choice = input("Chọn chức năng (1-7): ").strip()
        
        if choice == '1':
            function_1_recruit(employees, current_employee)
        elif choice == '2':
            function_2_view_info(current_employee)
        elif choice == '3':
            function_3_update_kpi(current_employee)
        elif choice == '4':
            function_4_salary_summary(current_employee)
        elif choice == '5':
            function_5_working_hours_comparison(employees, current_employee)
        elif choice == '6':
            function_6_payroll_disbursement(current_employee)
        elif choice == '7':
            print("Cảm ơn đã sử dụng hệ thống Quản lý Nhân sự Rikkei Education Pro!")
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng chọn từ 1 đến 7.")


if __name__ == "__main__":
    main()