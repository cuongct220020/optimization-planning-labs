# Cơ sở lý thuyết và mô hình hoá toán học cho các bài toán tối ưu tổ hợp và thoả mãn ràng buộc

## 1. Giới thiệu: Bản chất của mô hình hoá

Mô hình hoá không đơn thuần là việc viết ra các phương trình; đó là nghệ thuật của sự trừu tượng hoá. Một mô hình tốt phải đảm bảo hai yếu tố (mô tả chính xác thực tế) và tính giải được (có thể xử lý bởi các thuật toán trong thời gian chấp nhận được).
Tài liệu giới thiệu một khung lý thuyết nền tảng dựa trên bộ tứ ($X, D, C, f$), trong đó:
* $X$: Tập hợp các biến quyết định (Variables).
* $D$: Miền giá trị của các biến (Domains).
* $C$: Tập hợp các ràng buộc (Constraints).
* $f$: Hàm mục tiêu (Objective function - chỉ áp dụng cho COP).

Sự phân biệt giữa CSP và COP là điểm khởi đầu quan trọng. Trong khi CSP tập trung vào tính khả thi (feasibility) - tìm kiếm một cấu hình thoả mãn mọi luật lệ, thì COP tiến xa hơn một bước bằng cách tìm kiếm cấu hình tốt nhất (optimality) dựa trên tiêu chí định lượng. 
Báo cáo này sẽ đi sâu phân tích từng lớp bài toán thông các ví dụ kinh điển như N-Queen, Sudoku, Phân công giảng dạy (Teacher Assignment), Phân bổ lớp học (Class Allocation) và Người du lịch (TSP), đồng thời tích hợp các kiến thức nâng cao về thuật toán Backtracking và phương pháp giải quyết hiện đại. 

## 2. Phân tích chuyên sâu về bài toán thoả mãn ràng buộc (CSP)

Bài toán thoả mãn ràng buộc (CSP) là nền tảng của trí tuệ nhân tạo biểu tượng và lập trình ràng buộc. 
Đặc trưng của CSP là không gian tìm kiếm rời rạc và sự bùng nổ tổ hợp (combinatorial explosion). 
Mục tiêu không phải là cực đại hóa lợi nhuận hay cực tiểu hóa chi phí, mà là tìm ra một trạng thái "hợp lệ" trong một biển các trạng thái "bất hợp lệ".

### 2.1. Bài toán xếp hậu (N-Queen Problem)

Bài toán N-Hậu yêu cầu đặt $N$ quân hậu lên bàn cờ kích thước $N \times N$ sao cho không quân nào tấn công quân nào. Đây là ví dụ kinh điển minh họa cho việc lựa chọn biến quyết định ảnh hưởng thế nào đến độ phức tạp của mô hình.

#### 2.1.1. Lựa chọn biến và không gian tìm kiếm

Cách tiếp cận ngây thơ nhất là sử dụng ma trận nhị phân $x_{ij}$ cho $N^2$ ô cờ. Tuy nhiên, tài liệu đề xuất một mô hình tinh gọn hơn nhiều dựa trên nhận định: "Mỗi cột chỉ có thể chứa duy nhất một quân hậu".

* **Biến quyết định (X):** $X = \{x_1, x_2,..., x_n\}$. Ở đây, $x_i$ đại điện cho chỉ số hàng của quân hậu nằm tại cột $i$.
* **Miền giá trị (D):** $D_i = \{1, 2,..., n\}$ với mọi $i$.

Sự chuyển đổi này giảm không gian tìm kiếm từ $2^{N^2}$ xuống còn $N^N$. Thêm vào đó, nếu ta ràng buộc các giá trị của $x_i$ phải đôi một khác nhau, không gian giảm xuống còn $N!$.

#### 2.1.2. Phân tích toán học của các ràng buộc

Sức mạnh của mô hình này nằm ở cách nó chuyển đổi các ràng buộc hình học (đường chéo) thành các bất đẳng thức số học.

