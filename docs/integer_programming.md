# Quy hoạch nguyên: Cơ sở lý thuyết, thuật toán và ứng dụng thực tiễn

## 1. Tổng quan và cơ sở lý thuyết của quy hoạch nguyên

**Quy hoạch nguyên (Integer Programming - IP)** là một nhánh chuyên sâu và phức tạp của tối ưu hoá toán học, 
đóng vai trò nền tảng trong việc giải quyết các bài toán quyết định rời rạc. Khác với quy hoạch tuyến tính (Linear Programming - LP) nơi các biến quyết định có thể nhận giá trị thực liên tục.
Quy hoạch nguyên áp đặt các ràng buộc nghiêm ngặt về tính nguyên lên một phần hoặc toàn bộ các biến số. Sự chuyển dịnh từ miền liên tục sang miền rời rạc này, mặc dù có vẻ đơn giản về mặt hình thức, 
lại thay đổi hoàn toàn bản chất tính toán, biến từ lớp bài toán có thể giải được tỏng thời gian đa thức (Polynomial Time) sang lớp bài toán NP-khó (NP-hard).

Báo cáo này được xây dựng dựa trên cấu trúc bài giảng về **Quy hoạch Nguyên Tuyến tính (Integer Linear Programming - ILP)**, 
mở rộng với các nghiên cứu chuyên sâu về lý thuyết nới lỏng (relaxation), các kỹ thuật sinh mặt cắt (cutting planes), và các ứng dụng thực tế trong quản lý vận hành.   

### 1.1. Phân loại và cấu trúc bài toán
Trong không gian tối ưu hoá rời rạc, các bài toán quy hoạch nguyên thường được phân loại dựa trên đặc tính của các biến quyết định:

* **Quy hoạch nguyên thuần tuý (Pure Integer Programming - IP):** Đây là dạng bài toán mà tính nguyên được yêu cầu cho tất cả các biến quyết định ($x \in \mathbb{Z}^n$). 
Miền chấp nhận được  $X$ là tập hợp các điểm lưới nguyên nằm trong một đa diện lồi được định nghĩa bởi các ràng buộc tuyến tính $Ax \le b$.

* **Quy hoạch nguyên hỗn hợp (Mixed Integer Programming - MIP):** Đây là lớp bài toán phổ biến nhất trong mô hình hoá thực tế, nơi chỉ một tập hợp con các biến ($I \subset \{1, \dots, n\}$) bị buộc phải là số nguyên, trong khi các biến còn lại ($C = \{1, \dots, n\} \setminus I$) có thể nhận giá trị thực. 
MIP cho phép mô hình hoá các chi phí cố định (fixed costs) kết hợp với các dòng chảy liên tục, ví dụ như trong bài toán thiết kế mạng lưới hoặc lập lịch sản xuất.  

* **Quy hoạch nguyên nhị phân (Binary Integer Programming - BIP):** Một trường hợp đặc biệt nhưng cực kỳ quan trọng, nơi các biến chỉ nhận giá trị 0 hoặc 1 ($x \in \{0, 1\}^n$). Các biến nhị phân đóng vai trò như các công tắc logic, cho phép mô hình hoá các quyết định định tính "có/không", "chọn/không chọn", hoặc các quan hệ logic phức tạp như "nếu A thì B". 


### 1.2. Lý thuyết nới lỏng (Relaxation Theory)

Khái niệm "nới lỏng" là trung tâm của mọi thuật toán giải quyết IP hiện đại. 
Do không thể sử dụng các phương pháp dựa trên đạo hàm (gradient-based) trong không gian rời rạc, chúng ta buộc phải thay thế bài toán gốc khó giải bằng bài toán gần đúng dễ giải hơn để thu thập thông tin về nghiệm tối ưu.

Một bài toán $(RP) \quad z^R = \max \{f(x) : x \in T\}$ được gọi là nới lỏng của bài toán gốc $(IP) \quad z = \max \{c^T x : x \in X\}$ nếu nó thỏa mãn hai điều kiện tiên quyết:
1. **Bao hàm miền nghiệm:** Tập nghiệm của bài toán nới lỏng phải chứa tập nghiệm của bài toán gốc ($X \subseteq T$).
2. **Bao hàm giá trị mục tiêu:** Với mọi nghiệm chấp nhận được, giá trị mục tiêu trong bài toán nới lỏng phải tốt hơn hoặc bằng giá trị mục tiêu gốc ($f(x) \ge c^T x, \forall x \in X$).

**Nới lỏng tuyến tính (Linear Relaxation)** 

