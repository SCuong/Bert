const translations = {
  en: {
    title: "BERT Sentiment Analysis | Hotel Review Classification", skipLink: "Skip to analyzer", brandSubtitle: "Sentiment Analysis", brandAria: "BERT Sentiment Analysis home", primaryNavigationAria: "Primary navigation", pageSectionsAria: "Page sections", languageSelectorAria: "Language selector", switchToVietnamese: "Chuyển sang Tiếng Việt", switchToEnglish: "Switch to English", navAnalyze: "Analyze", navModel: "Model", navResults: "Results", navAbout: "About", navCta: "Try the demo",
    heroEyebrow: "University AI course project", heroTitle: "Understand hotel reviews <em>with BERT.</em>", heroText: "A polished demonstration layer around a fine-tuned BERT classifier for English hotel-review sentiment. Enter a review to receive the model’s overall positive or negative prediction.", heroPrimary: "Analyze a review", heroSecondary: "View frozen results", binarySentimentClassification: "Binary sentiment classification", heroVisualAria: "Abstract language-model illustration", pipelineLabel: "BERT PIPELINE", predictionLabel: "Prediction", readyForInput: "Ready for input", liveOutput: "live output",
    analyzerEyebrow: "Interactive demonstration", analyzerTitle: "Analyze a hotel review", analyzerText: "Use a manually written example or enter your own English review. The model is loaded once and reused for inference.", englishOnlyNotice: "The model is currently trained to classify hotel reviews written in English.", reviewLabel: "Hotel review", reviewPlaceholder: "Enter a hotel review here...", inputHelp: "The classifier returns one overall sentiment label. The local demo accepts up to 5,000 characters; the canonical tokenizer handles normal truncation behavior.", exampleReviewsAria: "Example reviews", examplePrompt: "Try an example:", positive: "Positive", negative: "Negative", mixed: "Mixed", analyzeButton: "Analyze sentiment", analyzingButton: "Analyzing sentiment...", clearButton: "Clear",
    resultAria: "Prediction result", resultPlaceholderTitle: "Your result will appear here", resultPlaceholderText: "Submit a review to display the BERT prediction and model probabilities.", bertPrediction: "BERT prediction", confidence: "Confidence", resultExplanation: "The BERT classifier predicts the overall sentiment expressed in the review. Mixed or ambiguous reviews can be more difficult because they may contain competing opinions.",
    resultsEyebrow: "Frozen test-set results", resultsTitle: "A measured improvement over the baseline.", resultsText: "Metrics below are the project’s frozen comparative results; this interface does not retrain or reevaluate either model.", baseline: "Baseline", fineTunedModel: "Fine-tuned model", fineTuned: "Fine-tuned", improvement: "Improvement", bertVsBaseline: "BERT vs. baseline", percentagePoints: "percentage points",
    howItWorks: "How it works", modelTitle: "A compact language pipeline.", modelText: "BERT is a Transformer-based language model. In this project, it was fine-tuned for hotel-review sentiment classification and compared with a TF-IDF + Logistic Regression baseline.", hotelReview: "Hotel review", tokenizer: "Tokenizer", fineTunedBert: "Fine-tuned BERT", sentimentPrediction: "Sentiment prediction",
    inputContext: "Input context", tokenSnapshot: "Token-length snapshot", tokenScope: "Calculated on Train + Validation sets to preserve the held-out Test Set.", modelContextAria: "Model context and limitations", maxLength128: "At MAX_LENGTH=128", coverage: "coverage", above128: "Above 128 tokens", above256: "Above 256 tokens", limitationsEyebrow: "Evidence-based limitations", limitationsTitle: "Where the model can struggle", limitationMixed: "audited errors involved mixed sentiment.", limitationNoise: "involved possible label ambiguity or noise.", limitationNegation: "involved negation or concession.", limitationMarkers: "involved template markers.", truncationNote: "In the 20 audited errors, none exceeded <code>MAX_LENGTH=128</code>.", academicContext: "Academic context", aboutTitle: "Designed for a university AI course presentation.", aboutText: "This application is a demonstration layer around the trained model developed for a hotel-review sentiment classification project. It is not intended as a production sentiment-analysis service.", footerText: "© Academic demonstration · BERT hotel-review sentiment classification", backToTop: "Back to top ↑",
    characters: "characters", enterReview: "Please enter a hotel review before analyzing.", analyzingMessage: "Analyzing the review with the BERT classifier...", predictionCompleted: "Prediction completed.", predictionFailed: "Prediction could not be completed. Please try again.",
  },
  vi: {
    title: "Phân tích cảm xúc BERT | Phân loại đánh giá khách sạn", skipLink: "Chuyển đến phần phân tích", brandSubtitle: "Phân tích cảm xúc", brandAria: "Trang chủ Phân tích cảm xúc BERT", primaryNavigationAria: "Điều hướng chính", pageSectionsAria: "Các phần trên trang", languageSelectorAria: "Chọn ngôn ngữ", switchToVietnamese: "Chuyển sang Tiếng Việt", switchToEnglish: "Chuyển sang Tiếng Anh", navAnalyze: "Phân tích", navModel: "Mô hình", navResults: "Kết quả", navAbout: "Giới thiệu", navCta: "Dùng thử",
    heroEyebrow: "Dự án học phần AI đại học", heroTitle: "Hiểu đánh giá khách sạn <em>với BERT.</em>", heroText: "Lớp trình diễn trực quan cho bộ phân loại BERT đã tinh chỉnh về cảm xúc đánh giá khách sạn bằng tiếng Anh. Nhập một đánh giá để nhận dự đoán tích cực hoặc tiêu cực tổng thể của mô hình.", heroPrimary: "Phân tích đánh giá", heroSecondary: "Xem kết quả cố định", binarySentimentClassification: "Phân loại cảm xúc nhị phân", heroVisualAria: "Minh họa trừu tượng mô hình ngôn ngữ", pipelineLabel: "QUY TRÌNH BERT", predictionLabel: "Dự đoán", readyForInput: "Sẵn sàng nhận dữ liệu", liveOutput: "kết quả trực tiếp",
    analyzerEyebrow: "Trình diễn tương tác", analyzerTitle: "Phân tích đánh giá khách sạn", analyzerText: "Dùng ví dụ có sẵn hoặc nhập đánh giá của bạn bằng tiếng Anh. Mô hình được tải một lần và tái sử dụng cho suy luận.", englishOnlyNotice: "Mô hình hiện được huấn luyện để phân loại đánh giá khách sạn bằng tiếng Anh.", reviewLabel: "Đánh giá khách sạn", reviewPlaceholder: "Nhập đánh giá khách sạn bằng tiếng Anh tại đây...", inputHelp: "Bộ phân loại trả về một nhãn cảm xúc tổng thể. Bản demo cục bộ nhận tối đa 5.000 ký tự; tokenizer chuẩn xử lý hành vi cắt ngắn thông thường.", exampleReviewsAria: "Các đánh giá ví dụ", examplePrompt: "Thử ví dụ:", positive: "Tích cực", negative: "Tiêu cực", mixed: "Trái chiều", analyzeButton: "Phân tích cảm xúc", analyzingButton: "Đang phân tích...", clearButton: "Xóa",
    resultAria: "Kết quả dự đoán", resultPlaceholderTitle: "Kết quả sẽ hiển thị tại đây", resultPlaceholderText: "Gửi một đánh giá để hiển thị dự đoán BERT và các xác suất của mô hình.", bertPrediction: "Dự đoán BERT", confidence: "Độ tin cậy", resultExplanation: "Bộ phân loại BERT dự đoán cảm xúc tổng thể trong đánh giá. Các đánh giá trái chiều hoặc mơ hồ có thể khó hơn vì chúng chứa những ý kiến đối lập.",
    resultsEyebrow: "Kết quả tập kiểm tra cố định", resultsTitle: "Cải thiện được đo lường so với mô hình cơ sở.", resultsText: "Các chỉ số dưới đây là kết quả so sánh cố định của dự án; giao diện này không huấn luyện lại hoặc đánh giá lại mô hình nào.", baseline: "Mô hình cơ sở", fineTunedModel: "Mô hình đã tinh chỉnh", fineTuned: "Đã tinh chỉnh", improvement: "Cải thiện", bertVsBaseline: "BERT so với mô hình cơ sở", percentagePoints: "điểm phần trăm",
    howItWorks: "Cách hoạt động", modelTitle: "Quy trình ngôn ngữ gọn nhẹ.", modelText: "BERT là mô hình ngôn ngữ dựa trên Transformer. Trong dự án này, mô hình được tinh chỉnh cho phân loại cảm xúc đánh giá khách sạn và được so sánh với mô hình cơ sở TF-IDF + Logistic Regression.", hotelReview: "Đánh giá khách sạn", tokenizer: "Tokenizer", fineTunedBert: "BERT đã tinh chỉnh", sentimentPrediction: "Dự đoán cảm xúc",
    inputContext: "Ngữ cảnh đầu vào", tokenSnapshot: "Tổng quan độ dài token", tokenScope: "Tính trên tập Train + Validation để bảo toàn Test Set độc lập.", modelContextAria: "Ngữ cảnh và giới hạn của mô hình", maxLength128: "Ở MAX_LENGTH=128", coverage: "phủ dữ liệu", above128: "Trên 128 token", above256: "Trên 256 token", limitationsEyebrow: "Giới hạn dựa trên bằng chứng", limitationsTitle: "Trường hợp mô hình có thể gặp khó khăn", limitationMixed: "lỗi đã kiểm tra có cảm xúc trái chiều.", limitationNoise: "có thể liên quan đến sự mơ hồ hoặc nhiễu nhãn.", limitationNegation: "có phủ định hoặc nhượng bộ.", limitationMarkers: "có dấu hiệu mẫu (template).", truncationNote: "Trong 20 lỗi đã kiểm tra, không lỗi nào vượt <code>MAX_LENGTH=128</code>.", academicContext: "Bối cảnh học thuật", aboutTitle: "Thiết kế cho bài thuyết trình học phần AI đại học.", aboutText: "Ứng dụng này là lớp trình diễn cho mô hình đã huấn luyện trong dự án phân loại cảm xúc đánh giá khách sạn. Đây không phải là dịch vụ phân tích cảm xúc dùng trong sản xuất.", footerText: "© Trình diễn học thuật · Phân loại cảm xúc đánh giá khách sạn bằng BERT", backToTop: "Về đầu trang ↑",
    characters: "ký tự", enterReview: "Vui lòng nhập đánh giá khách sạn trước khi phân tích.", analyzingMessage: "Đang phân tích đánh giá bằng bộ phân loại BERT...", predictionCompleted: "Đã hoàn tất dự đoán.", predictionFailed: "Không thể hoàn tất dự đoán. Vui lòng thử lại.",
  },
};

