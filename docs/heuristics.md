# Cơ sở lý thuyết, kiến trúc giải thuật và ứng dụng thực tiễn của Heuristic trong tối ưu tổ hợp


## 1. Cơ sở lý thuyết và triết lý kiến tạo của Heuristic trong khoa học máy tính. 

### 1.1. Bối cảnh toán học và sự cần thiết của cách tiếp cận phi chính xác

Trong lĩnh vực khoa học máy tính lý thuyết và vận trù học, bài toán tối ưu đóng vai trò trung tâm, từ việc lập lịch trình cho các hãng hàng không, tối ưu hoá chuỗi cung ứng,
đến việc huấn luyện các mạng nơ-ron sâu trong trí tuệ nhân tạo. Tuy nhiên, một rào cản toán học to lớn tồn tại dưới dạng các lớp độ phức tạp tính toán. Trong khi các bài toán thuộc lớp
P (Polynomial Time) có thể giải quyết hiệu quả, phần lớn các bài toán tối ưu hoá thực tế lại thuộc lớp **NP-khó (NP-hard)** hoặc **NP-đẩy đủ (NP-complete)**. 
Đặc trưng của các lớp này bài toán này là không gian tìm kiếm giải pháp bùng nổ theo hàm số mũ khi kích thước dữ liệu đầu vào tăng lên.

Đối mặt với sự bùng nổ tổ hợp (combinatorial explosion) này, các phương pháp giải quyết chính xác (exact methods) như quy hoạch động (dynamic programming),
nhánh cận (branch and bound), hay quy hoạch tuyến tính nguyên (integer linear programming) thường trở nên bất khả thi về mặt thời gian. 
Việc tìm kiếm một lời giải tối ưu toàn cục (global optimum) cho một bài toán người du lịch (TSP) với hàng nghìn thành phố có thể tiêu tốn hàng thế kỷ nếu sử dụng
các siêu máy tính hiện đại nhất để duyệt toàn bộ không gian. Đây chính là điểm khởi đầu cho sự ra đời và thống trị của các **Giải thuật Heuristic.**

Heuristic, bắt nguồn từ tiếng Hy Lap "eurisko" (tôi tìm ra), không đại diện cho sự từ bỏ tính chính xác, mà là sự dịch chuyển triết lý từ "tối ưu tuyệt đối" sang "tối ưu thực dụng" (pragmatic optimizatin).
Bản chất của heuristic là một kỹ thuật giải quyết vấn đề dựa trên kinh nghiệm, trực giác hoặc các quy tắc ngón tay cái (rules of thumb) để tìm ra các giải pháp khả thi trong thời gian chấp nhận được. 
Mục tiêu của heuristic là sản sinh ra một giải pháp "đủ tốt" (good enough) cho vấn đề hiện tại, hy sinh tính tối ưu, tính đầy đủ, hoặc độ chính xác để đổi lấy tốc độ xử lý (speed). 


### 1.2. Tam giác đánh đỏi (The Trade-off Triangle) và phân tích chi phí - Lợi ích

Mọi giải thuật heuristic đều vận hành dựa trên một sự thoả hiệp có tính toán. Chúng ta có thể hình dung điều này qua một tam giác đánh đổi với ba đỉnh:
1. **Chất lượng giải pháp (Optimality):** Mức độ gần của giải pháp tìm được so với giải pháp tối ưu thực sự. Heuristic thường chỉ cam kết tìm được cực trị địa phương (local optima) hoặc một giải pháp xấp xỉ nằm trong giới hạn sai số cho phép. 
2. **Tài nguyên tính toán (Computational Cost):** Bao gồm thời gian chạy (Time Complexity) và bộ nhớ (Space Complexity). Heuristic được thiết kế để giảm thiểu yếu tố này xuống mức đa thức thấp (ví dụ: $O(n^2)$) hoặc $O(nlogn)$). 
3. **Độ bao phủ (Completeness):** Khả năng tìm thấy giải pháp nếu nó tồn tại. Một số heuristic có thể thất bài trong việc tìm ra giải pháp khả thi trong các trường hợp biên ngặt nghèo. 