Hình thức nới lỏng phổ biến nhất là nới lỏng tuyến tính (Linear Relaxation - LP Relaxation). Đối với một bài toán IP: $Z_{IP} = \max { c^T x : Ax \le b, x \in \mathbb{Z}^n_+ }$. Bài toán nới lỏng tương ứng được tạo ra bằng cách bỏ qua ràng buộc tính nguyên:

$$Z_{LP} = \max \{ c^T x : Ax \le b, x \in \mathbb{R}^n_+ \}$$

Giá trị tối ưu của bài toán nới lỏng cung cập một cận trên (uppber bound) cho bài toán gốc (đối với bài toán cực đại hoá). Mối quan hệ này là cơ sở cho các thuật toán nhánh cận: $Z_{IP} \le Z_{LP}$. Nếu nghiệm tối ưu của $Z_{LP}$ tình cờ thỏa mãn tính nguyên, đó chính là nghiệm tối ưu của $Z_{IP}$.

**Nới lỏng Lagrangian (Lagrangian Relaxation)**

Một kỹ thuật nới lỏng mạnh mẽ khác, thường được sử dụng khi nới lỏng tuyến tính không cung cấp cận đủ chặt, là nới lỏng Lagrangian. 
Ý tưởng cốt lõi là đưa ràng buộc "khó" vào hàm mục tiêu dưới dạng các khoản phạt (penalties) nhân với nhân tử Lagrange. 
Xét bài toán: $\min \{ cx : Ax \le b, Dx \le d, x \in \mathbb{Z}^n \}$. 
Nếu các ràng buộc $Ax \le b$ làm cho bài toán trở nên khó giải, ta có thể nới lỏng chúng bằng cách đưa vào hàm mục tiêu với vectơ nhân tử $\lambda \ge 0$:

$$Z_{LR}(\lambda) = \min \{ cx + \lambda(Ax - b) : Dx \le d, x \in \mathbb{Z}^n \}$$

Bài toán con này thường dễ giải hơn nhiều (ví dụ, có thể phân rã thành các bài toán con nhỏ hơn). 
Giá trị tối ưu của bài toán đối ngẫu Lagrangian $\max_{\lambda \ge 0} Z_{LR}(\lambda)$ cung cấp một cận dưới tốt hơn hoặc bằng so với nới lỏng tuyến tính. 


### 1.3. Cận nguyên thuỷ và cận đối ngẫu (Primal and Dual Bounds)

Trong quá trình giải một bài toán tối ưu hóa rời rạc, hai giá trị quan trọng luôn được duy trì và cập nhật liên tục:


| Loại cận | Định nghĩa (Bài toán Max)                                                         | Nguồn gốc                                       | Vai trò                                                                |
|----------|-----------------------------------------------------------------------------------|-------------------------------------------------|------------------------------------------------------------------------|
|Cận Nguyên thủy <br/>(Primal Bound - $\underline{Z}$) | Giá trị mục tiêu của một nghiệm chấp nhận được tốt nhất tìm thấy cho đến hiện tại | Heuristic, Nghiệm nguyên tìm thấy trong cây B&B | Đảm bảo sự tồn tại của nghiệm, dùng để cắt tỉa các nhánh kém tiềm năng |
|Cận Đối ngẫu <br/>(Dual Bound - $\overline{Z}$) | Giá trị chặn trên lý thuyết mà nghiệm tối ưu không thể vượt qua.                  | Nghiệm của bài toán nới lỏng (LP, Lagrangian).  | Đánh giá chất lượng nghiệm nguyên thuỷ, chứng minh tính tối ưu.        |

Mục tiêu của thuật toán là thu hẹp khoảng cách (gap) giữa hai cận này. Thuật toán dừng khi $\overline{Z} - \underline{Z} \le \epsilon$, hoặc đối với bài toán nguyên, khi $\lfloor \overline{Z} \rfloor = \underline{Z}$.1

## 2. Thuật toán nhánh và cận (Brand and Bound)

Thuật toán nhánh và cận (Branch and Bound - B&B) là phương pháp giải chính xác (exact method) tiêu chuẩn cho các bài toán quy hoạch nguyên. 
Nguyên lý hoạt động dựa trên chiến lược "chia để trị" (divide and conquer), chia nhỏ không gian tìm kiếm thành các bài toán con (subproblems) 
và sử dụng các cận để loại bỏ (prune/fathom) các vùng không gian không chứa nghiệm tối ưu. 