1. **Ràng buộc hàng (Row Constraint):** Để đảm bảo không có hai quân hậu cùng hàng, giá trị của các biến phải khác nhau:
    $$x_i \neq x_j, \quad \forall 1 \le i < j \le n$$

Trong lý thuyết đồ thị, điều này tương đương với việc tìm một tập độc lập trên đồ thị đầy đủ hoặc bài toán tô màu đồ thị với $N$ màu cho $N$ đỉnh.

2. **Ràng buộc đường chéo (Diagonal Constraints):** Hai ô $(i, x_i)$ và $(j, x_j)$ nằm trên cùng một đường chéo khi và chỉ khi khoảng cách giữa các hàng bằng khoảng cách giữa các cột: $|x_i - x_j| = |i - j|$. Điều này dẫn đến hai hệ quả toán học đuợc liệt kê trong tài liệu.
   * **Đường chéo chính (Main Diagonal):** $x_i - x_j = i - j \implies x_i - i = x_j - j$. Do đó, ràng buộc là:
        $$x_i - i \neq x_j - j$$
   * **Đường chéo phụ (Anti-Diagonal):** $x_i - x_j = -(i - j) \implies x_i + i = x_j + j$. Do đó, ràng buộc là:
      $$x_i + i \neq x_j + j$$

**Nhận định chuyên sâu:** Việc biến đổi này cho phép kiểm tra tính hợp lệ trong thời gian O(1) cho mỗi cặp, thay vì phải quét lại toàn bộ bàn cờ. Trong lập trình ràng buộc hiện đại, các hệ thức này thường được gói gọn trong ràng buộc toàn cục `AllDifferent` áp dụng cho ba tập hợp: tập giá trị $\{x_i\}$, tập hiệu $\{x_i - i\}$, và tập tổng $\{x_i + i\}$.

### 2.2. Bài toán Sudoku: Sự mở rộng của logic ràng buộc

Sudoku là một bước tiến phức tạp hơn của CSP, nơi các ràng buộc chồng chéo lên nhau theo nhiều chiều kích: hàng, cột, và khối con (subgrid).

#### 2.2.1. Mô hình hoá biến và miền giá trị
* **Biến (X):** $x_{ij}$ là giá trị tại hàng $i$, cột $j$ ($1 \le i, j \le 9$).
* **Miền giá trị (D):** $D(x_{ij}) = \{1,..., 9\}$. Đối với các ô đã điền sẵn số k. Đối với các ô đã điền sẵn số $k$, miền giá trị bị thu hẹp thành {$k$}.

#### 2.2.2. Cấu trúc ràng buộc "All-Different"

Mô hình Sudoku được xây dựng hoàn toàn dựa trên nguyên lý "đôi một khác nhau" (pairwise distinct):

| Loại ràng buộc | Công thức toán học | Ý nghĩa |
|----------------|--------------------|---------|
| Cột            | $x_{i_1,j} \neq x_{i_2,j}, \forall 1 \le i_1 < i_2 \le 9$ | Các số trong cùng một cột không được trùng nhau. |
| Hàng           | $x_{i,j_1} \neq x_{i,j_2}, \forall 1 \le j_1 < j_2 \le 9$ | Các số trong cùng một hàng không được trùng nhau. |
| Khối 3 × 3     | $x_{3i+i_1,3j+j_1} \neq x_{3i+i_2,3j+j_2}$ | Các số trong cùng một khối con không được trùng nhau. |

**Phân tích Chi tiết về Ràng buộc Khối Con:** Công thức cho khối con trong slide 1 sử dụng kỹ thuật chỉ số hóa (indexing) thông minh. Bằng cách sử dụng $i, j \in \{0, 1, 2\}$ để chỉ định tọa độ của khối lớn, và $i_1, i_2, j_1, j_2 \in \{1, 2, 3\}$ để chỉ định tọa độ cục bộ trong khối, ta có thể quét qua toàn bộ 9 khối một cách hệ thống.Điều này minh chứng cho tầm quan trọng của việc biểu diễn dữ liệu (data representation) trong mô hình hóa. Một biểu diễn chỉ số tốt sẽ giúp việc viết các vòng lặp tạo ràng buộc trong code trở nên đơn giản và ít lỗi hơn.