const examples = {
  positive: "The room was clean, the staff were friendly, and the location was excellent.",
  negative: "The room was noisy, the bathroom was dirty, and the service was disappointing.",
  mixed: "The location was great, but the room was small and the staff were not very helpful.",
};

const reviewText = document.querySelector("#review-text");
const characterCount = document.querySelector("#character-count");
const analyzeButton = document.querySelector("#analyze-button");
const clearButton = document.querySelector("#clear-button");
const formMessage = document.querySelector("#form-message");
const resultPanel = document.querySelector("#result-panel");
const resultPlaceholder = resultPanel.querySelector(".result-placeholder");
const resultContent = resultPanel.querySelector(".result-content");
const header = document.querySelector("#site-header");
const languageButtons = document.querySelectorAll("[data-language]");
let language = "en";
let lastScrollY = window.scrollY;
let scrollFramePending = false;
const HEADER_SCROLL_THRESHOLD = 8;

function t(key) {
  return translations[language][key] || translations.en[key] || key;
}

function setLanguage(nextLanguage) {
  language = translations[nextLanguage] ? nextLanguage : "en";
  document.documentElement.lang = language;
  document.title = t("title");

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-html]").forEach((element) => {
    element.innerHTML = t(element.dataset.i18nHtml);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    element.setAttribute("aria-label", t(element.dataset.i18nAria));
  });
  languageButtons.forEach((button) => {
    const isActive = button.dataset.language === language;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });

  if (!resultPanel.classList.contains("is-empty")) {
    const isPositive = resultPanel.dataset.sentiment === "positive";
    document.querySelector("#sentiment-label").textContent = t(isPositive ? "positive" : "negative");
  }
  updateCharacterCount();
  try {
    localStorage.setItem("bert-demo-language", language);
  } catch (_) {
    // The demo remains usable when browser storage is disabled.
  }
}