### 2.1. Cấu trúc cây tìm kiếm
Quá trinh B&B tạo ra một cây tìm kiếm (search tree) với:
* **Nút gốc (Root Node):** Đại diện cho bài toán ban đầu với đầy đủ miền nghiệm nhưng chưa có ràng buộc phân nhánh nào.

* **Các nút con (Child Nodes):** Đại diện cho các bài toán con với miền nghiệm bị thu hẹp bởi các ràng buộc phân nhánh thêm vào.

### 2.2. Quy trình xử lý tại một nút
Tại mỗi nút của cây tìm kiếm, ba bước chính được thực hiện:

1. **Nới lỏng (Relaxation):** Giải bài toán nới lỏng tuyến tính (LP relaxation) tương ứng với nút hiện tại. Giả sự nghiệm thu được là $x^*$ và giá trị mục tiêu là $z^*$.

2. **Kiểm tra cắt tỉa (Pruning):** Nút hiện tại có thể bị loại bỏ (Không cần xét tiếp các con của nó) nếu một trong ba điều kiện sau xảy ra: 
   * **Vô nghiệm (infeasibility):** Bài toán nới lỏng vô nghiệm $\implies$ Bài toán gốc tại nhánh này cũng vô nghiệm.
   * **Giới hạn cận (Bound):**  Giá trị $z^*$ tồi hơn hoặc bằng cận nguyên thủy tốt nhất hiện có ($\underline{Z}$). Đối với bài toán Max, nếu $z^* \le \underline{Z}$, thì không thể tìm thấy nghiệm tốt hơn $\underline{Z}$ trong nhánh này.
   * **Tính nguyên (Integrality):** Nghiệm $x^*$ thỏa mãn tất cả các ràng buộc nguyên. Đây là một nghiệm chấp nhận được cho bài toán gốc. Ta cập nhật $\underline{Z} = \max(\underline{Z}, z^*)$ và lưu nghiệm này làm nghiệm tốt nhất hiện tại (incumbent).

3. **Phân nhánh (Branching):** Nếu không thể cắt tỉa (tức là $z^* > \underline{Z}$ và $x^*$ chưa nguyên), ta chọn một biến $x_j$ có giá trị phân số $\bar{x}_j$ trong nghiệm nới lỏng để phân nhánh. Ta tạo ra hai nút con bằng cách thêm ràng buộc:
    * **Nút con 1:** $x_j \le \lfloor \bar{x}_j \rfloor$
    * **Nút con 2:** $x_j \ge \lceil \bar{x}_j \rceil$. Việc này chia miền nghiệm thành hai phần rời nhau, loại bỏ giá trị phân số $\bar{x}_j$ hiện tại nhưng vẫn bảo toàn tất cả các điểm nguyên.

### 2.3. Chiến lược chọn nút và biến phân nhánh

Hiệu suất B&B phụ thuộc rất lớn vào các chiến lược heuristic:

* **Chiến lược chọn nút (Node Selection Strategy):**
  * Depth-First Search (DFS): Ưu tiên đi sâu xuống cây. Lợi ích là giữ nguyên cấu trúc bài toán LP (dễ giải lại bằng Dual Simplex) và nhanh chóng tìm thấy nghiệm nguyên để cập nhật cận dưới. 
  * Best-Bound Search: Chọn nút có cận đối ngẫu tốt nhất. Chiến lược này giúp cải thiện cận trên toàn cục, nhưng tiêu tốn bộ nhớ hơn. 

* **Chiến lược chọn biến (Variable Selection/Branching Rule):**
  * _Most Infeasible Branching:_ Chọn biến có phần thập phân gần nhất 0.5 nhất (độ vi phạm tính nguyên lớn nhất).
  * _Strong Branching:_ Thử nghiệm giải sơ bộ LP cho một số biến ứng viên và chọn biến làm tăng cận đối ngẫu (giảm $Z^{LP}$) nhiều nhất. Phương pháp này rất mạnh nhưng tốn kém chi phí tính toán.
  * _Pseudocost Branching:_ Sử dụng lịch sử phân nhánh để ước lượng tác động của việc phân nhánh lên hàm mục tiêu mà không cần giải thử LP.

## 3. Phương pháp mặt cắt (Cutting Plane Methods)
Nếu B&B tiếp cận bài toán bằng cách chia nhỏ không gian, thì phương pháp Mặt cắt (Cutting Planes) tiếp cận bằng cách làm chặt (tighten) không gian đó. 
Mục tiêu là tìm các bất đẳng thức hợp lệ (valid inequalities) để cắt bỏ nghiệm phân số của bài toán nới lỏng mà không loại bỏ bất kỳ nghiệm nguyên nào. 

### 3.1. Nguyên lý hình học

