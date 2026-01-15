# Báo cáo chuyên khảo: Cơ sở lý thuyết, thuật toán và ứng dụng thực tiễn của Quy hoạch tuyến tính

## 1. Tổng quan về tối ưu hoá và quy hoạch tuyến tính

**Quy hoạch tuyến tính (Linear Programming - LP)** không chỉ đơn thuần là một công cụ toán học, mà là nền tảng cốt lõi của lý thuyết tối ưu hoá hiện đại, đóng vai trò then chốt trong việc ra quyết định khoa học trong các lĩnh vực từ quản trị chuỗi cung ứng, tài chính, đến quy hoạch năng lượng và y tế. 
Dựa trên tài liệu nghiên cứu được cung cấp, báo cáo này sẽ phân tích sâu sắc cấu trúc lý thuyết, cơ chế hình học và các thuật toán đại số (Simplex và Two-Phase Simplex), đồng thời hướng dẫn triển khai tính toán thực tế thông qua thư viện Or-Tools của Google. 

### 1.1. Bản chất của bài toán tối ưu hoá

Trong bối cảnh khan hiếm nguồn lực, mọi tổ chức đều đối mặt với bài toán kinh tế cơ bản: làm thế nào để phân bổ các nguồn lực giới hạn (nhân lực, nguyên vật liệu, thời gian, vốn) nhằm đạt được hiệu quả cao nhất (tối đa hoá lợi nhuận hoặc tối thiểu hoá chi phí). 
Quy hoạch tuyến tính là phương pháp mô hình hoá các vấn đề này dưới dạng các biểu thức toán học bậc nhất. Thuật ngữ "Linear" (tuyến tính) ám chỉ hai giả định kinh tế quan trọng:

1. **Tính tỷ lệ (Proportionality):** Đóng góp của một hoạt động vào hàm mục tiêu hoặc mức tiêu thụ nguồn lực tỷ lệ thuận trực tiếp với quy mô của hoạt động đó. Không có hiệu ứng quy mô (economies of scale) phi tuyến tính trong mô hình LP cơ bản. 
2. **Tính cộng (Additivity):** Tổng giá trị của hàm mục tiêu và tổng nguồn lực sử dụng bằng tổng của các thành phần riêng lẻ. Điều này loại trừ các tương tác phức tạp (synergy) giữa các biến số.


### 1.2. Ứng dụng thực tiễn trong công nghiệp và xã hội

Trước khi đi sâu vào toán học, cần nhận thức rõ tầm quan trọng của LP thông qua các ứng dụng thực tế được ghi nhận trong tài liệu nghiên cứu:
* **Lập lịch trình hàng không:** Các hãng hàng không sử dụng LP để giải quyết bài toán lập lình trình bay cực kỳ phức tạp, bao gồm việc gán máy bay cho các chặng bay và sắp xếp phi hành đoàn. Mục tiêu là tối thiểu hoá chi phí nhiên liệu và nhân sự trong khi phải tuân thủ hàng nghìn ràng buộc về bảo dưỡng máy bay, quy định nghi ngơi của phi công và sức chứa máy bay. Một mô hình như vậy có thể chứa hàng nghìn biến số và ràng buộc. 
* **Quy hoạch sản xuất và hỗn hợp sản phẩm:** Trong sản xuất, LP giúp xác định số lượng tối ưu của từng loại sản phẩm cần sản xuất để tối đa hoá lợi nhuận, dựa trên giới hạn về nguyên liệu thô và giờ máy. Ví dụ, một nhà máy nội thất cần quyết định số lượng bàn và ghế sản xuất từ lượng gỗ giới hạn. 
* **Tối ưu hoá khẩu phần ăn (The Diet Problem):** Một trong những ứng dụng kinh điển nhất là xác định chế độ ăn uống đáp ứng đủ các yêu cầu dinh dưỡng (calo, vitamin, protein) với chi phí thấp nhất. Đây là nền tảng cho các bài toán pha trộn nguyên liệu trong công nghệ thực phẩm và chăn nuôi.
* **Phân phối năng lượng:** Các công ty tiện ích áp dụng LP để điều phối việc phát điện từ các nguồn khác nhau (thuỷ điện, nhiệt điện, năng lượng tái tạo) nhằm đáp ứng nhu cầu tiêu thụ biến động theo thời gian thực với chi phí vận hành thấp nhất, đồng thời tuân thủ các ràng buộc về môi trường và công suất truyền tải. 