Sự đánh đổi này không phải là ngẫu nhiên mà đã được thiết kế dựa trên đặc thù của bài toán. Ví dụ, trong các hệ thống giao dịch chứng khoán cao tần (high-frequency trading), tốc độ ra quyết định (mili-giây) quan trọng hơn việc tìm được mức giá tối ưu
tuyệt đối mà phải mất 10 phút mới tính xong. Ngược lại, trong thiết kế kết cấu cầu đường, độ chính xác lại được ưu tiên hàng đầu. Heuristic trong khoa học máy tính thường nhắm đến việc tối đa hóa chất lượng giải pháp trong một quỹ thời gian cố định.

### 1.3. Phân loại chiến lược Heuristic

Dựa trên tài liệu tham khảo và tổng quan văn liệu, báo cáo này sẽ phân tích sâu hai dòng chảy chính của heuristic:
* **Heuristic xây dựng (Constructive Heuristics):** Tiêu biểu là **Giải thuật Tham lam (Greedy Algorithms)** Cách tiếp cận này xây dựng giải pháp từ con số không, từng bước thêm các thành phần vào giải pháp dựa trên các quyết định tối ưu cục bộ.
Quá trình này thường diễn ra nhanh chóng và kết thúc khi một giải pháp hoàn chỉnh được hình thành. 

* **Heuristic cải tiến (Improvement Heuristics):** Tiêu biểu là **tìm kiếm cục bộ (Local Search)** và các biến thể Metaheuristic như **Simulated Annealing**. 
Cách tiếp cận này bắt đầu từ một giải pháp hoàn chỉnh (có thể được tạo ngẫu nhiên hoặc bởi heuristic xây dựng) và liên tục sửa đổi nó để nâng cao chất lượng. Đây là quá trình lặp (iterative) và thường tốn kém thời gian hơn nhưng có khả năng thoát khỏi các bẫy tối ưu cục bộ tốt hơn. 


## 2. Giải thuật tham lam (Greedy Algorithms): Kiến trúc và phân tích hiệu năng

Giải thuật tham lam đại diện cho triết lý "nhìn ngắn hạn để đạt được mục tiêu dài hạn". 
Nguyên lý cốt lõi của nó là tại mỗi bước ra quyết định, luôn chọn phương án tốt nhất có vào thời điểm đó (locally optimal choice) với hi vọng rằng chuỗi các lựa chọn cục bộ này sẽ dẫn đến một giải pháp tối ưu toàn cục (global optimum). 

### 2.1. Cấu trúc giải phẫu của giải thuật tham lam

Một giải thuật tham lam tiêu chuẩn không chỉ đơn thuần là "chọn cái lớn nhất". Để đảm bảo tính đúng đắn và hiệu quả, nó phải tuân thủ một cấu trúc chặt chẽ gồm 5 thành phần,
như được mô tả trong slide 6 của tài liệu và nguồn bổ trợ:
1. **Tập Ứng viên ($C$ - Candidate Set):** Chứa tất cả các thành phần tiềm năng có thể tham gia vào giải pháp (ví dụ: danh sách các đồ vật trong bài toán cái túi, danh sách các cạnh trong bài toán tìm đường).
2. **Tập Giải pháp ($S$ - Solution Set):** Chứa các thành phần đã được lựa chọn. Ban đầu tập này rỗng.
3. **Hàm Lựa chọn (select Function):** Đây là "trái tim" của giải thuật. Hàm này đánh giá các ứng viên trong $C$ và chọn ra ứng viên hứa hẹn nhất theo một tiêu chí tham lam xác định (greedy criterion). 
Tiêu chí này có thể là giá trị lớn nhất, trọng lượng nhỏ nhất, hoặc tỷ lệ lợi nhuận cao nhất.
4. **Hàm khả thi (`feasible` Function):** Đóng vai trò là bộ lọc kiểm soát. Trước khi một ứng viên $x$ được thêm vào $S$, hàm này kiểm tra xem $S \cup \{x\}$ có vi phạm bất kỳ ràng buộc nào của bài toán hay không (ví dụ: có vượt quá trọng lượng túi không). Nếu vi phạm, ứng viên bị loại bỏ vĩnh viễn.
5. **Hàm mục tiêu (`solution` Function):**  Xác định xem tập $S$ đã cấu thành một giải pháp hoàn chỉnh cho bài toán hay chưa.

