# Cơ sở lý thuyết, Kiến trúc thuật toán và ứng dụng thực tiễn của Constraint Programming

## 1. Giới thiệu và phạm vi nghiên cứu

Trong bối cảnh Computer Science và Operation Research, Constraint Programming đã nổi lên như một phương pháp luận mạnh mẽ để giải quyết các bài toán tổ hợp phức tạp.
Khác với các phương pháp lập trình mệnh lệnh truyền thống, nơi lập trình viên phải chỉ rõ từng bước thực hiện để đạt được kết quả, CP thuộc về mô hình lập trình khai báo
(declarative programming). Tại đây, trọng tâm được chuyển dịch từ việc định nghĩa "làm thế nào" (how) sang việc mô tả chính xác "cái gì" (what) là vấn đề cần giải quyết thông qua tập hợp các biến và các ràng buộc giữa chúng.

Nội dung của báo cáo bao gồm việc phân tích nền tảng lý thuyết toán học của **Bài toán Thỏa mãn Ràng buộc (CSP)**, cơ chế lan truyền ràng buộc (constraint propagation), các chiến lược tìm kiếm (search strategies), 
và việc ứng dụng thực tiễn thông qua các công cụ hiện đại như Google OR-Tools. Đặc biệt, báo cáo sẽ đi sâu vào các khía cạnh kỹ thuật như sự khác biệt giữa các mức độ nhất quán (consistency levels), 
vai trò của các ràng buộc toàn cục (global constraints), và các nguyên lý thiết kế heuristic trong tìm kiếm.

### 1.1. Bối cảnh lịch sử và sự phát triển

Lập trình ràng buộc không phải là một phát minh đơn lẻ mà là kết quả của sự hội tự giữa Trí tuệ nhân tạo (AI) và vận trù học (Operation Research - OR). 
Nó bắt đầu phát triển mạnh mẽ từ những nằm 1980, với sự ra đời của các ngôn ngữ như Prolog III tại Marseille (Pháp), CLP(R) tại Melbourne và IBM, hay CHIP tại ECRC (Đức). 
Sự giao thoa này đã tạo ra một lĩnh vực nghiên cứu năng động, được thúc đẩy bởi nhu cầu giải quyết các bài toán lập lịch, phân bổ nguồn lực, và cấu hình sản phẩm trong công nghiệp, 
những nơi mà các phương pháp truyền thống thường gặp khó khăn do sự bùng nổ tổ hợp của không gian tìm kiếm.

## 2. Lý thuyết hình thức và bài toán thoả mãn ràng buộc (CSP)

Để hiểu sâu về CP, trước hết cần thiết lập một nền tảng toán học vững chắc cho đối tượng nghiên cứu chính: **Bài toán Thoả mãn ràng buộc (CSP**). 
Một CSP được định nghĩa hình thức bởi một bộ ba $\langle X, D, C \rangle$, tạo thành cấu trúc cốt lõi cho mọi mô hình CP. 

### 2.1. Các thành phần cấu trúc

- **Tập hợp biến  $X = \{x_1, x_2, \dots, x_n\}$**: Đây là các thực thể đại diện cho các quyết định cần được đưa ra. Trong bài toán lập lịch lớp học, biến có thể là thời gian bắt đầu của một môn học; trong bài toán N-hậu, biến là vị trí hàng của quân hậu trên bàn cờ.
- **Tập hợp miền giá trị $D = \{D_1, D_2, \dots, D_n\}$**:  Mỗi biến $x_i$ được liên kết với một miền giá trị $D_i$, tập hợp các giá trị khả dĩ mà biến đó có thể nhận. Miền này có thể là tập hợp số nguyên hữu hạn (Finite Domain), tập số thực (cho các bài toán liên tục),
hoặc các cấu trúc phức tạp hơn như tập hợp (Finite Sets) hay đồ thị. Trong phạm vi báo cáo này và tài liệu tham khảo, trong tâm chính là miền hữu hạn (Finite Domain - FD).
- **Tập hợp ràng buộc  $C = \{c_1, c_2, \dots, c_m\}$**: Một ràng buộc $c_j$ là một quan hệ được định nghĩa trên một tập con các biến, quy định các tổ hợp giá trị được phép hoặc bị cấm. Ví dụ, ràng buộc "không có hai quân hậu nào cùng hàng" trong bài toán N-hậu là một ràng buộc cấm có cặp giá trị trùng nhau.