## 2. Mô hình hoá Toán học và Dạng chuẩn (Standard Form)

Để giải quyết một bài toán thực tế bằng thuật toán Simplex, trước hết ta phải chuyển đổi các mô tả bằng lời văn thành một mô hình toán học chuẩn hoá. Tài liệu nhấn mạnh tầm quan trọng của việc đưa bài toán về **Dạng chuẩn (Standard Form)** để đảm bảo tính nhất quán trong xử lý thuật toán.

### 2.1. Cấu trúc dạng chuẩn

Theo định nghĩa trong tài liệu, một bài toán quy hoạch tuyến tính ở dạng chuẩn phải thoả mãn ba điều kiện tiên quyết:

1. Hàm mục tiêu phải là cực đại hoá (Maximization):

    $$f(x) = c_{1}x_{1} + c_{2}x_{2} +... + c_{n}x_{n} \rightarrow \max$$

2. Các ràng buộc phải ở dạng bất đẳng thức "nhỏ hơn hoặc bằng" ($\le$):
    $$a_{i,1}x_{1} + a_{i,2}x_{2} +... + a_{i,n}x_{n} \le b_{i}$$

    với $i = 1,..., m$.
3. Các biến quyết định không âm:
    $$x_{j} \ge 0$$
    
    với mọi $j = 1,..., n$.

Trong đó:
* $x_j$ là các biến quyết định (ví dụ: số lượng sản phẩm cần làm).
* $c_j$ là hệ số của hàm mục tiêu (ví dụ: lợi nhuận trên mỗi đơn vị).
* $b_i$ là giới hạn nguồn lực (RHS - Right Hand Side).
* $a_{i,j}$ là hệ số công nghệ, biểu thị lượng tài nguyên $i$ cần để sản xuất một đơn vị $j$.

### 2.2. Các kỹ thuật chuyển đổi về dạng chuẩn

Thực tế, các bài toán thường xuất hiện ở dạng tổng quát (General Form) với các yêu cầu tối thiểu hoá (Minimization), ràng buộc lớn hơn hoặc bằng ($\ge$), ràng buộc đẳng thức ($=$), hoặc biến tự do (không bị ràng buộc dấu). 
Tài liệu cung cấp quy tắc chuyển đổi đại số nghiêm ngặt để xử lý các trường hợp ngoại lệ này:

#### 2.2.1. Chuyển đổi hàm mục tiêu

Nếu bài toán yêu cầu tối thiểu hoá một hàm chi phí  $f(x)$, về mặt toán học, điều này tương đương với việc tối đa hoá giá trị âm của hàm đó. Khi tìm được điểm cực trị, giá trị biến $x$ là như nhau, ta chỉ cần đổi dấu giá trị mục tiêu cuối cùng.

$$f(x) \rightarrow \min \Leftrightarrow -f(x) \rightarrow \max$$

#### 2.2.2. Chuyển đổi ràng buộc

Thuật toán Simplex nguyên thuỷ (Primal Simplex) thường được thiết kế để xử lý các bất đẳng thức dạng $\le$ (tương ứng với việc sử dụng nguồn lực có sẵn).

* **Xử lý bất đẳng thức $\ge$:** Nếu có ràng buộc $g(x) \ge b$, ta nhân cả hai về với $-1$ để đảo chiều bất đẳng thức:
    $$g(x) \ge b \iff -g(x) \le -b$$

    Ví dụ: $2x_1 + 3x_2 \ge 10$ trở thành $-2x_1 - 3x_2 \le -10$.