```
Greedy(C) {
    S = {}; // Khởi tạo giải pháp rỗng
    while (C khác rỗng) và (not solution(S)) {
        x = select(C); // Lựa chọn tham lam
        C = C \ {x};   // Loại bỏ x khỏi tập ứng viên
        if feasible(S U {x}) { // Kiểm tra ràng buộc
            S = S U {x}; // Chấp nhận x
        }
    }
    return S;
}
```

**Phân tích rủi ro:** Đặc điểm quan trọng nhất của cấu trúc này là tính **không thể đảo ngược (irrevocability)**. Một khi ứng viên $x$ đã được chọn vào S, nó sẽ ở đó mãi mãi, và một khi bị loại, nó sẽ không bao giờ được xem xét lại. 
Giải thuật tham lam không có cơ chế quay lui (backtracking) để sửa sai. Điều này giúp giải thuật đạt tốc độ cực nhanh thường là $O(N)$ hoặc $O(N \log N)$ do chi phí sắp xếp), nhưng cũng chính là điểm yếu chí mạng khiến nó dễ rơi vào tối
ưu cục bộ nếu bài toán không có cấu trúc nền tảng phù hợp (Matroid structure).

### 2.2. Nghiên cứu điển hình 1: Các biến thể bài toán cái túi (Knapsack Problems)


### 2.2.1 Bài toán Cái túi Phân số (Fractional Knapsack)


### 2.2.2 Bài toán Cái túi 0/1 (0/1 Knapsack)


### 2.2.3. Bài toán đa cái túi (Multi-Knapsack) và Bin Packing


## 2.3. Nghiên cứu điển hình 2: Bài toán người du lịch (TSP)
Bài toán TSP yêu cầu tìm chu trình ngắn nhất đi qua $n$ thành phố. Đây là bài toán kiểm thử kinh điển cho mọi giải thuật heuristic.

**Chiến lược Nearest Neighbor (Láng giềng gần nhất):**
- _Thuật toán:_ Xuất phát từ một thành phố bất kỳ. Tại mỗi bước, đi đến thành phố chưa thăm gần nhất. Quay về điểm đầu khi đã đi hết. 
- _Phân tích hiệu năng:_ Slide 21  và dữ liệu nghiên cứu  chỉ ra rằng phương pháp này thường cho kết quả kém (trung bình tệ hơn 15-20% so với tối ưu). Nguyên nhân là do tính "tham lam": việc chọn cạnh ngắn nhất hiện tại có thể buộc người du lịch phải chọn một cạnh cực dài ở bước cuối cùng để khép kín vòng tròn (hiện tượng "painting yourself into a corner").

**Chiến lược cải tiến:** Tài liệu đề xuất các cải tiến:
1. **Multi-start:** Chạy Nearest Neighbor n lần, mỗi lần bắt đầu từ một thành phố khác nhau, và chọn lộ trình tốt nhất. 
2. **MST-based:** Xây dựng cây khung nhỏ nhất (Minimum Spanning Tree), sau đó duyệt cây theo chiều sâu (DFS) để tạo lộ trình. 
Phương pháp này đảm bảo lộ trình không vượt qua 2 lần tối ưu (2-approximation ratio) trong không gian metric. 

   
## 2.4. Nghiên cứu điển hình 3: Bài toán phủ tập (Set Cover)