Xét đa diện $P$ của bài toán nới lỏng LP và bao lồi $P_I$ của các điểm nguyên ($P_I = \text{conv}(P \cap \mathbb{Z}^n)$). 
Nghiệm tối ưu của LP, $x^*_{LP}$, thường là một đỉnh của $P$ nhưng nằm ngoài $P_I$. Một "mặt cắt" là một siêu phẳng ngăn cách $x^*_{LP}$ khỏi $P_I$. 
Bằng cách thêm mặt cắt này vào $P$, ta thu được một đa diện mới $P'$ chặt hơn ($P_I \subseteq P' \subset P$). Lặp lại quá trình này sẽ đẩy nghiệm LP dần về phía $P_I$.


### 3.2. Làm tròn nguyên (Integer Rounding)

Một kỹ thuật cơ bản để tạo mặt cắt là khai thác tính chất nguyên của biến số trong các bất đẳng thức. 
Xét ràng buộc: $\sum a_j x_j \le b$. Nếu tất cả $a_j$ là số nguyên và $x_j$ là biến nguyên không âm, thì vế trái luôn là số nguyên. 
Do đó, giá trị của nó không thể vượt quá phần nguyên của $b$.Ta có bất đẳng thức mạnh hơn (Chvátal-Gomory cut): $\sum \lfloor a_j \rfloor x_j \le \lfloor b \rfloor$.10

Ví dụ từ tài liệu 1: Xét miền $P = \{ x \in \mathbb{R}^3_+ : 5x_1 + 9x_2 + 13x_3 \ge 19 \}$.
Chia cho 5: $x_1 + 1.8x_2 + 2.6x_3 \ge 3.8$. Vì $x \ge 0$, ta có thể làm giảm hệ số vế trái: $x_1 + 2x_2 + 3x_3 \ge x_1 + 1.8x_2 + 2.6x_3 \ge 3.8$.
Do vế trái là biểu thức nguyên (với $x$ nguyên), giá trị của nó phải $\ge \lceil 3.8 \rceil = 4$.
Valid inequality: $x_1 + 2x_2 + 3x_3 \ge 4$.

### 3.3. Mặt cắt Gomory (Gomory Mixed Integer Cuts)

Mặt cắt Gomory là kỹ thuật tổng quát nhất, có thể sinh ra từ bất kỳ hàng nào của bảng đơn hình tối ưu chứa biến cơ sở có giá trị phân số.

**Dẫn xuất toán học:** Tại bảng đơn hình tối ưu, xét phương trình của một biến cơ sở $x_i$:

$$x_i + \sum_{j \in J} \bar{a}_{ij} x_j = \bar{b}_i$$

Trong đó $J$ là tập các biến phi cơ sở, $\bar{b}_i$ không nguyên. Ta tách các hệ số thành phần nguyên và phần thập phân: $\bar{a}_{ij} = \lfloor \bar{a}_{ij} \rfloor + f_{ij}$ và $\bar{b}_i = \lfloor \bar{b}_i \rfloor + f_i$ (với $0 \le f < 1$).Viết lại phương trình:

$$x_i + \sum (\lfloor \bar{a}_{ij} \rfloor + f_{ij}) x_j = \lfloor \bar{b}_i \rfloor + f_i$$

Gom nhóm các phần nguyên và phần thập phân:

$$x_i + \sum \lfloor \bar{a}_{ij} \rfloor x_j - \lfloor \bar{b}_i \rfloor = f_i - \sum f_{ij} x_j$$

Vế trái là một số nguyên (vì $x$ nguyên). Do đó vế phải cũng phải là số nguyên. Mặt khác, vì $f_i < 1$ và $\sum f_{ij} x_j \ge 0$ (do $x_j \ge 0$ trong LP), vế phải luôn nhỏ hơn 1. Một số nguyên nhỏ hơn 1 buộc phải $\le 0$. Vậy:

$$f_i - \sum_{j \in J} f_{ij} x_j \le 0 \implies \sum_{j \in J} f_{ij} x_j \ge f_i$$

Đây là dạng cơ bản của mặt cắt Gomory (fractional cut). Đối với bài toán MIP, công thức phức tạp hơn một chút để xử lý các biến liên tục, nhưng nguyên lý "tách phần nguyên" vẫn giữ nguyên.