function updateCharacterCount() {
  characterCount.textContent = `${reviewText.value.length} ${t("characters")}`;
}

function setMessage(message = "", type = "") {
  formMessage.textContent = message;
  formMessage.className = `form-message ${type}`.trim();
}

function setLoading(isLoading) {
  analyzeButton.disabled = isLoading;
  analyzeButton.classList.toggle("is-loading", isLoading);
  analyzeButton.querySelector(".button-label").textContent = isLoading
    ? t("analyzingButton")
    : t("analyzeButton");
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function showResult(prediction) {
  const isPositive = prediction.label === "positive";
  const positive = prediction.probabilities.positive;
  const negative = prediction.probabilities.negative;

  resultPanel.classList.remove("is-empty", "negative");
  resultPanel.classList.toggle("negative", !isPositive);
  resultPanel.dataset.sentiment = prediction.label;
  resultPlaceholder.hidden = true;
  resultContent.hidden = false;
  document.querySelector("#sentiment-label").textContent = t(isPositive ? "positive" : "negative");
  document.querySelector("#sentiment-icon").textContent = isPositive ? "✓" : "!";
  document.querySelector("#confidence-value").textContent = formatPercent(prediction.confidence);
  document.querySelector("#positive-probability").textContent = formatPercent(positive);
  document.querySelector("#negative-probability").textContent = formatPercent(negative);

  window.requestAnimationFrame(() => {
    document.querySelector("#positive-bar").style.width = `${positive * 100}%`;
    document.querySelector("#negative-bar").style.width = `${negative * 100}%`;
  });
}

async function analyzeReview() {
  const text = reviewText.value.trim();
  if (!text) {
    setMessage(t("enterReview"), "error");
    reviewText.focus();
    return;
  }

  setLoading(true);
  setMessage(t("analyzingMessage"));

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(t("predictionFailed"));
    }

    showResult(payload);
    setMessage(t("predictionCompleted"));
  } catch (error) {
    setMessage(error.message || t("predictionFailed"), "error");
  } finally {
    setLoading(false);
  }
}