### 3. Phân tích chuyên sâu về bái toán tối ưu tổ hợp (COP)

Khi chuyển từ CSP sang COP, chúng ta giới thiệu thêm hàm mục tiêu $f$. Đây là thước đo định lượng cho "chất lượng" của giải pháp. 
Các bài toán được trình bày trong slide tập trung vào hai lớp bài toán kinh điển trong vận trù học (operation research): Phân công nguồn lực (Resource Allocation) và Định tuyến (Routing).


#### 3.1. Bài toán phân công giảng dạy cân bằng (Balanced Class Teacher Assignment)

Đây là biến thể của bài toán **Generalized Assignment Problem (GAP)** với mục tiêu **Minimax**. Vấn đề thực tế đặt ra là: Đã có thời khoá biểu (lớp này học giờ nào), cần phân giáo viên vào lớp sao cho không ai bị quá tải.

#### 3.1.1. Dự liệu đầu vào và cấu trúc tập hợp
Để mô hình hoá chính xác, ta cần định nghĩa rõ ràng các tham số đầu vào (parameters):
* Tập hợp lớp học $S = {1,...,n}$.
* Tập hợp giáo viên $T = {1,...,m}$.
* Trọng số $c(i)$: Số tín chỉ (tải lượng công việc) của lớp $i$.
* Danh sách xung đột $Q$: Tập hợp các cặp lớp $(i, j)$ được xếp lịch học cùng giờ. Đây là ràng buộc cứng về thời gian.
* Danh sách năng lực $T_i$: Tập hợp các giáo viên có chuyên môn để dạy lớp $i$.

Ví dụ Minh họa từ Tài liệu : Bảng dưới đây tóm tắt dữ liệu về số tín chỉ cho 13 lớp học (0-12) được trích xuất từ slide 9:   

| Lớp (Class) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|-------------|---|---|---|---|---|---|---|---|---|---|----|----|----|
| Tín chỉ     | 3 | 3 | 4 | 3 | 4 | 3 | 3 | 3 | 4 | 4 | 3  | 4  | 4  |


#### 3.1.2. Biến quyết định và kỹ thuật tuyến tính hoá Minimax
Mô hình sử dụng biến nhị phân $x_{ij}$ để biểu diễn sự gán ghép:
* $x_{ij} = 1$ nếu giáo viên $j$ dạy lớp $i$.
* $x_{ij} = 0$ nếu ngược lại.

Mục tiêu là "Cực tiểu hoá tải lượng lớn nhất" (Minimize the maximum load). Hàm mục tiêu dạng $\min (\max_j (\sum_i c(i)x_{ij}))$ là phi tuyến lồi. Để giải quyết bằng quy hoạch tuyến tính nguyên (MILP),
ta sử dụng beiens phụ trợ:
* Gọi biến nguyên `maxcredit` là tải trọng tối đa.
* Đặt ràng buộc: Tổng tải của mỗi giáo viên phải nhỏ hơn hoặc bằng `maxcredit`.
* Hàm mục tiêu trở thành: `Minimize maxcredit`. 

#### 3.1.3. Phân tích hệ thống ràng buộc
1. **Ràng buộc phân hoạch (Partitioning Constraint):** Mỗi lớp phải có chính xác một giáo viên dạy.

    $$\sum_{j \in T_i} x_{ij} = 1, \quad \forall i \in S$$

Việc tổng chạy trên  $j \in T_i$ (thay vì toàn bộ $T$) đã khéo léo tích hợp ràng buộc năng lực vào mô hình, giúp giảm số lượng biến số bằng 0 không cần thiết. 

