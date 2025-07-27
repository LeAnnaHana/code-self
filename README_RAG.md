## Flow hệ thống RAG (Retrieval-Augmented Generation) đơn giản

### 1. **Data Chunking (Chia nhỏ dữ liệu)**
- **Cơ sở dữ liệu (DB)**: Dữ liệu sản phẩm được thu thập từ các nguồn (website bán hàng) và được lưu trữ trong cơ sở dữ liệu (DB), bao gồm các thông tin như mô tả, giá cả, thông số kỹ thuật, khuyến mãi, đánh giá sản phẩm, v.v.
- **Chunking**: Dữ liệu trong DB sẽ được chia thành các phần nhỏ hơn (chunks). Mỗi chunk đại diện cho một đoạn thông tin liên quan đến sản phẩm như mô tả sản phẩm, giá, đánh giá, khuyến mãi, v.v. Điều này giúp hệ thống truy xuất và xử lý dữ liệu nhanh chóng hơn.

### 2. **Search (Truy vấn dữ liệu)**
- **Search Engine (Elastic Search)**: Dữ liệu sau khi được chunking sẽ được **index** và truy vấn qua công cụ tìm kiếm (Elastic Search). Elastic Search giúp tìm kiếm các đoạn dữ liệu liên quan nhanh chóng dựa trên truy vấn của người dùng.
- **Vector Search**: Sử dụng **vector search** để tìm kiếm các kết quả có liên quan đến truy vấn của người dùng. Hệ thống có thể sử dụng embeddings để tạo vector cho mỗi chunk và so khớp với truy vấn của người dùng để trả về kết quả liên quan nhất.

### 3. **Prompt System (Hệ thống gợi ý)**

#### A. **User Prompt (Từ người dùng)**
- **Mô tả**: Đây là những câu truy vấn hoặc yêu cầu trực tiếp từ phía người dùng, bao gồm các thông tin về sản phẩm, tính năng, giá cả, chương trình khuyến mãi, hoặc bất kỳ thông tin nào mà người dùng đang quan tâm. Dữ liệu từ **User Prompt** sẽ là cơ sở để hệ thống RAG truy xuất thông tin và sinh câu trả lời.
- **Các yếu tố chính của User Prompt**:
  - **Context** (Ngữ cảnh): Những thông tin người dùng đã tìm kiếm trước đó, hoặc các thông tin bổ sung giúp chatbot hiểu rõ ngữ cảnh của câu hỏi. Ví dụ: người dùng đã tìm kiếm về điện thoại và hiện muốn so sánh giá của các mẫu điện thoại khác nhau.
  - **History** (Lịch sử tương tác): Những truy vấn trước đó của người dùng có thể ảnh hưởng đến câu trả lời hiện tại. Ví dụ: nếu người dùng đã tìm kiếm một sản phẩm cụ thể, chatbot có thể tự động gợi ý các sản phẩm tương tự dựa trên lịch sử.
  - **Specific Needs** (Nhu cầu cụ thể): Những yêu cầu cụ thể từ phía người dùng như so sánh sản phẩm, tìm kiếm dựa trên ngân sách hoặc thông số kỹ thuật cụ thể.
  
- **Ví dụ User Prompt**:
  - "Tôi muốn tìm điện thoại giá dưới 10 triệu."
  - "So sánh giúp tôi điện thoại A và điện thoại B."
  - "Có chương trình khuyến mãi nào cho laptop không?"