**Vấn đề ổn định số:** Trong lịch sử, mặt cắt Gomory từng bị coi là kém hiệu quả do vấn đề sai số tính toán (numerical instability). 
Các phép chia và làm tròn trên máy tính có thể tích luỹ sai số, dẫn đến việc tạo ra các mặt cắt sai (cắt bỏ cả nghiệm tối ưu). 
Tuy nhiên, các bộ giải hiện đại đã áp dụng các kỹ thuật "safe rounding" và quản lý mặt cắt, biến Goromy cuts thành thành phần quan trọng giúp giảm kích thước cây tìm kiếm tới 50% trong nhiều bài toán. 

## 4. Thuật toán lai: Nhánh và Cắt (Branch and Cut)

Thuật toán Nhánh và Cắt (Branch and Cut - B&C) là sự kết hợp tối ưu giữa B&B và Cutting Planes. Đây là "tiêu chuẩn vàng" trong các bộ giải MIP hiện đại như CPLEX, Gurobi và SCIP (được tích hợp trong Google OR-Tools).

### 4.1. Cơ chế hoạt động

Thay vì chỉ phân nhánh khi gặp nghiệm phân số, B&C cố gắng thêm các mặt cắt ngay tại nút đó để thắt chặt miền nghiệm trước khi buộc phải phân nhánh. Quy trình tại một nút xử lý như sau:

1. **Giải nới lỏng:** Giải LP tại nút hiện tại. 
2. **Kiểm tra nghiệm:** Nếu nghiệm vô nghiệm hoặc nguyên, xử lý như B&B truyền thống. 
3. **Vòng lặp mặt cắt (Cut Loop):** Nếu nghiệm là phân số:
   * Tìm kiếm các mặt cắt bị vi phạm (Seperation Problem). Các loại mặt cắt thường dùng bao gồm **Gomory cuts, Cover cuts** (cho bài toán Knapsack), **Clique cuts** (cho bài toán set packing).
   * Nếu tìm thấy mặt cắt hiệu quả, thêm vào LP và giải lại (quay về bước 1). Bước này lặp lại cho đến khi không tìm thấy mặt cắt nào hoặc sự cải thiện cận không đáng kể (tailing off).
4. **Phân nhánh:** Khi không thể thêm mắt cắt nữa, tiến hành phân nhánh biến số.


### 4.2. Ưu điểm chiến lược
Sự kết hợp này tận dụng ưu điểm của cả hai phương pháp:
* Mặt cắt giúp cải thiện cận đối ngẫu (Dual Bound) nhanh chóng mà không làm tăng kích thước cây tìm kiếm.
* Phân nhánh giúp chia nhỏ bài toán khi mắt cắt không còn hiệu quả (tránh hiện tượng hội tụ chậm của phương pháp mặt cắt thuần tuý). 
Sơ đồ thuật toán trong tài liệu 1 (trang 21) minh họa rõ quy trình này: một vòng lặp `LP RELAXATION` $\leftrightarrow$ `CUT` nằm bên trong quy trình xử lý nút trước khi đến bước `BRANCHING`.


## 5. Kỹ thuật mô hình hoá và tuyến tính hoá nâng cao

Khả năng giải quyết bài toán không chỉ phụ thuộc vào thuật toán mà còn phụ thuộc vào cách mô hình hoá. 
Nhiều ràng buộc logic phi tuyến có thể được chuyển đổi về dạng tuyến tính MIP bằng cách sử dụng biến nhị phân và kỹ thuật Big-M

### 5.1. Ràng buộc Logic "If - Then"
Cấu trúc logic: "Nếu biến nhị phân $\delta = 1$ thì ràng buộc $f(x) \le b$ phải thỏa mãn. Nếu $\delta = 0$, ràng buộc này được bỏ qua." 

Mô hình hóa:

$$f(x) \le b + M(1 - \delta)$$

Trong đó $M$ là một hằng số dương đủ lớn (Big-M).

* Khi $\delta = 1$: $f(x) \le b$ (ràng buộc kích hoạt).
* Khi $\delta = 0$: $f(x) \le b + M$ (luôn đúng với $M$ lớn, ràng buộc vô hiệu).1

**Ứng dụng trong TSP:** Ràng buộc loại bỏ chu trình con (Subtour Elimination) trong mô hình MTZ sử dụng logic này. 
Nếu xe đi từ $i$ đến $j$ ($x_{ij}=1$), thì thứ tự thăm của $j$ ($u_j$) phải lớn hơn $i$ ($u_i$).
    
$$u_i - u_j + 1 \le M(1 - x_{ij}) \iff u_i - u_j + (n-1)x_{ij} \le n-2$$ 

Ở đây $M = n-1$ là chặn trên chặt chẽ cho sự chênh lệch thứ tự.

### 5.2. Tuyến tính hoá tích của các biến