2. **Ràng buộc xung đột (Conflict Clique Constriants):** Nếu hai lớp $i_1$ và $i_2$ học cùng giờ (thuộc tập $Q$), một giáo viên không thể dạy cả hai.

    $$x_{i_1 j} + x_{i_2 j} \le 1, \quad \forall j \in T, \forall (i_1, i_2) \in Q$$

Tại sao là $\le 1$? Vì giáo viên $j$ có thể không dạy lớp nào trong hai lớp đó ($0+0=0$), hoặc dạy một lớp ($1+0=1$). Họ tuyệt đối không thể dạy cả hai ($1+1=2 > 1$). Đây là cách toán học biểu diễn sự loại trừ lẫn nhau (mutual exclusion).

3. **Ràng buộc Tải trọng (Load Constraints):**

    $$\sum_{i \in S} c(i) x_{ij} \le \text{maxcredit}, \quad \forall j \in T$$

Ràng buộc này liên kết các biến nhị phân $x_{ij}$ với biến nguyên liên tục `maxcredit`, tạo thành cơ chế cân bằng tải. 
Khi solver cố gắng giảm `maxcredit` (theo hàm mục tiêu), nó buộc phải san sẻ các lớp có tin chỉ cao (như lớp 2, 4, 8, 9, 11, 12 có 4 tín chỉ) đều cho các giáo viên. 

**Kết quả phân công mẫu (Slide 10):** Mô hình đã tạo ra một phân công tối ưu với độ cân bằng tải rất cao:
* **Giáo viên 0:** 15 tín chỉ.
* **Giáo viên 1:** 15 tín chỉ.
* **Giáo viên 2:** 14 tín chỉ. Sự chênh lệch chỉ là 1 tín chỉ, chứng tỏ hiệu quả của mô hình Minimax trong việc đảm bảo công bằng. 

### 3.2. Bài toán phân bổ lớp học (Class Allocation Problem)

Khác với bài toán gán giáo viên (người - việc), bài toán này gán lớp học vào các học kỳ (việc - thời gian). Đây là bài toán lập lịch (Scheduling) với các ràng buộc về thứ tự (Precedence) và tài nguyên (Knapsack constraints).

#### 3.2.1. Cấu trúc dữ liệu và tham số
* Tập lớp $C$ và tập học kỳ $S$.
* Cân bằng số giới hạn:
  * $[\alpha, \beta]$: Số lượng lớp tối thiểu/tối đa trong một kỳ.
  * $[\delta, \gamma]$: Số tín chỉ tối thiểu/tối đa trong một kỳ.
* Tập tiên quyết $Q$: $(i, k) \in Q$ nghĩa là lớp $i$ phải học trước lớp $k$.


#### 3.2.2. Cơ chế ràng buộc thứ tự

Điểm đặc sắc nhất của mô hình này nằm ở cách biểu diễn khái niệm "trước - sau" bằng đại số tuyến tính.
* Biến $x_{ij} = 1$ nếu lớp $i$ được gán vào học kỳ $j$.
* Học kỳ của lớp $i$ được tính bằng biểu thức: $\sum_{j \in S} j \cdot x_{ij}$.
  * Vì $x_{ij}$ chỉ bằng 1 tại đúng một học kỳ $j^*$, tổng này sẽ trả về giá trị $j^*$.

Ràng buộc tiên quyết cho cặp $(i_1, i_2) \in Q$:
    $$\sum_{j \in S} j \cdot x_{i_1 j} < \sum_{j \in S} j \cdot x_{i_2 j}$$

**Phân tích sâu:** Trong các bộ giải quy hoạch nguyên (IP Solvers), bất đẳng thức ngặt (<) thường không được hỗ trợ trực tiếp. Ta phải chuyển đổi thành dạng $\le$ bằng cách cộng thêm 1 vào vế trái (vì học kỳ là số nguyên):
    $$\sum_{j \in S} j \cdot x_{i_1 j} + 1 \le \sum_{j \in S} j \cdot x_{i_2 j}$$