* **Xử lý đẳng thức ($=$):** Một phương trình $A = B$ có tính chất ràng buộc chặt chẽ hơn bất đẳng thức. Về mặt logic, $A = B$ đồng nghĩa với việc $A$ vừa không được lớn hơn $B$, vừa không được nhỏ hơn $B$. Do đó, ta có thể tác một đẳng thức thành hai bất đẳng thức ngược chiều nhau: 
    $$A = B \iff \begin{cases} A \le B \\ A \ge B \end{cases} \iff \begin{cases} A \le B \\ -A \le -B \end{cases}$$

#### 2.2.3. Xử lý biến tự do (Unrestricted Variables)

Trong một số mô hình tài chính hoặc vật lý, biến số có thể nhận giá trị âm (ví dụ: dòng tiền ròng, nhiệt độ). Tuy nhiên, thuật toán Simplex yêu cầu biến phải không âm để đảm bảo tính khả thi hình học trong góc phần tư thứ nhất. Để giải quyết, ta biểu diễn biến tự do $x_j$ thành hiệu của hai biến không âm:
    $$x_{j} = x_{j}^{+} - x_{j}^{-}$$

với $x_{j}^{+}, x_{j}^{-} \ge 0$.
* Nếu $x_j$ dương, $x_{j}^{+}$ nhận giá trị đó và $x_{j}^{-} = 0$.
* Nếu $x_j$ âm, $x_{j}^{-}$ nhận giá trị tuyệt đối và $x_{j}^{+} = 0$. Kỹ thuật này cho phép thuật toán làm việc hoàn toàn trong miền không âm mà vẫn bao quát được toàn bộ trục số thực.

### 2.3. Phân tích ví dụ minh hoạ chuyển đổi

Xem xét ví dụ cụ thể từ Slide 7 để minh họa quá trình này. Bài toán gốc:
    $$f(x_1, x_2) = 3x_1 + 2x_2 \rightarrow \min$$

Thoả mãn:
1. $2x_1 + x_2 \le 7$
2. $x_1 + 2x_2 = 8$
3. $x_1 - x_2 \ge 2$
4. $x_1, x_2 \in \mathbb{R}$ (Biến tự do), $x_2 \ge 0$ (Chỉ $x_1$ là tự do).

Quá trình chuyển đổi:
1. **Hàm mục tiêu:** Chuyển Min thành Max. $Z' = -3x_1 - 2x_2 \rightarrow \max$.
2. **Biến số:** Thay $x_1 = x_1^+ - x_1^-$. Hàm mục tiêu trở thành: $-3(x_1^+ - x_1^-) - 2x_2 = -3x_1^+ + 3x_1^- - 2x_2$.
3. **Ràng buộc 1:** $2(x_1^+ - x_1^-) + x_2 \le 7 \Rightarrow 2x_1^+ - 2x_1^- + x_2 \le 7$.
4. **Ràng buộc 2:** $x_1 + 2x_2 = 8$ tách thành:
   * $x_1^+ - x_1^- + 2x_2 \le 8$
   * $-(x_1^+ - x_1^- + 2x_2) \le -8 \Rightarrow -x_1^+ + x_1^- - 2x_2 \le -8$.
5. **Ràng buộc 3:** $x_1 - x_2 \ge 2 \Rightarrow -(x_1 - x_2) \le -2$. Thay biến: $-x_1^+ + x_1^- + x_2 \le -2$.

Kết quả cuối cùng là một hệ thống nhất quán, sẵn sàng cho việc áp dụng các thuật toán giải tích ma trận.

## 3. Cách tiếp cận hình học (Geometric Approach)

Trước khi đi vào thuật toán đại số phức tạp, việc hiểu biết bản chất hình học của LP là cực kỳ quan trọng. 
Cách tiếp cận hình học cung cấp trực giác "tại sao" lời giải tối ưu lại nằm ở nơi nó nằm. 

### 3.1. Miền khả thi và đa diện lồi