Tích hai biến nhị phân ($z = x \cdot y$): $z$ sẽ bằng 1 khi và chỉ khi cả $x$ và $y$ đều bằng 1. Hệ ràng buộc:

$$z \le x; \quad z \le y; \quad z \ge x + y - 1; \quad z \ge 0$$.

Tích biến nhị phân và biến liên tục ($z = x \cdot y$): Với $x \in \{0, 1\}$ và $0 \le y \le U$.Hệ ràng buộc:

$$z \le U \cdot x$$

$$z \le y$$

$$z \ge y - U(1 - x)$$

$$z \ge 0$$

Nếu $x=0 \implies z=0$. Nếu $x=1 \implies z=y$. 

### 5.3. Hàm Max/Min và Giá trị Tuyệt đối

1. Hàm Max ($z = \max(x, y)$): Cần biến nhị phân $t$ để chỉ thị $x$ hay $y$ lớn hơn.

$$z \ge x; \quad z \ge y$$

$$z \le x + M(1-t)$$

$$z \le y + M \cdot t$$.

Giá trị Tuyệt đối ($|f(x)| \le z$): Tương đương với hệ hai bất đẳng thức tuyến tính:

$$f(x) \le z$$

$$-f(x) \le z$$

Ngược lại, với $|f(x)| \ge z$, ta cần biến nhị phân để tách thành hai trường hợp rời rạc (disjunctive constraints).

## 6. Triển khai tính toán với Google OR-Tools

Google OR-Tools cung cấp một hệ sinh thái mạnh mẽ để giải quyết các bài toán MIP. 
Việc lựa chọn công cụ và cách triển khai mã nguồn đóng vai trò quyết định đến hiệu năng.

### 6.1. Lựa chọn bộ giải (Solver Selection)
OR-Tools cung cấp hai giao diện chính cho bài toán nguyên:

1. **MPSolver (`pywraplp`):** Giao diện truyền thống cho MIP. Nó hoạt động như một wrapper gọi tới các backend solvers. 
   * `SCIP`: Bộ giải phi thương mại mặc định, rất mạnh cho MIP tổng quát. 
   * `GLOP`: Bộ giải LP của Google (chỉ dùng cho nới lỏng).
   * `CBC`: Một lựa chọn mã nguồn mở khác.
   * `GUROBI`, `CPLEX`: Các bộ giải thương mại hiệu năng cao (cần license).
   * **Lưu ý:** `pywraplp` phù hợp khi mô hình có biến liên tục (Mixed Integer). 

2. CP-SAT (`cp_model`): Bộ giải Constraint Programming (CP) thế hệ mới dựa trên công nghệ SAT (Satisfiability).
   * **Ưu điểm:** Cực kỳ hiệu quả cho các bài toán tổ hợp thuần tuý (Pure Integer), lập lịch (scheduling), và các bài toán có ràng buộc logic phức tạp (Boolean Constraints).
   * **Khác biệt:** CP-SAT chỉ làm việc với số nguyên. Nếu bài toán có biến liên tục, phải nhân tỷ lệ (scaling) để chuyển về nguyên hoặc dùng `pywraplp`. CP-SAT thường vượt trội hơn các bộ giải MIP truyền thống trong các bài toán lập lịch và phân công. 

### 6.2. Phân tích mã nguồn và Best Practices

Dựa trên các ví dụ trong tài liệu và snippet, quy trình chuẩn bao gồm:
* **Khai báo:**
    ```bash
    from ortools.linear_solver import pywraplp
    solver = pywraplp.Solver.CreateSolver('SCIP')
    ```
* **Biến:** Sử dụng IntVar cho biến nguyên và NumVar cho biến thực.

    ```bash
    x = solver.IntVar(0, infinity, 'x')
    ```

* **Ràng buộc:** Có thể thêm trực tiếp biểu thức Python.

    ```bash
    solver.Add(x + 7*y <= 17.5)
    ```
* **Tham số:** Cần chú ý các tham số về thời gian (`SetTimeLimit`) và dung sai (`SetRelativeGap`) để tránh việc bộ giải chạy vô hạn trên các bài toán lớn.
* **Debug:** Sử dụng `EnableOutput()` để xem log quá trình B&C (số node, số cuts, giá trị cận) giúp chẩn đoán hiệu năng mô hình.

## 7. Phân tích các bài toán ứng dụng điển hình

### 7.1. Bài toán phân công giáo viên (Balanced Class Teacher Assignment)

**Bài toán:** Phân công $n$ lớp học cho $m$ giáo viên sao cho tải trọng (số tín chỉ) lớn nhất của một giáo viên là nhỏ nhất, thoả mãn các ràng buộc về chuyên môn và xung đột thời gian.