**Mô hình:** Cần chọn một số lượng tối thiểu các tập con từ một họ các tập hợp sao cho hợp của chúng bao phủ toàn bộ các phần tử của tập vũ trụ $U$.
Ứng dụng trong việc chọn địa điểm đặt trạm phát sóng, tối ưu hóa đội ngũ nhân sự. 




## 3. Nghiên cứu Tình huống Chuyên sâu: Bài toán Phân công Giảng dạy Cân bằng (Balanced Class Teacher Assignment)









## 4. Tìm kiếm cục bộ (Local Search): Khai phá cảnh quan tối ưu hoá

Khi giải thuật tham lam bị mắc kẹt tại các "hố" tối ưu cục bộ do tầm nhìn ngắn hạn, 
tìm kiếm cục bộ (local search) cung cấp một phương pháp tiếp cận khác: cải tiến liên tục (iterative improvement).
Thay vì xây dựng giải pháp từ đầu, Local Search bắt đầu từ một giải pháp hoàn chỉnh (dù có thể tồi) và tìm cách sửa chữa nó. 

### 4.1. Nguyên lý hoạt động và ẩn dụ địa hình

Local Search coi không gian các giải pháp khả thi như một cảnh quan địa hình (landscape), trong đó độ cao của mỗi điểm tương ứng với giá trị hàm mục tiêu (fitness).
- **Trạng thái (State):** Một cấu hình giải pháp cụ thể (ví dụ: một cách đặt 8 quân hậu). 
- **Láng giềng (Neighbor):** Các giải pháp có thể đạt được tại trạng thái hiện tại thông qua một thay đổi nhỏ (move).
- **Mục tiêu:** Tìm "đỉnh núi" cao nhất (Global Maximum).

Thuật toán cơ bản nhất là **Leo đồi (Hill Climbing)**: Từ vị trí hiện tại, quan sát các láng giềng. 
Nếu có láng giềng nào cao hơn, bước sang đó. Lặp lại cho đến khi đứng ở định cao nhất trong tầm mắt. 

### 4.2. Các cạm bẫy của cảnh quan tối ưu hoá
Tài liệu (slide 37, 43) và các nguồn bổ trợ phân tích chi tiết các cấu trúc địa hình khiến hill climbing thất bại:
1. **Cực trị cục bộ (Local Optima):** Là một đỉnh đồi, nhưng thấp hơn đỉnh Everest. Tại đây, mọi bước đi đều dẫn xuống dốc, khiến thuật toán tưởng nhầm mình dã đến đích tối thượng. Đây là vấn đề phổ biến nhất (ví dụ: Leo đồi 8-Queens bị kẹt 86% số lần thử).
2. **Cao nguyên (Plateaus):** Một vùng đất phẳng nơi giá trị hàm mục tiêu không thay đổi giữa các láng giềng. Thuật toán mất phương hướng vì không biết đi hướng nào để lên cao hơn ("Lạc trong sương mù").
3. **Gờ (Ridges):** Dạng địa hình hẹp và dốc, giống như sống lưng khủng long. Mặc dù đỉnh dốc đi lên, nhưng các bước di chuyển cơ bản (Bắc/Đông/Nam/Tây) của thuật toán lại chỉ dẫn xuống dốc, khiến nó không thể leo dọc theo sống lưng.


### 4.3. Đinh nghĩa láng giềng (Neighborhood Definition): Chìa khoá của Local Search

Sức mạnh của Local Search phụ thuộc hoàn toàn vào cách ta định nghĩa "ai là hàng xóm". Một định nghĩa láng giềng tốt phải đảm bảo sự kết nối của không gian tìm kiếm. Tài liệu về đề cập các định nghĩa quan trọng.