Trong không gian hai chiều (với 2 biến $x_1$, $x_2$), mỗi bất đẳng thức tuyến tính $ax_1 + bx_2 \le c$ xác định một **nửa mặt phẳng (half-plane)**. Đường thẳng $ax_1 + bx_2 = c$ là biên giới, và vùng thoả mãn nằm ở một phía của đường thẳng đó. Giao điểm của tất cả các nửa mặt phẳng này tạo thành **Miền khả thi (Feasible Region).**
* Miền này luôn là một **Đa giác** (trong 2D) hoặc **Đa diện** (Polytope - trong n chiều).
* Tính chất quan trọng nhất của miền này là **Tính Lồi (Convexity)**. Điều này có nghĩa là nếu ta lấy hai điểm bất kỳ nằm trong miền khả thi và nối chúng lại bằng một đoạn thẳng, thì toàn bộ đoạn thẳng đó cũng nằm trọng vẹn trong miền khả thi. Tính chất này đảm bảo rằng trong quy hoạch tuyến tính, mọi cực trị địa phương (local optimum) cũng chính là cực trị toàn cục (global optimum).

### 3.2. Định lý cơ bản của Quy hoạch tuyến tính

Hàm mục tiêu $Z = c_1x_1 + c_2x_2$ có thể được hình dung như một mặt phẳng (hoặc đường thẳng trong 2D) di chuyển trên đồ thị. Khi ta muốn tối đa hoá Z, ta "đẩy" đường thẳng này đi xa nhất có thể theo hướng của vector pháp tuyến ($c_1, c_2$). Định lý cơ bản phát biểu rằng: **Nếu bài toán quy hoạch tuyến tính có phương án tối ưu, thì phương án đó phải nằm tại ít nhất một điểm cực biên (đỉnh/corner point) của miền khả thi.** Lý do là vì hàm mục tiêu tuyến tính không có độ cong; nó tăng liên tục cho đến khi bị chặn lại bởi biên của đa giác. Điểm xa nhất về một hướng trên một đa giác lồi luôn là một đỉnh (hoặc một cạnh nối hai đỉnh nếu đường mức song song với cạnh đó).


### 3.3. Phân tích ví dụ hình học

Xét ví dụ trong Slide 11-13: Maximize $Z = 3x_1 + 2x_2$. Thỏa mãn:

1. $2x_1 + x_2 \le 7$
2. $x_1 + 2x_2 \le 8$
3. $x_1 - x_2 \le 2$
4. $x_1, x_2 \ge 0$

**Xây dựng đồ thị:** Ta vẽ các đường thẳng biên tương ứng với các bất đẳng thức:

* Đường (1) đi qua (0,7) và (3.5,0). Vùng khả thi nằm dưới đường này.
* Đường (2) đi qua (0,4) và (8,0). Vùng khả thi nằm dưới. 


## 4. Phương pháp Simplex: Cỗ máy đại số (Algebraic Engine)

Phương pháp Simplex, phát triển bởi George Dantzig, thực chất là việc dịch chuyển "thông minh" từ đỉnh này sang đỉnh khác của đa diện lồi trong không gian n-chiều. 
Thay vì vẽ hình, Simplex sử dụng các phép biến đổi sơ cấp trên ma trận để "nhảy" giữa các đỉnh sao cho giá trị hàm mục tiêu luôn tăng lên. 

### 4.1. Chuyển đổi sang dạng phương trình (Equational Form)

Để giải hệ phương trình bằng đại số ma trận, ta không thể làm việc với bất đẳng thức. Ta cần chuyển chúng thành đẳng thức bằng cách sử dụng **Biến bù (Slack Variables).** Với một ràng buộc $2x_1 + x_2 \le 7$, 
điều này có nghĩa là tổng tài nguyên sử dụng ($2x_1 + x_2$) cộng với một lượng chưa dùng hết (biến bù $x_3$) phải đúng bằng 7.
    $$2x_1 + x_2 + x_3 = 7$$

Biến bù $x_3$ phải không âm ($x_3 \ge 0$). Nếu $x_3 = 0$, nghĩa là tài nguyên đã được dùng hết (ràng buộc chặt). Nếu $x_3 > 0$, tài nguyên còn dư. 

Hệ phương trình từ ví dụ trên được viết lại như sau (Slide 19):

$$Z - 3x_1 - 2x_2 = 0 \quad (\text{Hàm mục tiêu})$$ 