#### B. **System Prompt (Gợi ý từ hệ thống)**
- **Mô tả**: **System Prompt** là các gợi ý được sinh ra tự động từ hệ thống nhằm dẫn dắt và tối ưu hóa quá trình truy vấn của người dùng. Điều này giúp cải thiện hiệu quả tìm kiếm và đảm bảo rằng chatbot cung cấp thông tin chính xác và phù hợp nhất.
- **Vai trò của System Prompt**:
  - **Hướng dẫn người dùng**: Nếu người dùng đưa ra truy vấn không đầy đủ hoặc không rõ ràng, chatbot sẽ sử dụng system prompt để hỏi thêm chi tiết nhằm cung cấp câu trả lời tốt hơn.
  - **Bổ sung thông tin quan trọng**: Khi nhận truy vấn, nếu hệ thống cảm thấy thiếu thông tin, system prompt sẽ hỏi lại hoặc đưa ra các gợi ý giúp người dùng tìm kiếm hiệu quả hơn.
  - **Cải thiện độ chính xác**: Hệ thống có thể tự động định hướng truy vấn của người dùng đến các chủ đề liên quan để cải thiện độ chính xác và chất lượng của câu trả lời.
  
- **Ví dụ System Prompt**:
  - Nếu người dùng hỏi: "Tôi muốn mua điện thoại", chatbot có thể tự động hỏi lại: "Bạn có muốn tìm theo thương hiệu hoặc theo giá không?"
  - Khi người dùng hỏi về một sản phẩm hết hàng, chatbot có thể gợi ý: "Sản phẩm này hiện không có sẵn, bạn có muốn xem các sản phẩm tương tự không?"

### 4. **RAG Process (Quá trình RAG)**
- **Retrieval (Truy xuất dữ liệu)**: Sau khi nhận truy vấn từ **User Prompt** và bổ sung thông tin từ **System Prompt**, hệ thống sẽ tìm kiếm và truy xuất các chunks dữ liệu từ **Elastic Search** hoặc **Vector Search**. Các dữ liệu này có thể bao gồm mô tả sản phẩm, đánh giá, thông số kỹ thuật hoặc các thông tin liên quan khác.
- **Augmentation (Bổ sung thông tin)**: Dữ liệu truy xuất sẽ được bổ sung và sắp xếp lại dựa trên ngữ cảnh truy vấn của người dùng. Hệ thống sẽ kết hợp các kết quả từ các chunks dữ liệu để tạo ra một câu trả lời hoàn chỉnh và liên kết hợp lý.
- **Generation (Sinh câu trả lời)**: Hệ thống sử dụng mô hình LLM (Large Language Model) để sinh ra câu trả lời tự nhiên dựa trên dữ liệu đã truy xuất và các thông tin bổ sung. Mô hình LLM sẽ ghép các thông tin đã truy xuất thành câu trả lời mạch lạc, phù hợp với ngữ cảnh truy vấn của người dùng.

### 5. **Kết quả (Response)**
- Sau khi **sinh câu trả lời**, hệ thống chatbot sẽ gửi phản hồi cho người dùng. Kết quả bao gồm thông tin chính xác về sản phẩm mà người dùng quan tâm, các chi tiết như giá, khuyến mãi, đánh giá, hoặc bất kỳ thông tin nào khác liên quan đến truy vấn của họ.

### 6. **Tính năng gợi ý sản phẩm hoàn chỉnh**
- Sau khi câu trả lời được sinh ra từ hệ thống **RAG**, chatbot có thể đưa ra các đề xuất sản phẩm (product suggestions) phù hợp với nhu cầu của người dùng dựa trên các yếu tố như giá cả, tính năng, hoặc các sản phẩm có đánh giá cao từ người dùng khác.

---

## Tóm tắt luồng hoạt động của hệ thống RAG:
1. **Dữ liệu sản phẩm** được lưu trữ trong cơ sở dữ liệu và chia thành nhiều **chunk**.
2. Khi người dùng gửi truy vấn (**User Prompt**), nếu cần, hệ thống sẽ sinh ra các **System Prompt** để yêu cầu thêm thông tin chi tiết.
3. **Elastic Search** và **Vector Search** sẽ tìm kiếm các chunk dữ liệu liên quan.
4. **Dữ liệu được truy xuất** từ cơ sở dữ liệu và kết hợp với **mô hình LLM** để sinh câu trả lời tự nhiên.
5. **Phản hồi của chatbot** bao gồm các thông tin chi tiết về sản phẩm và có thể bổ sung **gợi ý sản phẩm** dựa trên nhu cầu cá nhân.