| Bài toán | Định nghĩa Láng giềng (Neighborhood/Move) | Phân tích Tác động |
|----------|-------------------------------------------|-------------------|
| **N-Queens** | Di chuyển 1 quân hậu trong cột của nó. Hoặc hoán đổi (swap) 2 cột. | Thay đổi nhỏ giúp giảm xung đột cục bộ. |
| **Two-Partition** | **Move:** Chuyển 1 phần tử từ tập A sang B. **Swap:** Hoán đổi 1 phần tử của A với 1 phần tử của B. | Swap giữ nguyên số lượng phần tử nhưng thay đổi tổng giá trị, giúp cân bằng lại 2 tập hợp. |
| **TSP** | **2-opt:** Loại bỏ 2 cạnh, nối lại chéo để đảo ngược một đoạn đường. **3-opt:** Loại 3 cạnh, nối lại theo cách mới. | 2-opt loại bỏ các điểm giao cắt chéo (uncrossing), rất hiệu quả để làm trơn đường đi. |

### 4.4. Metaheuristic: Vượt qua tính cục bộ ngẫu nhiên
Để khắc phục sự "thiển cận" của leo đồi, tài liệu giới thiệu các chiến lược chấp nhận rủi ro:
1. **Random Walk (Bước đi ngẫu nhiên):** Chọn láng giềng ngẫu nhiên. Nếu tốt hơn thì đi, nếu xấu hơn vẫn có thể đi. Giúp thoát khỏi hố nhưng rất chậm chạp. 
2. **Simulated Annealing (Tôi luyện mô phỏng):** 
- _Cảm hứng:_ Mô phỏng quá trình làm nguội kim loại từ từ để các nguyên từ sắp xép vào cấu trúc tinh thể bền vững nhất (năng lượng thấp nhất). 
- _Cơ chế Metropolis:_ Chấp nhận bước đi tồi (xuống dốc $\Delta E < 0$) với xác suất $P = e^{\Delta E / T}$.
- Vai trò của _Nhiệt độ T:_
  * Khi _T_ cao (giai đoạn đầu): $P \approx 1$. Giải thuật chấp nhận hầu hết các bước di, cư xử giống Random Walk, cho phép "nhảy" qua lại giữa các vùng đồi núi, khám phá rộng (Exploratiion).
  * Khi _T_ giảm (làm nguội): $P \to 0$. Giải thuật trở nên khó tính hơn, chỉ chấp nhận bước đi tốt, dần dần hội tụ về Leo đồi để tinh chỉnh chi tiết (Exploitation).
 
## 5. Tổng kết và kiến nghị

Qua phân tích, chúng ta thấy rằng Heuristic là một lĩnh vực phong phú, kết hợp giữa sự chặt chẽ của toán học và sự linh hoạt của thực nghiệm. 
1. **Từ tham lam đến tinh chỉnh:** Một mô hình giải quyết vấn đề hiệu quả thường là mô hình lai (hybrid): sử dụng **Greedy** để tạo ra một giải pháp khởi dầu tốt trong tích tắc, sau đó sử dụng **Local Search** hoặc **Simulated Annealing** để tinh chỉnh nó trong thời gian còn lại.
2. **Vai trò của dữ liệu:** Hiệu quả của Heuristic phụ thuộc nặng nề và khâu tiền xử lý dữ liệu. Viêc sắp xếp (sorting) trong bài toán Knapsack hay Multi-Knapsack chính là cách chúng ta nhúng "trí thông minh" vào dữ liệu trước khi thuật toán chạy.
3. **Tư duy thực dụng:** Heuristic dạy chúng ta rằng trong các bài toán phức tạp, một giải pháp khả thi ngay bây giờ có giá trị hơn một giải pháp hoàn hảo trong tương lai xa. Sự chấp nhận rủi ro và sai số là cái giá xứng đáng cho tính hiệu quả và tốc độ.