**Mô hình MIP:**
* **Biến:** $x_{ij} \in \{0, 1\}$ (Giáo viên j dạy lớp i). Biến phụ trợ **L_max** (Tải trọng lớn nhất).
* **Hàm mục tiêu:** $\min L_{max}$. Đây là mô hình Minimax điển hình.
* **Ràng buộc:**
1. Phủ kín: $\sum_j x_{ij} = 1, \forall i$ (Mỗi lớp có đúng 1 giáo viên).
2. Chuyên môn: $x_{ij} = 0$ nếu $j \notin T(i)$ (Chỉ phân công nếu dạy được).
3. Xung đột: $x_{i_1 j} + x_{i_2 j} \le 1, \forall j, \forall (i_1, i_2) \in Q$ (Không dạy 2 lớp trùng giờ). Ràng buộc này tương đương với bài toán tìm tập độc lập trên đồ thị xung đột.
4. Cân bằng tải: $\sum_i c(i) x_{ij} \le L_{max}, \forall j$. Ràng buộc này liên kết biến quyết định với biến mục tiêu Minimax.

**Insight:** Đây là bài toán Bottleneck Assignment. Việc tối ưu $L_{max}$ giúp đảm bảo công bằng. 
Trong thực tế, có thể thêm hàm mục tiêu phụ để tối thiểu hoá tống số giáo viên sử dụng hoặc tối ưu nguyện vọng (preference).

### 7.2. Bài toán hiệu chỉnh nhóm máu (Blood Type Correction Problem)
**Bài toán:** Dữ liệu phả hệ bị lỗi. Cần tìm số lượng sửa đổi ít nhất để toàn bộ cây gia phả tuân theo quy luật di chuyền Mendel.

**Cơ sở sinh học & Logic:**
- Genotype (kiểu gen): AA, AO $\to$ A; BB, BO $\to$ B; AB $\to$ AB; OO $\to$ O.
- Quy luật: Con nhận 1 alen từ cha và 1 alen từ mẹ. 
- Ví dụ logic: Nếu cha mẹ là (O, O), con chắc chắn là O. Nếu cha mẹ là (AB, O), con chỉ có thể là A hoặc B (không thể là AB hay O).

**Mô hình MIP:**
- **Biến:**  $x_{i, \text{type}} \in \{0, 1\}$ xác định nhóm máu đích thực của người $i$. Biến $y_i$ xác định xem người $i$ có bị sửa đổi so với dữ liệu gốc không.
- **Ràng buộc di truyền (Hard Constraints):** Đây là thách thức lớn nhất. Cần chuyển đổi bảng quy luật di truyền thành các bất đẳng thức tuyến tính. Ví dụ: Luật "Con O thì cha mẹ không thể là AB".

$$x_{i, O} + x_{\text{cha}, AB} \le 1$$

$$x_{i, O} + x_{\text{mẹ}, AB} \le 1$$

Tài liệu  liệt kê đầy đủ 4 quy tắc suy diễn logic để bao phủ mọi trường hợp.

- **Hàm mục tiêu:** $\min \sum y_i$.

**Insight:** Đây là bài toán _Maximum Feasible Subsystem_ hoặc _Data Cleaning_. Với các dây phả hệ lớn và phức tạp, việc sử dụng CP-SAT sẽ hiệu quả hơn MIP truyền thống do bản chất bài toán thuần tuý logic và rời rạc.


### 7.3. Bài toán người du lịch (TCP)

**Bài toán:** Tìm chu trình Hamilton ngắn nhất trên đồ thị đầy đủ có trọng số.

**Mô hình và Thách thức:**

- Ràng buộc bậc (Degree constraints): Vào 1, ra 1 tại mỗi nút. Dễ mô hình hóa.
- Ràng buộc loại bỏ chu trình con (Subtour Elimination Constraints - SECs): Khó khăn nhất.
  * Phương pháp Dantzig-Fulkerson-Johnson (DFJ): $\sum_{i,j \in S} x_{ij} \le |S| - 1, \forall S \subset V$. Số lượng ràng buộc là $2^n$, không thể liệt kê hết.
  * Phương pháp trong Slide : **Lazy Constraints (Cắt lười).**
    * Giải bài toán chỉ với ràng buộc bậc (đây là bài toán Assignment).
    * Kiểm tra nghiệm: Nếu tạo thành 1 chu trình duy nhất $\to$ Tối ưu.
    * Nếu tạo thành nhiều chu trình con rời rạc: Tìm các chu trình con này, thêm ràng buộc SEC vi phạm tương ứng vào mô hình và giải lại.