### 2.2. Định nghĩa nghiệm và độ phức tạp tính toán

Một nghiệm của CSP là một phép gán giá trị đầy đủ (complete assignment) cho tất cả các biến,  $\theta = \{x_1 \leftarrow v_1, \dots, x_n \leftarrow v_n\}$, sao cho $v_i \in D_i$ với mọi $i$, và mọi ràng buộc $c_j \in C$ đều được thỏa mãn.
Nếu bài toán yêu cầu một nghiệm tối ưu hoá một hàm mục tiêu $f(X)$, nó trở thành bài toán tối ưu hoá ràng buộc (COP). Trong trường hợp này, CP không chỉ tìm kiếm sự thoả mãn (satisfaction) mà còn chứng minh tính tối ưu (optimality) hoặc tìm ra cận tốt nhất. 

Về mặt lý thuyết độ phức tạp, CSP thuộc lớp bài toán NP-Hard. Điều này ngụ ý rằng, trong trường hợp xấu nhất, thời gian để tìm ra nghiệm hoặc chứng minh vô nghiệm sẽ tăng theo hàm mũ so với kích thước đầu vào. Không có thuật toán đa thức nào được biết đến có thể giải quyết mọi CSP. 
Tuy nhiên, sự "khó khăn" này không đồng đều; nhiều bài toán thực tế có cấu trúc đặc biệt mà CP có thể khai thác để giải quyết hiệu quả hơn nhiều so với tìm kiếm vét cạn thuần tuý. 

### 2.3. Phân loại ràng buộc trong mô hình hoá

Sức mạnh biểu đạt của CP nằm ở sự đa dạng của các loại ràng buộc có thể mô hình hoá:

- **Ràng buộc số học (Numerical Constraints):** Các bất phương trình hoặc phương trình tuyến tính/phi tuyến, ví dụ: $2X + 3Y \le 17$ hoặc $X^2 - Y^3 = 17$. 
CP xử lý các ràng buộc này không chỉ bằng các phương pháp đại số mà còn thông qua lan truyền biên. 
- **Ràng buộc ký hiệu (Symbolic Constraints):** Đây là một đặc trưng độc đáo của CP, cho phép sử dụng biến làm chỉ số cho mảng, ví dụ: `cost = sum(price[rack[i]])`. 
Khả năng này giúp mô hình hóa các bài toán định tuyến hay phân bổ một cách tự nhiên, trực quan hơn nhiều so với Lập trình Nguyên (Integer Programming - MIP).   

- **Ràng buộc logic (Logical Constraints):** Kết hợp các mệnh đề boolean, ví dụ: $(X > 5) \lor (Y < 3) \implies (Z = 1)$. Trong Google OR-Tools, điều này thường được thực hiện thông qua cơ chế `OnlyEnforceIf`, cho phép kích hoạt ràng buộc dựa trên giá trị của biến logic.

## 3. Cơ chế lan truyền ràng buộc (Constaint Propagation) và các mức độ nhất quán

Nếu tìm kiếm (search) là động cơ của CP, thì lan truyền ràng buộc (propagation) chính là hệ thống dẫn đường giúp tránh các ngõ cụt.
Mục tiêu cốt lõi của lan truyền là suy diễn diễn ra các hệ quả từ các ràng buộc hiện có để loại bỏ các giá trị không thể tham gia vào lời giải khỏi miền của các biến, từ đó thu hẹp không gian tìm kiếm một cách đáng kể trước khi thực hiện bất kỳ quyết định phân nhánh nào. 

### 3.1. Khái niệm nhất quán cục bộ (Local Consistency)