reviewText.addEventListener("input", updateCharacterCount);
analyzeButton.addEventListener("click", analyzeReview);
clearButton.addEventListener("click", () => {
  reviewText.value = "";
  updateCharacterCount();
  setMessage();
  reviewText.focus();
});

document.querySelectorAll("[data-example]").forEach((button) => {
  button.addEventListener("click", () => {
    reviewText.value = examples[button.dataset.example];
    updateCharacterCount();
    setMessage();
    reviewText.focus();
  });
});

languageButtons.forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.language));
});

function updateHeader() {
  const currentScrollY = window.scrollY;
  const distance = currentScrollY - lastScrollY;
  if (Math.abs(distance) >= HEADER_SCROLL_THRESHOLD || currentScrollY <= HEADER_SCROLL_THRESHOLD) {
    header.classList.toggle("is-hidden", distance > 0 && currentScrollY > HEADER_SCROLL_THRESHOLD);
    header.classList.toggle("is-scrolled", currentScrollY > HEADER_SCROLL_THRESHOLD);
    lastScrollY = currentScrollY;
  }
  scrollFramePending = false;
}

window.addEventListener("scroll", () => {
  if (!scrollFramePending) {
    scrollFramePending = true;
    window.requestAnimationFrame(updateHeader);
  }
}, { passive: true });

try {
  setLanguage(localStorage.getItem("bert-demo-language") || "en");
} catch (_) {
  setLanguage("en");
}
updateHeader();