Điều này đảm bảo lớp $i_2$ phải học ít nhất là ở học kỳ ngay sau lớp $i_1$.

#### 3.2.3. Ràng buộc dung lượng (Capacity Constraints)

Mô hình áp dụng hai tầng ràng buộc dung lượng cho mỗi "thùng chứa" (học kỳ):

1. **Số lượng lớp (Cardinality):** $\alpha \le \sum_{i \in C} x_{ij} \le \beta$. Đảm bảo sinh viên không học quá ít hoặc quá nhiều môn.
2. **Khối lượng kiến thức (Weighted Sum):** $\delta \le \sum_{i \in C} c(i) x_{ij} \le \gamma$. Đảm bảo khối lượng tín chỉ nằm trong ngưỡng cho phép của quy chế đào tạo.

### 3.3. Bài toán người đi du lịch (Traveling Salesman Problem - TSP)

TSP là "trái tim" của tối ưu hoá tổ hợp. Thách thức lớn nhất của TSP không phải là tính độ dài đường đi, mà là đảm bảo đường đi tạo thành một chu trình đơn duy nhất đi qua tất cả các thành phố (Hamiltonian Cycle) mà không bị vỡ thành các chu trình con rời rạc (Subtours).

#### 3.3.1. Mô hình biến và ràng buộc bậc (Degree Constraints)
* Biến  $x_{ij} \in \{0, 1\}$: Đi từ $i$ đến $j$.
* Hàm mục tiêu: $\min \sum c_{ij} x_{ij}$.

Hai ràng buộc đầu tiên định hình nên một bài toán gán (Assignment Problem):
1. Đến mỗi thành phố đúng một lần: $\sum_j x_{ij} = 1$.
2. Rời khỏi thành phố đúng một lần:  $\sum_i x_{ij} = 1$.

Tuy nhiên, nếu chỉ có 2 ràng buộc này, kết quả có thể là tập hợp các chu trình con (ví dụ: chu trình 1-2-3-1 và 4-5-6-4). Đây là lời giải hợp lệ cho bài toán Gán, nhưng vô nghĩa với TSP.

#### 3.3.2. Ràng buộc loại bỏ chu trình con (Subtour Elimination Constraints - SEC)

Tài liệu  trình bày công thức DFJ (Dantzig-Fulkerson-Johnson), phương pháp mạnh mẽ nhất nhưng cũng đắt đỏ nhất về mặt tính toán để loại bỏ chu trình con.

$$\sum_{i, j \in S, i \neq j} x_{ij} \le |S| - 1, \quad \forall S \subset \{1,..., n\}, S \neq \emptyset, S \neq V$$

**Cơ chế hoạt động:**
- Xét một tập con các thành phố S (ví dụ:  $\{1, 2, 3\}$).
- Nếu có một chu trình kín bên trong S (như 1-2-3-1), tổng sso cạnh nối đỉnh trong S sẽ bằng đúng số đỉnh $|S| = 3$.
- Ràng buộc yêu cầu tổng số cạnh nội bộ chỉ được tối đa là $|S| - 1 = 2$.
- Do đó, chu trình kín bị cấm. Đường đi buộc phải "vỡ" ra và kết nối với các thành phố bên ngoài tập $S$.

**Vấn đề độ phức tạp:** Số lượng tập con S là $2^n - 2$. Với $n=20$, ta có hơn 1 triệu ràng buộc. Với $n=50$, con số này vượt quá khả năng xử lý của máy tính.

- **Giải pháp thực tế (Lazy Constraints):** Các bộ giải hiện đại (như Gurobi, CPLEX) không thêm tất cả ràng buộc này từ đầu. Họ giải bài toán chỉ với ràng buộc bậc. Nếu phát hiện chu trình con trong nghiệm, họ mới thêm đúng ràng buộc SEC vi phạm vào và giải lại. Đây là kỹ thuật "Row Generation" hay "Cutting Planes".