Đây chính là ứng dụng thủ công của quy trình Branch and Cut. Cách này hiệu quả hơn nhiều so với mô hình MTZ (Miller-Tucker-Zemlin) vốn yếu (weak relaxation) dù số lượng biến ít hơn ($O(n^2)$).

### 7.4. Bài toán định vị cơ sở (Facility Location Problem)

**Bài toán:** Chọn mở các nhà máy nào ($y_i$) để phục vụ nhu cầu khách hàng ($d_j$) sao cho tổng chi phí (mở nhà máy + vận chuyển) là nhỏ nhất.

**Mô hình:**

- Hàm mục tiêu: $\min \sum f_i y_i + \sum c_{ij} x_{ij}$.
- Ràng buộc:
  * Đáp ứng nhu cầu: $\sum_i x_{ij} = d_j$.
  * Năng lực (Capacity): $\sum_j x_{ij} \le Q_i y_i$.

**Insight về "Strong Formulation":** Ràng buộc năng lực về mặt logic là đủ: Nếu $y_i=0 \implies \sum x_{ij} \le 0 \implies x_{ij}=0$. Tuy nhiên, miền nới lỏng LP của ràng buộc này rất lỏng lẻo (weak).Để tăng cường (tighten) mô hình, ta nên thêm các ràng buộc dư thừa logic nhưng mạnh về hình học (Valid Inequalities):

$$x_{ij} \le d_j y_i$$

Ràng buộc này (variable upper bound constraints) buộc $x_{ij}$ phải bằng 0 ngay khi $y_i$ có giá trị nhỏ trong bài toán nới lỏng, giúp cận đối ngẫu $\overline{Z}$ chặt hơn rất nhiều, làm giảm đáng kể thời gian chạy B&B.

### 7.5. Bài toán định tuyến Multicast và VRP

**Multicast Routing:** Tìm cây Steiner trên đồ thị để truyền tin từ nguồn đến nhiều đích với ràng buộc độ trễ.

- **Mô hình:** Sử dụng biến luồng hoặc biến thời gian tích lũy $Y_i$ tại mỗi nút để kiểm soát độ trễ.Ràng buộc: $Y_i + t_{ij} \le Y_j + M(1 - x_{ij})$. Nếu cạnh $(i, j)$ được chọn, thời gian tại $j$ phải lớn hơn tại $i$. 
- **Ràng buộc** $Y_{\text{đích}} \le L_{max}$ đảm bảo QoS (Chất lượng dịch vụ).

**Capacitated Vehicle Routing Problem (CVRP):** 

- Đây là sự mở rộng của TSP với nhiều xe và ràng buộc dung lượng. 
- Mô hình trong slide sử dụng biến 3 chỉ số $X_{ijk}$ (xe $k$ đi từ $i$ đến $j$) hoặc biến tích lũy tải trọng để loại bỏ chu trình con và đảm bảo không vượt quá tải trọng xe. Tương tự TSP, các ràng buộc SEC là mấu chốt và thường được xử lý bằng Branch and Cut.

## Kêt luận và khuyến nghị

Quy hoạch nguyên là một công cụ cực kỳ mạnh mẽ, cho phép giải quyết chính xác các bài toán quyết định phức tạp trong thực tế. Tuy nhiên, bản chất NP-khó đòi hỏi người thực hiện phải nắm vững không chỉ cú pháp công cụ (như OR-Tools) mà còn cả lý thuyết sâu sắc bên dưới. 

**Các điểm mấu chốt cần ghi nhớ:**
1. **Mô hình hoá là nghệ thuật:** Một mô hình tốt (Strong Formulation) với các ràng buộc chặt (như trong Facility Location) có giá trị hơn một máy tính mạnh. Hãy luôn tìm cách thêm các "Valid Inequalities" để hỗ trợ bộ giải. 
2. **Hiểu rõ thuật toán:** Biết cách B&B và Gomory Cuts hoạt động giúp ta hiểu tại sao bộ giải bị chậm (ví dụ: do Big-M quá lớn làm yếu cận LP), hay do đối xứng symmetry. 
3. **Lựa chọn công cụ:** Với các bài toán logic thuần tuý (như Blood Type, Xếp lịch), hãy cân nhắc CP-SAT thay vì MIP truyền thống. 
4. **Tuyến tính hoá:** Nắm vững kỹ thuật Big-M và xử lý biến nhị phân là kỹ thuật sinh tồn trong thế giới IP.