Thay vì kiểm tra tính nhất quán của toàn bộ bài toán (Global Consistency - vốn rất tốn kém), CP tập trung vào nhất quán cục bộ. 
Một bài toán được gọi là nhất quán cục bộ nếu mọi ràng buộc riêng lẻ hoặc nhóm nhỏ các ràng buộc đều thoả mãn một tính chất nhất quán nào đó. 

#### 3.1.1. Nhất quán miền (Domain Consistency - DC) / Nhất quán Cung (Arc Consistency)

Đây được coi là "chén thánh" trong lan truyền ràng buộc cho các miền hữu hạn.
- **Định nghĩa:** Một ràng buộc C đạt được nhất quán miền (domain consistency) nếu với mỗi biến $x_i$ thuộc phạm vi của C và mỗi giá trị $v \in D(x_i)$, tồn tại ít nhất một bộ giá trị $\{v_j\}$ trong miền của các biến còn lại $x_j$ sao cho bộ giá trị $\{v, \{v_j\}\}$ thoả mãn C. Giá trị $v$ được gọi là có "giá trị hỗ trợ" (support).
- **Cơ chế hoạt động:** Nếu một giá trị $v$ trong miền của $x_i$ không có hỗ trợ, nó sẽ bị loại bỏ khỏi $D(x_i)$. Việc loại bỏ này có thể kích hoạt làn truyền sang các ràng buộc khác.
- **Ví dụ:** Xét ràng buộc $X < Y$ với  $D(X) = \{4, 5\}$ và $D(Y) = \{2, 3\}$.
  * Xét $X=4$: Cần tìm $y \in D(Y)$ sao cho $4 < y$. Không có giá trị nào trong $\{2, 3\}$ thỏa mãn. Vậy 4 bị loại khỏi $D(X)$.
  * Xét $X=5$: Tương tự, không có $y$ nào thỏa mãn $5 < y$. Vậy 5 bị loại.
  * Kết quả: $D(X) = \emptyset$, phát hiện mâu thuẫn ngay lập tức.
- **Đánh đổi:** Mặc dù DC có khả năng lọc mạnh nhất, chi phí tính toán để duy trì nó có thể rất cao (đa thức bậc cao), đặc biệt với các ràng buộc n-ngôi phức tạp.

#### 3.1.2. Nhất quán biên (Bound Consistency - BC)

Trong nhiều trường hợp thực tế, đặc biệt với miền giá trị lớn hoặc ràng buộc số học, việc duy trì DC là quá tốn kém. Nhất quán biên là một sự nới lỏng (relaxation) hiệu quả.

- **Định nghĩa:** Một ràng buộc đạt BC nếu các cận dưới (min) và cận trên (max) của mỗi biến đều có hỗ trợ miền thực (Bound(R)) hoặc miền nguyên (Bound(Z)) của các biến khác. 
- **Ví dụ:** Xét các phương trình $X = Y + Z$ với các miền liên tục. Thay vì kiểm tra từng điểm, thuật toán chỉ cần cập nhật:
  * $min(X) \leftarrow \max(min(X), min(Y) + min(Z))$
  * $max(X) \leftarrow \min(max(X), max(Y) + max(Z))$
  * Và tương tự cho Y, Z. 
- **Ưu điểm:** Chi phí tính toán thấp, thường là $O(1)$ cho mỗi lần cập nhật ràng buộc số học cơ bản. Tuy nhiên, khả năng lọc yếu hơn DC vì nó không thể phát hiện được các "lỗ hổng" ở miền giá trị.

#### 3.2. Thuật toán làn truyền AC-3