## 4. Thuật toán Backtracking: Cầu nối giữa mô hình và lời giải

Sau khi xây dựng mô hình $(X, D, C)$, ta cần một thuật toán để tìm kiếm nghiệm. Backtracking (Quay lui) là thuật toán tổng quát được giới thiệu trong slide để giải quyết cả CSP và COP.

### 4.1. Nguyên lý hoạt động

Backtracking thực chất là quá trình duyệt cây tìm kiếm theo chiều sâu (DFS). Nó xây dựng lời giải từng bước (incrementally). Tại mỗi bước $k$, nó thử gán một giá trị cho biến $x_k$.
* Nếu việc gán không vi phạm ràng buộc nào (hàm check(v,k) trả về TRUE), nó đệ quy sang bước $k+1$.
* Nếu vi phạm, hoặc nếu đi đến bước tiếp theo mà không tìm thấy lời giải, nó "quay lui" (backtracks), hủy bỏ phép gán hiện tại và thử giá trị khác.


### 4.2. Cấu trúc mã giả và phân tích

Đoạn mã giả `TRY(k)` trong slide  là khuôn mẫu chuẩn mực:

```
TRY(k)
Begin
  Foreach v in D_k (Miền giá trị của biến k)
    If check(v, k) Then  // Kiểm tra tính khả thi cục bộ
      x[k] = v;          // Ghi nhận quyết định
      Update(Datastruct); // Lan truyền ràng buộc (Forward Checking)
      
      If k == n Then
        Record_Solution(); // Tìm thấy nghiệm
      Else
        TRY(k+1);        // Đệ quy
        
      Restore(Datastruct); // Quay lui: Hoàn tác trạng thái
    EndIf
  EndForeach
End
```

**Phân tích kĩ thuật:**
1. **Hàm `check(v, k)`:** Đây là nơi các ràng buộc mô hình hóa ở phần trên được thực thi. Đối với N-Queen, nó kiểm tra các đường chéo. Đối với TSP, nó kiểm tra xem thành phố $v$ đã được thăm chưa.
2. **Cắt tỉa (Pruning):** Dòng `If check(v, k)` đóng vai trò cực kỳ quan trọng. Nó giúp cắt bỏ toàn bộ nhánh cây tìm kiếm xuất phát từ một quyết định sai lầm, giúp thuật toán nhanh hơn nhiều so với duyệt toàn bộ (Brute-force).   

## 5. Tổng kết và khuyến nghị

Việc mô hình hoá các bài toán tối ưu là một quá trình tịnh tiến từ tư duy định tính sang định lượng. Từ các ví dụ trong tài liệu, ta rút ra các nguyên tắc cốt lõi:
1. **Chuyển đổi hình học sang số học:** Như trong N-Queen, việc biến đổi quan hệ không gian thành quan hệ chỉ số giúp đơn giản hoá mô hình.
2. **Tuyến tính hoá mục tiêu phức tạp:** : Kỹ thuật Minimax trong bài toán Phân công giáo viên cho thấy cách xử lý các mục tiêu công bằng bằng biến phụ trợ.
3. **Xử lý Logic Thời gian:** Sử dụng tổng có trọng số ($\sum j \cdot x_{ij}$) để biểu diễn thời gian trong bài toán Phân bổ lớp học.
4. **Xử lý Cấu trúc Đồ thị:** Sử dụng ràng buộc tập con để đảm bảo tính liên thông trong TSP, mặc dù phải trả giá bằng độ phức tạp tính toán.

Các mô hình toán học này không chỉ là bài tập lý thuyết mà là nền tảng của các hệ thống lập lịch, logistics và quản lý nguồn lực trong thực tế. 
Việc hiểu sâu sắc cấu trúc biến và ràng buộc cho phép ta lựa chọn công cụ giải (Solver) phù hợp, từ CP (Constraint Programming) cho Sudoku đến MILP cho Phân công giáo viên và TSP.