$$2x_1 + x_2 + x_3 = 7$$

$$x_1 + 2x_2 + x_4 = 8$$

$$x_1 - x_2 + x_5 = 2$$

Ở đây $x_3, x_4, x_5$ là các biến bù tương ứng cho 3 ràng buộc.

### 4.2. Khái niệm phương án cực biên (Basic Feasible Solution - BFS)

Trong hệ phương trình này, ta có 5 biến ($x_1$ đến $x_5$) nhưng chỉ có 3 phương trình ràng buộc. 
Hệ này có vô số nghiệm. Để tìm một nghiệm duy nhất tương ứng với một "đỉnh" (hình học), ta áp dụng nguyên tắc cơ sở:

* Chọn $n - m$ (ở đây là $5 - 3 = 2$ biến) và gán giá trị của chúng bằng 0. Nhưng biến này gọi là **Biến phi cơ sở (Non-basic Variables).**
* Giải hệ phương trình để tìm giá trị của $m$ biến còn lại. Những biến này gọi là **Biến cơ sở (Basic Variables).**
* Nếu tất cả các biến cơ sở đều  $\ge 0$, nghiệm đó gọi là **Phương án Cực biên (BFS)**.

**BFS Ban đầu:** Cách đơn giản nhất để bắt đầu là cho các biến quyết định ban đầu ($x_1, x_2$) bằng 0. Khi đó $x_1 = 0, x_2 = 0$ (Non-basic)
$\Rightarrow x_3 = 7, x_4 = 8, x_5 = 2$ (Basic). Nghiệm này tương ứng với gốc tọa độ O(0,0).

### 4.3. Bảng đơn hình (The Simplex Tableau)

Bảng đơn hình là công cụ để tổ chức và thực hiện các phép biến đổi Gauss-Jordan. Cấu trúc bảng bao gồm các hệ số của ràng buộc và hàm mục tiêu.

**Bảng khởi tạo (Initial Tableau - Slide 28):**


### 4.4. Quy trình xoay (Pivot Operation)


## 5. Phương pháp Hai Pha (The Two-Phase Simplex Method)

### 5.1. Logic của biến giả (Artificial Variables)

### 5.2. Pha 1: Bài toán phụ (Auxiliary Linear Program)


### 5.3. Chuyển tiếp và Pha 2


### 5.4. Trường hợp suy biến tại pha 1



## 6. Triển khai tính toán với Google OR-Tools

### 6.1. Cấu trúc mã nguồn Python

### 6.2. So sánh lý thuyết và thực hành



## 7. Kết luận và các vấn đề nâng cao

Quy hoạch Tuyến tính là sự kết hợp hoàn hảo giữa trực giác hình học (đa diện lồi) và sự chặt chẽ của đại số (ma trận, khử Gauss). Từ việc vẽ các đường thẳng đơn giản trên mặt phẳng, ta đã phát triển nên thuật toán Simplex và phương pháp Hai Pha, cho phép giải quyết các bài toán khổng lồ với hàng nghìn ràng buộc trong không gian đa chiều mà trí tưởng tượng con người không thể hình dung.

Một khía cạnh nâng cao chưa được đề cập sâu trong slide nhưng rất quan trọng là Phân tích Độ nhạy (Sensitivity Analysis) và Bài toán Đối ngẫu (Duality). Mọi bài toán LP (Primal) đều có một bài toán Đối ngẫu (Dual) đi kèm. Giá trị biến đối ngẫu (Shadow Price) cho biết giá trị hàm mục tiêu sẽ thay đổi bao nhiêu nếu ta nới lỏng một ràng buộc thêm 1 đơn vị. Đây là thông tin cực kỳ quý giá trong quản trị kinh doanh, giúp trả lời câu hỏi "Nên bỏ thêm bao nhiêu tiền để mua thêm nguyên liệu?"

Tóm lại, việc nắm vững Simplex và kỹ năng mô hình hóa với OR-Tools trang bị cho ta một công cụ mạnh mẽ để tối ưu hóa việc ra quyết định trong một thế giới mà nguồn lực luôn là hữu hạn.