Thuật toán lan truyền phổ biến nhất là AC-3 (Arc Consistency Algorithm #3). Nó hoạt động dựa trên một hàng đợi Q chứa các cặp (biến, ràng buộc) cần kiểm tra.
1. **Khởi tạo:** Đưa tất cả các cung vào $Q$. 
2. **Lặp:** Lấy một cung (x, c) ra khỏi $Q$. Gọi hàm `Revise(x, c)` để loại bỏ các giá trị không có hỗ trợ khỏi $D(x)$.
3. **Cập nhật:** Nếu $D(x)$ thay đổi (bị thu hẹp), tất cả các ràng buộc khác $c'$ liên quan đến $x$ (trừ $c$) phải được thêm lại vào $Q$ vì sự thay đổi của $D(x)$ có thể làm mất tính nhất quán của chúng.
4. **Kết thúc:** Khi $Q$ rỗng (đạt điểm bất động) hoặc miền trở nên rỗng (vô nghiệm).

Sự lan truyền này đảm bảo rằng các quyết định tại mỗi bước tìm kiếm được dựa trên thông tin cập nhật nhất, ngăn chặn sớm các nhánh tìm kiếm vô vọng. 

## 4. Chiến lược tìm kiếm (Search Strategies) và Heuristics

Lan truyền ràng buộc thường không đủ để tìm ra nghiệm duy nhất (trừ các bài toán tầm thường). Do đó, CP kết hợp lan truyền với một quy trình tìm kiếm có hệ thống (systematic search) để khám phá không gian trạng thái. 

### 4.1. Cấu trúc cây tìm kiếm và phân nhánh

Quá trinh giải quyết CSP có thể được hình dung như việc duyệt một cây tìm kiếm. Tại mỗi nút của cây (đại diện cho một trạng thái bài toán con), hai hoạt động chính diễn ra:
1. **Lan truyền (Propagate):** Chạy các thuật toán nhất quán để tỉa bớt các giá trị từ miền biến.
2. **Phân nhánh (Branch):** Nếu chưa tìm thấy nghiệm và chưa gặp mâu thuẫn, thuật toán sẽ chia bài toán hiện tại thành các bài toán con nhỏ hơn, tạo ra các nút con.


Các chiến lược phân nhánh (Branching Strategies) phổ biến bao gồm:
- **Gán nhãn (Enumeration/Labeling):** Chọn một biến $x$ và thử lần lượt từng giá trị $v \in D(x)$. Điều này tạo ra $d$ nhánh con, với $d = |D(x)|$.
- **Phân nhánh nhị phân (Binary Branching):** Chọn biến $x$ và giá trị $v$, tạo hai nhánh: nhánh trái gán $x = v$, nhánh phải gán $x \ne v$. Đây là chiến lược chuẩn trong nhiều bộ giải hiện đại vì nó giữ cho cây nhị phân, dễ quản lý.
- **Chia miền (Domain Splitting):** Phù hợp với miền giá trị lớn hoặc liên tục. Chọn giá trị $v$ (thường là điểm giữa), tạo hai nhánh $x \le v$ và $x > v$.


### 4.2. Heuristic chọn biến: Nguyên lý First-Fail

Thứ tự chọn biến để phân nhánh có ảnh hưởng quyết định đến kích thước của cây tìm kiếm. 
Nguyên lý chủ đạo trong CP là **First-Fail Principle** (Nguyên lý thất bại trước): _"Để thành công, hãy thử trước ở nơi bạn có khả năng thất bại cao nhất"._

- **Logic:** Nếu một nhánh dẫn đến vô nghiệm, ta muốn phát hiện điều này càng sớm càng tốt (fail fast) để quay lui, tránh lãng phí thời gian tìm kiếm sâu trong nhánh đó. 
- **Cài đặt:** Chiến lược **Dom** (Domain Size) chọn biến có miền giá trị nhỏ nhất hiện tại. Biến có ít lựa chọn nhất là biến "nguy hiểm" nhất, dễ gây ra mâu thuẫn nhất (bottle neck), do đó cần được xử lý trước. 
- **Biến thể nâng cao: Dom/Wdeg** (Domain over Weighted Degree) là một heuristic hiện đại hơn. Nó không chỉ xét kích thước miền mà còn xét đến lịch sử mâu thuẫn. 
Các biến tham gia các ràng buộc thường xuyên gây ra mâu thuẫn (trọng số cao) sẽ được ưu tiên chọn, giúp thuật toán tập trung vào phần "khó" nhất của bài toán. 

### 4.3. Heuristic chọn giá trị: Nguyên lý Best-First

Sau khi chọn biến, thứ tự thử các giá trị tuân theo nguyên lý Best-First. 
- **Logic:** Nếu bài toán có nghiệm, ta muốn đi thẳng đến nghiệm đó mà không phải quay lui.
- **Cài đặt:** Chọn giá trị có khả năng cao nhất thuộc về một nghiệm, hoặc giá trị ít gây ràng buộc nhất cho các biến còn lại (Least Constraining Value). 
Ví dụ, chọn giá trị để lại nhiều lựa chọn nhất cho các biến lân cận.

Bảng so sánh dưới đây tóm tắt sự khác biệt giữa các chiến lược tìm kiếm:

| Đặc điểm | Phương pháp Hệ thống (Systematic) | Phương pháp Không đầy đủ (Incomplete) |
|----------|-----------------------------------|---------------------------------------|
| Đại diện | Constraint Programming, Branch & Bound | Local Search, Genetic Algorithms, Greedy |
| Cách tiếp cận | Xây dựng dần lời giải (Constructive) | Sửa đổi lời giải đầy đủ (Perturbative) |
| Độ hoàn chỉnh | Đảm bảo tìm ra nghiệm tối ưu hoặc chứng minh vô nghiệm | Không đảm bảo tìm ra nghiệm tốt nhất |
| Chi phí | Cao (có thể bùng nổ tổ hợp nếu không có heuristic tốt) | Thấp hơn, dễ kiểm soát thời gian chạy |
| Ứng dụng | Bài toán cần độ chính xác tuyệt đối (lập lịch y tế, an toàn) | Bài toán quy mô cực lớn cần nghiệm "đủ tốt" nhanh |

### 4.4. Cơ chế Trailing và Backtracking
Khi một nhánh tìm kiếm dẫn đến mâu thuẫn (miền rỗng), thuật toán phải quay lui (backtrack). 
Để làm điều này hiệu quả, CP sử dụng cơ chế **Trailing**. Thay vì sao chép toàn bộ trạng thái dữ liệu tại mỗi nút (quá tốn bộ nhớ),
hệ thống chỉ ghi lại các thay đổi (ví dụ: "đã xoá giá trị 5 khỏi biến X tại độ sâu 3").  Khi quay lui từ độ sâu 3 về 2, hệ thống đọc nhật ký (trail) và hoàn tác (undo) các thao tác đó, khôi phục miền giá trị của X. Đây là yếu tố then chốt giúp CP thực hiện hàng triệu bước tìm kiếm mỗi giây.   


## 5. Ràng buộc toàn cục (Global Constraints): Động cơ suy diễn

Nếu biến và miền là khung xương, thì ràng buộc toàn cục chính là cơ bắp của CP. Một ràng buộc toàn cục gói gọn một cấu trúc tổ hợp phức tạp liên quan đến nhiều biến, 
cho phép bộ giải áp dụng các thuật toán lọc chuyên biệt mạnh mẽ hơn nhiều so với tập hợp các ràng buộc sơ cấp tương đương. 

### 5.1. Ràng buộc `AllDifferent`

Đây là ràng buộc toàn cục nổi tiếng và quan trọng nhất. `AllDifferent(x_1, \dots, x_n)` yêu cầu tất cả các biến phải nhận giá trị đôi một khác nhau. 
- **So sánh phân rã:** Ta có thể thay thế `AllDifferent` bằng $n(n-1)/2$ ràng buộc bất đẳng thức đôi $x_i \ne x_j$. Tuy nhiên, cách làm này làm mất đi khả năng nhìn nhận tổng thể (holistic view). Ví dụ, nếu $x_1, x_2, x_3$ đều có miền $\{1, 2\}$, các ràng buộc đôi sẽ không thấy vấn đề gì (vì mỗi cặp đều có thể khác nhau). Nhưng ràng buộc toàn cục sẽ phát hiện ra rằng ta có 3 biến nhưng chỉ có 2 giá trị ("chuồng bồ câu"), và báo mâu thuẫn ngay lập tức.
- **Thuật toán lọc:** Để đạt được nhất quán miền cho `AllDifferent`, CP sử dụng lý thuyết đồ thị, cụ thể là bài toán tìm bộ ghép cực đại trong đồ thị hai phía (Maximum Bipartite Matching). Thuật toán của Régin (1994) cho phép xác định các cạnh (giá trị) không thuộc bất kỳ bộ ghép nào và loại bỏ chúng với độ phức tạp đa thức, mang lại sức mạnh cắt tỉa vượt trội.


### 5.2. Các ràng buộc toàn cục khác

- **Global Cardinality Constraint (GCC):** Tổng quát hóa của `AllDifferent`, quy định số lần xuất hiện tối thiểu và tối đa của mỗi giá trị trong một tập biến. Ứng dụng trong xếp lịch nhân sự (mỗi người trực min 2 ca, max 5 ca).   
- **Circuit / Sub-circuit:** Buộc các biến tạo thành một chu trình Hamilton đi qua tất cả các nút. Đây là công cụ đắc lực cho các bài toán định tuyến xe (VRP) hay người du lịch (TSP).
- **Knapsack:** Mô hình hóa bài toán cái túi, giới hạn tổng trọng lượng của các món đồ được chọn. Nó sử dụng quy hoạch động hoặc lan truyền biên để lọc miền giá trị dựa trên khả năng lấp đầy túi.

## 6. Kỹ thuật mô hình hoá nâng cao
Mô hình hoá CP là nghệ thuật biến đổi bài toán thực tế thành ngôn ngữ mà bộ giải có thể hiểu và xử lý hiệu quả. 

### 6.1. Biến phụ (Auxiliary Variables)

Việc thêm các biến không xuất hiện trong đề bài gốc có thể làm đơn giản hóa mô hình và tăng cường lan truyền.

- **Ví dụ Cryptarithmetic (SEND + MORE = MONEY):** Bài toán yêu cầu tìm các chữ số cho các chữ cái sao cho phép cộng đúng. 
  * Mô hình ngây thơ: Viết một phương trình tổng lớn: $1000S + 100E + \dots = 10000M + \dots$. Mô hình này lan truyền rất kém vì sự phụ thuộc giữa các biến quá lỏng lẻo.
  * Mô hình biến nhớ (Carry): Thêm các biến nhớ $C_1, C_2, C_3, C_4 \in \{0, 1\}$ đại diện cho phần nhớ của phép cộng từng cột.$$D + E = Y + 10C_1$$$$C_1 + N + R = E + 10C_2$$...Mô hình này chia nhỏ bài toán thành các ràng buộc cục bộ nhỏ, giúp bộ giải lan truyền thông tin giữa các cột số cực kỳ nhanh chóng và hiệu quả.



### 6.2. Phá vỡ đối xứng (Symmetry Breaking)

Đối xứng là kẻ thù của tìm kiếm. Nếu bài toán có các nghiệm hoán vị (ví dụ: hai nhân viên có kỹ năng giống hệt nhau đổi chỗ cho nhau), không gian tìm kiếm sẽ phình to với các bản sao vô ích.

- **Giải pháp:** Thêm các "ràng buộc phá vỡ đối xứng" (symmetry-breaking constraints). 
Ví dụ, bắt buộc nhân viên A luôn được gán việc trước nhân viên B ($A \le B$), hoặc quân hậu ở hàng 1 phải nằm ở nửa trái bàn cờ. 
Điều này loại bỏ các nghiệm trùng lặp, chỉ giữ lại một đại diện duy nhất cho mỗi lớp đối xứng.


### 6.3. Ràng buộc dư thừa (Redundant Constraints)

Đây là các ràng buộc không thay đổi tập nghiệm của bài toán về mặt ngữ nghĩa (semantically redundant) nhưng giúp bộ giải phát hiện mâu thuẫn sớm hơn (computationally significant). 

* **Ví dụ:** Trong bài toán xếp hàng lên xe tải, ngoài các ràng buộc tải trọng từng xe, ta có thể thêm ràng buộc: "Tổng tải trọng các xe $\ge$ Tổng khối lượng hàng". 
Nếu tổng hàng lớn hơn tổng sức chứa đội xe, ràng buộc này sẽ gây mâu thuẫn ngay tại nút gốc, tránh việc thử xếp hàng vô ích.







