import json
from pathlib import Path

import pandas as pd
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_PATH = PROJECT_ROOT / "data" / "phishing_site_urls.csv"
METRICS_PATH = PROJECT_ROOT / "models" / "training_metrics.json"
OUTPUT_PATH = PROJECT_ROOT / "major_project_research_paper.pdf"


REFERENCES = [
    {
        "authors": "D. Sahoo, C. Liu, and S. C. H. Hoi",
        "title": "Malicious URL Detection using Machine Learning: A Survey",
        "venue": "arXiv",
        "year": "2017",
        "url": "https://arxiv.org/abs/1701.07179",
    },
    {
        "authors": "A. Hannousse and S. Yahiouche",
        "title": "Towards benchmark datasets for machine learning based website phishing detection: An experimental study",
        "venue": "Engineering Applications of Artificial Intelligence",
        "year": "2021",
        "url": "https://doi.org/10.1016/j.engappai.2021.104347",
    },
    {
        "authors": "A. Safi and S. Singh",
        "title": "A systematic literature review on phishing website detection techniques",
        "venue": "Journal of King Saud University - Computer and Information Sciences",
        "year": "2023",
        "url": "https://doi.org/10.1016/j.jksuci.2023.01.004",
    },
    {
        "authors": "F. Castano, E. Fidalgo, E. Alegre, D. Chaves, and M. Sanchez-Paniagua",
        "title": "State of the Art: Content-based and Hybrid Phishing Detection",
        "venue": "arXiv",
        "year": "2021",
        "url": "https://arxiv.org/abs/2101.12723",
    },
    {
        "authors": "M. Bahaghighat, M. Ghasemi, and F. Ozen",
        "title": "A high-accuracy phishing website detection method based on machine learning",
        "venue": "Journal of Information Security and Applications",
        "year": "2023",
        "url": "https://doi.org/10.1016/j.jisa.2023.103553",
    },
    {
        "authors": "S. K. Hasane Ahammad, S. D. Kale, G. D. Upadhye, and S. D. Pande",
        "title": "Phishing URL detection using machine learning methods",
        "venue": "Advances in Engineering Software",
        "year": "2022",
        "url": "https://doi.org/10.1016/j.advengsoft.2022.103288",
    },
    {
        "authors": "B. B. Gupta, K. Yadav, I. Razzak, and K. Psannis",
        "title": "A novel approach for phishing URLs detection using lexical based machine learning in a real-time environment",
        "venue": "Computer Communications",
        "year": "2021",
        "url": "https://doi.org/10.1016/j.comcom.2021.04.023",
    },
    {
        "authors": "A. Aljofey, Q. Jiang, A. Rasool, H. Chen, W. Liu, Q. Qu, and Y. Wang",
        "title": "An effective detection approach for phishing websites using URL and HTML features",
        "venue": "Scientific Reports",
        "year": "2022",
        "url": "https://doi.org/10.1038/s41598-022-10841-5",
    },
    {
        "authors": "A. Zamir, H. U. Khan, T. Iqbal, N. Yousaf, A. Aslam, and A. Anjum",
        "title": "Phishing web site detection using diverse machine learning algorithms",
        "venue": "The Electronic Library",
        "year": "2020",
        "url": "https://doi.org/10.1108/EL-05-2019-0118",
    },
    {
        "authors": "A. Awasthi and N. Goel",
        "title": "Phishing website prediction using base and ensemble classifier techniques with cross-validation",
        "venue": "Cybersecurity",
        "year": "2022",
        "url": "https://doi.org/10.1186/s42400-022-00126-9",
    },
    {
        "authors": "N. Nagy, M. Aljabri, A. Shaahid, A. Albin Ahmed, and M. Yamin",
        "title": "Phishing URLs Detection Using Sequential and Parallel ML Techniques: Comparative Analysis",
        "venue": "Sensors",
        "year": "2023",
        "url": "https://doi.org/10.3390/s23073467",
    },
    {
        "authors": "R. S. Rao and A. R. Pais",
        "title": "Detection of phishing websites using an efficient feature-based machine learning framework",
        "venue": "Neural Computing and Applications",
        "year": "2018",
        "url": "https://doi.org/10.1007/s00521-017-3305-0",
    },
    {
        "authors": "S. S. Shafin",
        "title": "An explainable feature selection framework for web phishing detection with machine learning",
        "venue": "Data Science and Management",
        "year": "2025",
        "url": "https://doi.org/10.1016/j.dsm.2024.08.004",
    },
    {
        "authors": "F. Rashid, B. Doyle, S. C. Han, and S. Seneviratne",
        "title": "Phishing URL detection generalisation using Unsupervised Domain Adaptation",
        "venue": "Computer Networks",
        "year": "2024",
        "url": "https://doi.org/10.1016/j.comnet.2024.110398",
    },
    {
        "authors": "M. Mia, D. Derakhshan, and M. M. A. Pritom",
        "title": "Can Features for Phishing URL Detection Be Trusted Across Diverse Datasets? A Case Study with Explainable AI",
        "venue": "Proceedings of the 11th International Conference on Networking, Systems, and Security",
        "year": "2024",
        "url": "https://doi.org/10.1145/3704522.3704532",
    },
    {
        "authors": "A. Butnaru, A. Mylonas, and N. Pitropakis",
        "title": "Towards Lightweight URL-Based Phishing Detection",
        "venue": "Future Internet",
        "year": "2021",
        "url": "https://doi.org/10.3390/fi13060154",
    },
    {
        "authors": "H. Tupsamudre, A. K. Singh, and S. Lodha",
        "title": "Everything Is in the Name - A URL Based Approach for Phishing Detection",
        "venue": "Lecture Notes in Computer Science",
        "year": "2019",
        "url": "https://doi.org/10.1007/978-3-030-20951-3_21",
    },
    {
        "authors": "P. Xu",
        "title": "A Transformer-based Model to Detect Phishing URLs",
        "venue": "arXiv",
        "year": "2021",
        "url": "https://arxiv.org/abs/2109.02138",
    },
    {
        "authors": "T. Kim, N. Park, J. Hong, and S.-W. Kim",
        "title": "Phishing URL Detection: A Network-based Approach Robust to Evasion",
        "venue": "arXiv / CCS",
        "year": "2022",
        "url": "https://arxiv.org/abs/2209.01454",
    },
    {
        "authors": "W. Guo, Q. Wang, H. Yue, and H. Sun",
        "title": "Efficient Phishing URL Detection Using Graph-based Machine Learning and Loopy Belief Propagation",
        "venue": "IEEE ICC",
        "year": "2025",
        "url": "https://doi.org/10.1109/ICC52391.2025.11161346",
    },
    {
        "authors": "Unknown author metadata in Crossref",
        "title": "Robust URL Phishing Detection Based on Deep Learning",
        "venue": "KSII Transactions on Internet and Information Systems",
        "year": "2020",
        "url": "https://doi.org/10.3837/tiis.2020.07.001",
    },
    {
        "authors": "C. Lai, A. Selamat, and R. Ibrahim",
        "title": "URL Phishing Detection by Using Natural Language Processing and Deep Learning Model",
        "venue": "Frontiers in Artificial Intelligence and Applications",
        "year": "2024",
        "url": "https://doi.org/10.3233/FAIA240360",
    },
    {
        "authors": "K. S. Jishnu and B. Arthi",
        "title": "Real-time phishing URL detection framework using knowledge distilled ELECTRA",
        "venue": "Automatika",
        "year": "2024",
        "url": "https://doi.org/10.1080/00051144.2024.2415797",
    },
    {
        "authors": "Q. E. ul Haq, M. H. Faheem, I. Ahmad, K. Saleem, J. Al-Muhtadi, and A. Alharthi",
        "title": "Detecting Phishing URLs Based on a Deep Learning Approach to Prevent Cyber-Attacks",
        "venue": "Applied Sciences",
        "year": "2024",
        "url": "https://doi.org/10.3390/app142210086",
    },
    {
        "authors": "A. Ozcan, C. Catal, E. Donmez, and B. Senturk",
        "title": "A hybrid DNN-LSTM model for detecting phishing URLs",
        "venue": "Neural Computing and Applications",
        "year": "2021",
        "url": "https://doi.org/10.1007/s00521-021-06401-z",
    },
    {
        "authors": "S. S. Roy, A. I. Awad, L. A. Amare, M. T. Erkihun, and M. Anas",
        "title": "Multimodel Phishing URL Detection Using LSTM, Bidirectional LSTM, and GRU Models",
        "venue": "Future Internet",
        "year": "2022",
        "url": "https://doi.org/10.3390/fi14110340",
    },
    {
        "authors": "Z. Alshingiti, R. Alaqel, J. Al-Muhtadi, Q. E. ul Haq, K. Saleem, and M. H. Faheem",
        "title": "A Deep Learning-Based Phishing Detection System Using CNN, LSTM, and LSTM-CNN",
        "venue": "Electronics",
        "year": "2023",
        "url": "https://doi.org/10.3390/electronics12010232",
    },
    {
        "authors": "L. Tang and Q. H. Mahmoud",
        "title": "A Deep Learning-Based Framework for Phishing Website Detection",
        "venue": "IEEE Access",
        "year": "2022",
        "url": "https://doi.org/10.1109/ACCESS.2021.3137636",
    },
    {
        "authors": "S. Asiri, Y. Xiao, and T. Li",
        "title": "PhishTransformer: A Novel Approach to Detect Phishing Attacks Using URL Collection and Transformer",
        "venue": "Electronics",
        "year": "2023",
        "url": "https://doi.org/10.3390/electronics13010030",
    },
    {
        "authors": "S. Y. Yerima and M. K. Alzaylaee",
        "title": "High Accuracy Phishing Detection Based on Convolutional Neural Networks",
        "venue": "ICCAIS",
        "year": "2020",
        "url": "https://doi.org/10.1109/ICCAIS48893.2020.9096869",
    },
    {
        "authors": "R. Patgiri, A. Biswas, and S. Nayak",
        "title": "deepBF: Malicious URL detection using learned Bloom Filter and evolutionary deep learning",
        "venue": "Computer Communications",
        "year": "2023",
        "url": "https://doi.org/10.1016/j.comcom.2022.12.027",
    },
    {
        "authors": "S. Abdelnabi, K. Krombholz, and M. Fritz",
        "title": "VisualPhishNet: Zero-Day Phishing Website Detection by Visual Similarity",
        "venue": "ACM CCS",
        "year": "2020",
        "url": "https://doi.org/10.1145/3372297.3417233",
    },
    {
        "authors": "J.-L. Chen, Y.-W. Ma, and K.-L. Huang",
        "title": "Intelligent Visual Similarity-Based Phishing Websites Detection",
        "venue": "Symmetry",
        "year": "2020",
        "url": "https://doi.org/10.3390/sym12101681",
    },
    {
        "authors": "M.-E. Maurer and D. Herzner",
        "title": "Using visual website similarity for phishing detection and reporting",
        "venue": "CHI Extended Abstracts",
        "year": "2012",
        "url": "https://doi.org/10.1145/2212776.2223683",
    },
    {
        "authors": "E. Medvet, E. Kirda, and C. Kruegel",
        "title": "Visual-similarity-based phishing detection",
        "venue": "SecureComm",
        "year": "2008",
        "url": "https://doi.org/10.1145/1460877.1460905",
    },
    {
        "authors": "I. Corona, B. Biggio, M. Contini, L. Piras, R. Corda, and M. Mereu",
        "title": "DeltaPhish: Detecting Phishing Webpages in Compromised Websites",
        "venue": "Lecture Notes in Computer Science",
        "year": "2017",
        "url": "https://doi.org/10.1007/978-3-319-66402-6_22",
    },
    {
        "authors": "Y. Ding, N. Luktarhan, K. Li, and W. Slamu",
        "title": "A keyword-based combination approach for detecting phishing webpages",
        "venue": "Computers & Security",
        "year": "2019",
        "url": "https://doi.org/10.1016/j.cose.2019.03.018",
    },
    {
        "authors": "Y. Zhang, J. Hong, and L. Cranor",
        "title": "CANTINA: A Content-Based Approach to Detecting Phishing Web Sites",
        "venue": "WWW",
        "year": "2007",
        "url": "https://www.cs.cmu.edu/~jasonh/publications/www2007-cantina-final.pdf",
    },
    {
        "authors": "G. Xiang, J. Hong, C. P. Rose, and L. Cranor",
        "title": "CANTINA+: A Feature-Rich Machine Learning Framework for Detecting Phishing Web Sites",
        "venue": "CMU technical manuscript",
        "year": "2011",
        "url": "https://www.cs.cmu.edu/~jasonh/publications/acmtissec2011-cantina-journal-submitted-v2.pdf",
    },
    {
        "authors": "M. He, S.-J. Horng, P. Fan, M. K. Khan, and others",
        "title": "An efficient phishing webpage detector",
        "venue": "Expert Systems with Applications",
        "year": "2011",
        "url": "https://doi.org/10.1016/j.eswa.2011.01.046",
    },
    {
        "authors": "P. A. Barraclough, G. Fehringer, and J. Woodward",
        "title": "Intelligent cyber-phishing detection for online",
        "venue": "Computers & Security",
        "year": "2021",
        "url": "https://doi.org/10.1016/j.cose.2020.102123",
    },
    {
        "authors": "N. Reyes-Dorta, P. Caballero-Gil, and C. Rosa-Remedios",
        "title": "Detection of malicious URLs using machine learning",
        "venue": "Wireless Networks",
        "year": "2024",
        "url": "https://doi.org/10.1007/s11276-024-03700-w",
    },
]


def cite(*nums: int) -> str:
    return "[" + ", ".join(str(n) for n in nums) + "]"


def load_project_data() -> dict:
    df = pd.read_csv(DATASET_PATH, usecols=["URL", "Label"])
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    counts = df["Label"].value_counts().to_dict()
    total = len(df)
    good = int(counts.get("good", 0))
    bad = int(counts.get("bad", 0))
    avg_len = float(df["URL"].astype(str).str.len().mean())
    median_len = float(df["URL"].astype(str).str.len().median())
    good_support = int(metrics["classification_report"]["good"]["support"])
    bad_support = int(metrics["classification_report"]["bad"]["support"])
    bad_precision = float(metrics["classification_report"]["bad"]["precision"])
    bad_recall = float(metrics["classification_report"]["bad"]["recall"])
    tp_bad = round(bad_support * bad_recall)
    fn_bad = bad_support - tp_bad
    fp_bad = round(tp_bad * (1 / bad_precision - 1))
    tn_good = good_support - fp_bad
    return {
        "total_rows": total,
        "good_rows": good,
        "bad_rows": bad,
        "good_pct": 100 * good / total,
        "bad_pct": 100 * bad / total,
        "avg_len": avg_len,
        "median_len": median_len,
        "accuracy": metrics["accuracy"],
        "roc_auc": metrics["roc_auc"],
        "good_precision": metrics["classification_report"]["good"]["precision"],
        "good_recall": metrics["classification_report"]["good"]["recall"],
        "good_f1": metrics["classification_report"]["good"]["f1-score"],
        "bad_precision": bad_precision,
        "bad_recall": bad_recall,
        "bad_f1": metrics["classification_report"]["bad"]["f1-score"],
        "weighted_f1": metrics["classification_report"]["weighted avg"]["f1-score"],
        "macro_f1": metrics["classification_report"]["macro avg"]["f1-score"],
        "test_rows": metrics["classification_report"]["accuracy"],
        "feature_names": metrics["feature_names"],
        "tp_bad": tp_bad,
        "fn_bad": fn_bad,
        "fp_bad": fp_bad,
        "tn_good": tn_good,
    }


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=12.3,
            leading=18.8,
            alignment=TA_JUSTIFY,
            spaceAfter=9,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading1"],
            fontName="Times-Bold",
            fontSize=16,
            leading=20,
            spaceBefore=10,
            spaceAfter=10,
            textColor=colors.black,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitle",
            parent=styles["Heading2"],
            fontName="Times-Bold",
            fontSize=13,
            leading=17,
            spaceBefore=6,
            spaceAfter=6,
            textColor=colors.black,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CenterTitle",
            parent=styles["Title"],
            fontName="Times-Bold",
            fontSize=20,
            alignment=TA_CENTER,
            leading=24,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CenterBody",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=12.3,
            leading=18.8,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Caption",
            parent=styles["BodyText"],
            fontName="Times-Italic",
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#555555"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Reference",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=10.2,
            leading=14.5,
            alignment=TA_JUSTIFY,
            leftIndent=12,
            firstLineIndent=-12,
            spaceAfter=4,
        )
    )
    return styles


def paragraph_block(story, text: str, style):
    for chunk in text.strip().split("\n\n"):
        story.append(Paragraph(chunk.strip(), style))


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawRightString(A4[0] - 1.5 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def reference_note(ref: dict) -> str:
    title = ref["title"].lower()
    venue = ref["venue"]
    if "survey" in title or "review" in title or "state of the art" in title:
        return (
            f'This reference is used in the paper to frame the broader scholarship around phishing detection and to justify the taxonomy adopted in the literature review. '
            f'Its value for the current project lies in synthesizing prior methods, evaluation concerns, and open problems that help position a lightweight URL-based baseline within the wider field. '
            f'The paper is cited whenever the discussion turns to trends, categories of defenses, or unresolved methodological issues.'
        )
    if "benchmark" in title or "dataset" in title or "trusted across diverse datasets" in title or "adaptation" in title:
        return (
            f'This study is especially relevant to the reproducibility argument of the major project because it foregrounds dataset choice, transferability, or cross-corpus validity. '
            f'In the research paper it supports the claim that phishing results must be interpreted cautiously when datasets, label semantics, or feature spaces differ. '
            f'It also motivates the paper’s explicit reporting of class balance, feature construction, and local evaluation setup.'
        )
    if "visual" in title or "delta" in title:
        return (
            f'This paper is referenced in the discussion of attacks that cannot be reliably captured by lexical URL features alone. '
            f'Its importance for the present project is that it illustrates how screenshot analysis, visual similarity, or compromised-site inspection can detect phishing pages that look legitimate at the URL level. '
            f'The major project uses it to explain why the rebuilt model should be treated as a first-stage detector rather than a full anti-phishing platform.'
        )
    if "transformer" in title or "electra" in title or "lstm" in title or "cnn" in title or "deep learning" in title or "deepbf" in title:
        return (
            f'This reference contributes to the deep-learning side of the literature survey and helps contrast neural sequence models with the project’s simpler gradient boosting baseline. '
            f'In the paper it is used to show that more expressive models can learn richer URL patterns or sequence dependencies, but often with higher training and deployment complexity. '
            f'That contrast is central to explaining why the implemented project favors a reproducible tabular pipeline.'
        )
    if "graph" in title or "network-based" in title:
        return (
            f'This work is used to discuss robustness under evasive phishing behavior, where attackers deliberately craft URLs that look benign in isolation. '
            f'It matters for the project because it shows that relational evidence from infrastructure or graph context can recover signals that handcrafted lexical features may miss. '
            f'The paper cites it when identifying realistic future extensions beyond URL-only classification.'
        )
    if "html" in title or "content" in title or "keyword" in title or "cantina" in title:
        return (
            f'This reference supports the sections comparing lexical-only methods with content-based and hybrid phishing detection frameworks. '
            f'Its relevance to the project is that it demonstrates what becomes possible once page text, hyperlinks, DOM structure, or feature-rich filtering logic are added to URL evidence. '
            f'The research paper uses it to explain why the current model is fast and portable, but not as context-rich as stronger hybrid systems.'
        )
    return (
        f'This paper is cited as part of the empirical and methodological context for phishing URL detection in machine learning. '
        f'Within the major-project research paper, it helps establish how researchers have approached feature engineering, classifier design, or deployment trade-offs in {venue}. '
        f'It is particularly useful for comparing the rebuilt local system with existing approaches that target the same problem from a different modeling or systems perspective.'
    )


def feature_note(feature: str) -> str:
    notes = {
        "url_length": "Long URLs often embed tracking tokens, redirects, random identifiers, or fake directory structures. In the paper this feature is interpreted as a coarse but effective proxy for attack complexity and obfuscation, especially when combined with entropy and delimiter counts.",
        "hostname_length": "Hostnames that are unusually long can signal impersonation, typo-squatting, or deep brand stuffing. The project uses this feature to separate compact legitimate hosts from stretched phishing domains that attempt to look official by adding many lexical fragments.",
        "path_length": "Phishing URLs frequently move the deception into the path rather than the host, especially on compromised infrastructure. A long path can therefore indicate staged credential traps, fake login folders, or multi-hop redirection scaffolding.",
        "query_length": "The query string often carries session bait, billing references, or fake account tokens. Measuring its length provides a lightweight way to model whether the attacker is relying on parameter-heavy URLs to simulate legitimate web workflows.",
        "num_dots": "Dot count is a simple but durable cue because phishing URLs often exploit deep host segmentation and long filename-like suffixes. In isolation the signal is weak, but in combination it helps distinguish compact benign domains from structurally noisy ones.",
        "num_hyphens": "Hyphens are common in brand spoofing and token stitching because they allow attackers to concatenate words that mimic trusted services. This feature is especially useful when phishing pages include terms such as secure-login-update in the visible URL.",
        "num_slashes": "Slash count approximates path nesting and redirect complexity. Very deep paths can indicate copied site structures, compromised hosting directories, or landing-page chains that try to hide the phishing form behind plausible folders.",
        "num_digits": "Digits can appear in legitimate URLs, but phishing links often overuse them for account lures, fake transaction IDs, or random-looking tokens. Counting digits helps capture numeric noise that is hard for purely rule-based filters to contextualize.",
        "num_special_chars": "A high concentration of punctuation and separators often reflects obfuscation or encoding tricks. This feature provides a broad summary of URL complexity without requiring the model to inspect every symbol separately.",
        "has_at_symbol": "The at-sign remains a classic confusion technique because everything before it can visually mimic a trusted destination while the true host appears later. Its presence is therefore treated as a strong suspicious cue in the project.",
        "uses_ip_address": "Direct IP usage bypasses memorable domain names and is still common in opportunistic phishing campaigns. This feature is valuable because many benign consumer-facing services rarely present raw IPv4 destinations to end users.",
        "subdomain_count": "Deep subdomain chains can be used to front-load trusted brand names before the real registered domain. The project uses this signal to capture domain disguise strategies that exploit users’ tendency to read URLs from left to right.",
        "has_https": "HTTPS is no longer a marker of legitimacy, but it still contributes information when interpreted alongside other signals. In the rebuilt model it functions as one weak cue among many rather than as a trust label by itself.",
        "url_entropy": "Entropy estimates how irregular or random the character sequence is. High-entropy URLs can indicate generated strings, hidden tokens, or obfuscation, which is why the feature is frequently discussed in research on malicious URL detection.",
        "suspicious_keyword_hits": "Words such as login, verify, secure, account, password, and billing directly reflect common phishing lures. This feature gives the model a compact semantic view of credential-oriented language without needing a large language pipeline.",
        "brand_misuse": "Brand terms appearing outside the registered domain often indicate impersonation. This feature tries to capture exactly that pattern by asking whether a well-known brand appears in the broader URL while the actual host belongs elsewhere.",
        "has_port": "Explicit ports are uncommon in ordinary browsing but can appear in attacker-controlled services or nonstandard hosting setups. The feature is weak on its own but useful as part of a broader structural fingerprint.",
        "num_query_params": "Credential-harvesting and tracking flows often rely on multiple query parameters to preserve fake state. Counting parameters offers a simple way to quantify that behavior without parsing application semantics in depth.",
        "has_fragment": "Fragments can be used innocuously, but they also contribute to overly engineered or deceptive URLs. Including them makes the feature set slightly more robust to anchor-based tricks and unusual routing patterns.",
    }
    return notes[feature]


def flowchart_drawing() -> Drawing:
    d = Drawing(480, 220)
    palette = {
        "data": colors.HexColor("#d8ecff"),
        "proc": colors.HexColor("#dff4e5"),
        "model": colors.HexColor("#fff0c9"),
        "out": colors.HexColor("#ffe1df"),
        "stroke": colors.HexColor("#335b74"),
    }
    boxes = [
        (20, 150, 90, 42, "Input Dataset", palette["data"]),
        (145, 150, 95, 42, "Cleaning and\nLabel Mapping", palette["proc"]),
        (275, 150, 95, 42, "Feature\nEngineering", palette["proc"]),
        (20, 65, 90, 42, "Train/Test\nSplit", palette["proc"]),
        (145, 65, 95, 42, "HistGradient\nBoosting", palette["model"]),
        (275, 65, 95, 42, "Metrics and\nModel Bundle", palette["out"]),
        (400, 108, 60, 42, "URL\nPrediction", palette["out"]),
    ]
    for x, y, w, h, label, fill in boxes:
        d.add(Rect(x, y, w, h, rx=8, ry=8, fillColor=fill, strokeColor=palette["stroke"], strokeWidth=1.2))
        for idx, line in enumerate(label.split("\n")):
            d.add(String(x + w / 2, y + h / 2 + 7 - (idx * 12), line, fontName="Helvetica-Bold", fontSize=10, textAnchor="middle", fillColor=palette["stroke"]))
    arrows = [
        ((110, 171), (145, 171)),
        ((240, 171), (275, 171)),
        ((322, 150), (322, 107)),
        ((110, 86), (145, 86)),
        ((240, 86), (275, 86)),
        ((370, 129), (400, 129)),
    ]
    for (x1, y1), (x2, y2) in arrows:
        d.add(Line(x1, y1, x2, y2, strokeColor=palette["stroke"], strokeWidth=1.3))
        d.add(Polygon([x2, y2, x2 - 6, y2 + 3, x2 - 6, y2 - 3], fillColor=palette["stroke"], strokeColor=palette["stroke"]))
    d.add(Line(65, 150, 65, 107, strokeColor=palette["stroke"], strokeWidth=1.3))
    d.add(Polygon([65, 107, 62, 113, 68, 113], fillColor=palette["stroke"], strokeColor=palette["stroke"]))
    return d


def feature_family_drawing() -> Drawing:
    d = Drawing(480, 220)
    groups = [
        ("Structural URL Features", 20, 130, colors.HexColor("#d6ebff"), ["length", "dots", "slashes", "hyphens", "digits"]),
        ("Host and Routing Features", 190, 130, colors.HexColor("#e4f7df"), ["IP usage", "subdomains", "ports", "HTTPS", "fragments"]),
        ("Statistical and Semantic Features", 360, 130, colors.HexColor("#fff1d6"), ["entropy", "keywords", "brand misuse", "query count"]),
    ]
    for title, x, y, fill, bullets in groups:
        d.add(Rect(x, y, 110, 72, rx=8, ry=8, fillColor=fill, strokeColor=colors.HexColor("#385b72"), strokeWidth=1))
        d.add(String(x + 55, y + 58, title, fontName="Helvetica-Bold", fontSize=9.5, textAnchor="middle", fillColor=colors.HexColor("#26475a")))
        for idx, item in enumerate(bullets):
            d.add(String(x + 10, y + 42 - idx * 10, f"- {item}", fontName="Helvetica", fontSize=8.5, fillColor=colors.HexColor("#26475a")))
    d.add(Rect(170, 24, 140, 54, rx=10, ry=10, fillColor=colors.HexColor("#ffe1df"), strokeColor=colors.HexColor("#385b72"), strokeWidth=1.2))
    d.add(String(240, 58, "Feature Vector", fontName="Helvetica-Bold", fontSize=11, textAnchor="middle", fillColor=colors.HexColor("#7a2f2b")))
    d.add(String(240, 42, "19 numeric signals", fontName="Helvetica", fontSize=10, textAnchor="middle", fillColor=colors.HexColor("#7a2f2b")))
    for x in (75, 245, 415):
        d.add(Line(x, 130, 240, 78, strokeColor=colors.HexColor("#385b72"), strokeWidth=1.1))
        d.add(Polygon([240, 78, 235, 83, 243, 84], fillColor=colors.HexColor("#385b72"), strokeColor=colors.HexColor("#385b72")))
    return d


def metrics_chart(stats: dict) -> Drawing:
    d = Drawing(450, 230)
    chart = VerticalBarChart()
    chart.x = 45
    chart.y = 45
    chart.height = 135
    chart.width = 340
    chart.data = [[
        round(stats["accuracy"] * 100, 2),
        round(stats["roc_auc"] * 100, 2),
        round(stats["good_f1"] * 100, 2),
        round(stats["bad_f1"] * 100, 2),
    ]]
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 20
    chart.categoryAxis.categoryNames = ["Accuracy", "ROC AUC", "Good F1", "Bad F1"]
    chart.categoryAxis.labels.boxAnchor = "n"
    chart.categoryAxis.labels.dy = -8
    chart.bars[0].fillColor = colors.HexColor("#4378a7")
    chart.bars[0].strokeColor = colors.HexColor("#274967")
    d.add(chart)
    d.add(String(220, 200, "Model Performance Summary", fontName="Helvetica-Bold", fontSize=12, textAnchor="middle", fillColor=colors.HexColor("#274967")))
    return d


def class_distribution_chart(stats: dict) -> Drawing:
    d = Drawing(450, 230)
    chart = VerticalBarChart()
    chart.x = 65
    chart.y = 45
    chart.height = 135
    chart.width = 280
    chart.data = [[stats["good_rows"], stats["bad_rows"]]]
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 450000
    chart.valueAxis.valueStep = 100000
    chart.categoryAxis.categoryNames = ["Good", "Bad"]
    chart.bars[0].fillColor = colors.HexColor("#69a36e")
    chart.bars[1].fillColor = colors.HexColor("#cc6b66")
    d.add(chart)
    d.add(String(205, 200, "Dataset Class Distribution", fontName="Helvetica-Bold", fontSize=12, textAnchor="middle", fillColor=colors.HexColor("#274967")))
    return d


def confusion_chart(stats: dict) -> Drawing:
    d = Drawing(450, 235)
    chart = VerticalBarChart()
    chart.x = 45
    chart.y = 45
    chart.height = 140
    chart.width = 340
    chart.data = [[stats["tp_bad"], stats["fn_bad"], stats["fp_bad"], stats["tn_good"]]]
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 80000
    chart.valueAxis.valueStep = 20000
    chart.categoryAxis.categoryNames = ["TP bad", "FN bad", "FP bad", "TN good"]
    chart.categoryAxis.labels.boxAnchor = "n"
    chart.categoryAxis.labels.dy = -8
    chart.bars[0].fillColor = colors.HexColor("#5c88b3")
    chart.bars[0].strokeColor = colors.HexColor("#2b4f73")
    d.add(chart)
    d.add(String(220, 205, "Approximate Confusion Outcome Counts", fontName="Helvetica-Bold", fontSize=12, textAnchor="middle", fillColor=colors.HexColor("#274967")))
    return d


def precision_recall_chart(stats: dict) -> Drawing:
    d = Drawing(450, 235)
    chart = VerticalBarChart()
    chart.x = 45
    chart.y = 45
    chart.height = 140
    chart.width = 340
    chart.data = [
        [round(stats["good_precision"] * 100, 2), round(stats["bad_precision"] * 100, 2)],
        [round(stats["good_recall"] * 100, 2), round(stats["bad_recall"] * 100, 2)],
    ]
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 20
    chart.categoryAxis.categoryNames = ["Good class", "Bad class"]
    chart.categoryAxis.labels.boxAnchor = "n"
    chart.categoryAxis.labels.dy = -8
    chart.bars[0].fillColor = colors.HexColor("#6fa96f")
    chart.bars[0].strokeColor = colors.HexColor("#3f6f40")
    chart.bars[1].fillColor = colors.HexColor("#d37a68")
    chart.bars[1].strokeColor = colors.HexColor("#8f493d")
    d.add(chart)
    d.add(String(220, 205, "Precision and Recall by Class", fontName="Helvetica-Bold", fontSize=12, textAnchor="middle", fillColor=colors.HexColor("#274967")))
    d.add(String(320, 188, "Green: Precision  Orange: Recall", fontName="Helvetica", fontSize=9, textAnchor="middle", fillColor=colors.HexColor("#555555")))
    return d


def literature_table(styles):
    body = ParagraphStyle(
        name="TableBody",
        parent=styles["Body"],
        fontName="Helvetica",
        fontSize=8.4,
        leading=10.4,
        alignment=TA_JUSTIFY,
        spaceAfter=0,
    )
    header = ParagraphStyle(
        name="TableHeader",
        parent=styles["Body"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=10.5,
        textColor=colors.white,
        spaceAfter=0,
    )
    raw_rows = [
        ["Paper", "Focus", "Signal Type", "Reported takeaway"],
        [
            "Bahaghighat et al. [5]",
            "Classical ML",
            "112 handcrafted lexical, host, and structural features",
            "XGBoost produced the strongest results in their comparison and showed that carefully engineered tabular features still compete strongly with more complex pipelines."
        ],
        [
            "Aljofey et al. [8]",
            "Hybrid ML",
            "URL, hyperlink structure, and HTML TF-IDF content signals",
            "Their results showed that combining URL evidence with page-level features improved robustness and reduced dependence on external blacklist services."
        ],
        [
            "Rao and Pais [12]",
            "Random forest family",
            "URL, source-code, and third-party service features",
            "Random forest and PCA-RF delivered strong zero-day phishing detection, highlighting the value of multi-source feature engineering."
        ],
        [
            "Nagy et al. [11]",
            "Comparative study",
            "Website indicators and URL-derived handcrafted features",
            "The paper offered a broad side-by-side analysis of sequential and parallel ML workflows rather than relying on a single favorite classifier."
        ],
        [
            "Xu [18]",
            "Transformer",
            "Character-level URL sequence modeling with attention",
            "Attention-based models learned phishing patterns directly from URL text and reduced the need for manually assembled lexical rules."
        ],
        [
            "Kim et al. [19]",
            "Robustness",
            "Network and relational context around URLs and hosts",
            "Graph-aware context improved resilience against evasive URLs that appear benign when inspected only as isolated strings."
        ],
        [
            "Ozcan et al. [25]",
            "Hybrid deep learning",
            "URL sequence features captured by DNN and LSTM layers",
            "Their DNN-LSTM combination modeled both local character patterns and longer sequential dependencies in phishing URLs."
        ],
        [
            "Abdelnabi et al. [32]",
            "Visual similarity",
            "Screenshot and image-based website representations",
            "Visual matching was particularly effective for zero-day phishing pages that imitate trusted brands without obviously suspicious URLs."
        ],
        [
            "Zhang et al. [37]",
            "Content retrieval",
            "TF-IDF webpage text and search-oriented content cues",
            "CANTINA established an influential early content-based baseline and showed the value of page text for phishing identification."
        ],
        [
            "Xiang et al. [38]",
            "Feature-rich framework",
            "DOM, search-engine, and external service features",
            "Layered filtering logic helped reduce false positives while preserving strong recall, making CANTINA+ a classic hybrid reference."
        ],
    ]
    rows = []
    for row_index, row in enumerate(raw_rows):
        style = header if row_index == 0 else body
        rows.append([Paragraph(cell, style) for cell in row])
    table = Table(rows, colWidths=[3.6 * cm, 2.6 * cm, 3.5 * cm, 7.3 * cm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17384e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7fbff")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f7fbff"), colors.HexColor("#edf5fb")]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#8aa7be")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def feature_table(stats: dict):
    descriptions = {
        "url_length": "Overall character count of the raw URL string.",
        "hostname_length": "Length of the parsed host name.",
        "path_length": "Number of characters in the path component.",
        "query_length": "Number of characters in the query string.",
        "num_dots": "Proxy for domain depth and sub-structure complexity.",
        "num_hyphens": "Captures token obfuscation and spoof-like patterns.",
        "num_slashes": "Signals deep path nesting or redirect chains.",
        "num_digits": "Detects account IDs, random tokens, and numeric bait.",
        "num_special_chars": "Aggregates punctuation and encoded structure.",
        "has_at_symbol": "Flags URL confusion through userinfo-like syntax.",
        "uses_ip_address": "Captures direct IP hosting instead of domain names.",
        "subdomain_count": "Measures host fragmentation and disguise depth.",
        "has_https": "Signals transport protection, though not legitimacy alone.",
        "url_entropy": "Measures lexical randomness and character disorder.",
        "suspicious_keyword_hits": "Counts terms such as login, verify, secure, and billing.",
        "brand_misuse": "Indicates brand mentions that do not match the registered domain.",
        "has_port": "Detects explicit ports often used by nonstandard hosts.",
        "num_query_params": "Reflects parameter-heavy credential capture workflows.",
        "has_fragment": "Captures anchor-based obfuscation or redirect tricks.",
    }
    rows = [["Feature", "Role in the classifier"]]
    for feature in stats["feature_names"]:
        rows.append([feature, descriptions.get(feature, "Feature retained in the final model.")])
    table = Table(rows, colWidths=[4.7 * cm, 11.7 * cm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#244a63")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f8fc")]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9bb3c5")),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def build_story(stats: dict, styles):
    story = []
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("Design and Evaluation of a Machine Learning-Based Phishing URL Detection System Using Lexical Feature Engineering", styles["CenterTitle"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Research Paper Based on the Implemented Major Project", styles["CenterBody"]))
    story.append(Paragraph("Prepared from the working project in the Desktop folder and grounded in the supplied phishing URL dataset.", styles["CenterBody"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("Abstract", styles["SubTitle"]))
    abstract = f"""
    Phishing remains one of the most persistent delivery mechanisms for credential theft, financial fraud, and broader cyber intrusion campaigns. Prior work shows that blacklist systems alone are insufficient because they lag behind newly created or obfuscated phishing URLs, while many high-performing academic systems depend on expensive webpage rendering, third-party services, or feature sets that are difficult to reproduce consistently {cite(1,2,4,8,12,14)}. This paper presents a project-centered study built around a fully functioning phishing URL detection system implemented from the supplied source code and dataset. The resulting system uses lightweight lexical and host-derived features extracted directly from the URL string, a reproducible supervised learning pipeline, and a histogram-based gradient boosting classifier trained on {stats["total_rows"]:,} labeled URLs.

    The dataset copied into the project contains {stats["good_rows"]:,} benign URLs and {stats["bad_rows"]:,} phishing URLs, producing a class distribution of {stats["good_pct"]:.2f}% good and {stats["bad_pct"]:.2f}% bad. Nineteen numeric features were engineered from structural, semantic, and statistical properties of URLs, including entropy, subdomain depth, suspicious keyword counts, brand misuse indicators, IP address usage, and query complexity. The trained model achieved an accuracy of {stats["accuracy"]:.4f}, a ROC AUC of {stats["roc_auc"]:.4f}, a weighted F1-score of {stats["weighted_f1"]:.4f}, and a phishing-class F1-score of {stats["bad_f1"]:.4f} on the held-out test split. These results show that a compact lexical pipeline can still provide practical screening performance, although it remains less expressive than hybrid systems that combine URL, DOM, content, and network intelligence {cite(5,8,13,19,32,38)}.

    Beyond reporting the implementation, this paper synthesizes more than forty online research papers to position the project within the current literature. The discussion demonstrates that the project is best understood as a low-dependency baseline with strong deployability, quick inference, and good reproducibility, but with known limitations under domain compromise, HTTPS abuse, brand-new evasive campaigns, and visual mimicry attacks. The paper concludes by outlining concrete extensions such as richer content extraction, adversarial evaluation, model explainability, domain adaptation, graph reasoning, and browser-integrated defenses {cite(14,15,18,19,20,23,29,32)}.
    """
    paragraph_block(story, abstract, styles["Body"])
    abstract_extension = f"""
    In addition to these technical findings, the study highlights an important academic point: a major project in cybersecurity should be evaluated not only by whether a classifier works, but also by whether the surrounding workflow is reproducible, inspectable, and defensible. The present system satisfies that requirement by exposing clear scripts for training, prediction, and controlled dataset update while preserving the feature contract between all stages of the pipeline. This makes the project suitable for demonstration, discussion, and further extension in a research setting.

    The work also reinforces the argument that lightweight phishing detection remains useful despite the growing popularity of deep multimodal models. A compact URL-based classifier can act as an efficient screening layer that filters suspicious links before more expensive analysis is applied. For educational environments, prototype systems, and resource-limited deployments, such a design offers a strong balance between interpretability, speed, and practical value {cite(16,18,19,23,29)}. The broader significance of the project therefore lies not only in the reported metrics but also in showing how a well-structured baseline can serve as a credible foundation for future anti-phishing research.
    """
    paragraph_block(story, abstract_extension, styles["Body"])
    story.append(Paragraph("Keywords: phishing URL detection, lexical features, machine learning, cybersecurity, gradient boosting, malicious URL classification, phishing website detection", styles["Body"]))
    story.append(PageBreak())

    story.append(Paragraph("1. Introduction", styles["SectionTitle"]))
    intro = f"""
    Phishing is both a social engineering attack and a scalable technical workflow. The attacker creates or hijacks a destination, frames it as trustworthy, and pushes victims toward it through email, messaging, social posts, advertisements, or compromised sites. The URL is therefore not merely an address; it is often the first observable artifact in the attack chain. This explains why URL-focused detection remains attractive in both research and practice. A detector that can classify a suspicious link before the page loads can reduce risk earlier, lower runtime overhead, and avoid exposing the client to drive-by content or malicious scripts {cite(1,4,7,16,17)}.

    The literature nonetheless shows that URL-based detection is a difficult problem. Some phishing URLs are noisy and obvious, using IP addresses, excessive subdomains, long query strings, or keywords such as login and verify. Others are deliberately crafted to look benign, borrowing trusted domains, abusing HTTPS, relying on compromised servers, or using short lexical forms that evade simple heuristics {cite(6,14,19,24,35,36)}. In response, researchers have explored a wide spectrum of defenses: lists and reputation services, heuristic rules, visual similarity, content analysis, machine learning, deep learning, transfer learning, and graph-based reasoning {cite(3,4,8,18,19,20,31,32,37,38,39,40)}.

    The project examined in this paper originated from incomplete source files in which the training and prediction pipeline was not fully functional. Broken imports, incompatible function signatures, hard-coded paths, and missing model files prevented the original code from running reliably. The project was therefore re-engineered into a working Python system with a clear folder structure, a reproducible training script, a prediction script, a dataset update utility, and a saved model bundle. The redesigned system intentionally emphasizes low friction: it works with the user-provided dataset, avoids unavailable dependencies such as external parsing packages, and keeps the feature engineering local to the URL string and host information.

    This practical orientation motivates the main research question of the paper: <b>How effective is a lightweight, lexical-feature-based phishing URL detection pipeline when rebuilt as a reproducible end-to-end machine learning system on the supplied dataset, and how does its behavior compare with the broader anti-phishing literature?</b> Three sub-questions follow. First, which feature families are most defensible for a simple deployable baseline? Second, how well does the resulting model perform on a large dataset with realistic label imbalance? Third, what limitations remain when the system is compared with richer content-based, graph-based, and deep learning approaches?

    The significance of the study lies in its bridge between project implementation and research synthesis. Many student and prototype systems either remain purely conceptual or report performance without connecting design choices to the literature. Conversely, many surveys review large numbers of papers without grounding the discussion in an actual reproducible project. This paper does both. It documents a functioning major-project implementation and uses the surrounding literature to interpret what the observed performance means, where the design is strong, where it is weak, and what a rational next version should include {cite(1,2,3,4,11,13,15)}.
    """
    paragraph_block(story, intro, styles["Body"])

    story.append(Paragraph("2. Literature Review", styles["SectionTitle"]))
    lit_overview = f"""
    The anti-phishing literature can be organized into four broad families. The first includes list-based systems, which rely on blacklists, whitelists, and reputation services. These approaches are computationally cheap but react poorly to zero-day URLs. The second family focuses on lexical URL analysis, using patterns such as token count, delimiters, suspicious terms, host depth, and entropy. The third family examines webpage content, DOM structure, hyperlinks, search engine results, SSL clues, or other context once the page is loaded. The fourth family includes visual, neural, transfer-learning, and graph-based approaches that seek better generalization against sophisticated attacks {cite(1,3,4,18,19,24,31,32,39,40)}.

    Surveys remain useful because they expose recurring trade-offs. Sahoo et al. describe malicious URL detection as a machine learning problem shaped by feature representation, model choice, and system constraints {cite(1)}. Hannousse and Yahiouche argue that reproducible phishing research depends heavily on dataset construction choices, which often differ across studies and complicate direct comparison {cite(2)}. Safi and Singh similarly show that the field contains many high-accuracy claims, but not all use comparable data, evaluation rules, or operational assumptions {cite(3)}. Castano et al. refine the picture by distinguishing content-based and hybrid systems, noting that stronger performance often comes with higher runtime cost and more dependencies {cite(4)}.
    """
    paragraph_block(story, lit_overview, styles["Body"])

    story.append(Paragraph("URL-Based and Feature-Engineered Detection", styles["SubTitle"]))
    url_lit = f"""
    URL-based phishing detection is attractive because it can operate before page rendering. Bahaghighat et al. report strong performance from classical supervised learners trained on a large handcrafted feature set, with XGBoost outperforming other baselines {cite(5)}. Ahammad et al. also show that machine learning methods remain competitive on phishing URL tasks when feature construction is thoughtful and evaluation is systematic {cite(6)}. Gupta et al. propose a lexical machine learning method for real-time operation and emphasize that early-stage URL screening is practical when features are local and cheap to compute {cite(7)}.

    Other studies go further by blending URL features with auxiliary evidence. Rao and Pais extract features from URL structure, source code, and third-party services, reporting very strong random forest results and explicit comparison with CANTINA and CANTINA+ baselines {cite(12)}. Butnaru et al. advocate lightweight URL-based phishing detection for operational environments where speed and privacy matter more than maximal feature richness {cite(16)}. Tupsamudre et al. show that strong URL naming patterns alone can carry substantial predictive information, especially when the system is designed to focus on lexical structure rather than site rendering {cite(17)}.

    The main lesson from this body of work is that URL-only systems are still relevant, but their ceiling depends on whether the dataset contains sufficiently informative lexical clues. When URLs become short, semantically clean, or hosted on compromised infrastructure, URL-only methods lose context that richer systems can exploit {cite(1,4,14,19,35)}. The project in this paper therefore adopts the URL-only family deliberately, not because it is theoretically complete, but because it offers a realistic baseline with minimal runtime friction.
    """
    paragraph_block(story, url_lit, styles["Body"])

    story.append(Paragraph("Hybrid, HTML, and Content-Based Methods", styles["SubTitle"]))
    hybrid_lit = f"""
    Hybrid systems address the contextual blind spots of URL-only models. Aljofey et al. combine URL character information, hyperlink relationships, and textual content, showing that careful integration of URL and HTML features can outperform weaker baselines without relying on third-party services {cite(8)}. Barraclough et al. also frame phishing detection as a richer knowledge problem, combining blacklist-based, content-based, and heuristic evidence to improve overall judgment {cite(40)}. The keyword-based combination method of Ding et al. demonstrates that content cues can correct weaknesses in purely lexical reasoning, especially when page text reflects a targeted brand or service workflow {cite(36)}.

    Historically, CANTINA and CANTINA+ remain landmark systems in this space. CANTINA used TF-IDF signals from page content to detect phishing sites and reported strong early performance, especially compared with then-popular toolbars {cite(37)}. CANTINA+ extended the idea by layering DOM, search-engine, and third-party-service features with filtering logic to reduce false positives, becoming one of the most cited feature-rich frameworks in phishing research {cite(38)}. Later work such as He et al. continued the trend by mixing multiple feature sources to reduce weaknesses that appear when any single evidence stream is treated as sufficient {cite(39)}.

    These hybrid approaches matter for interpreting the current project. They remind us that the implemented model is intentionally narrower than many state-of-the-art academic systems. It does not inspect page HTML, JavaScript, hyperlinks, screenshots, or domain reputation feeds. As a result, it gains speed and simplicity but gives up the extra context that often pushes accuracy beyond URL-only baselines {cite(4,8,12,36,37,38)}.
    """
    paragraph_block(story, hybrid_lit, styles["Body"])

    story.append(Paragraph("Deep Learning, Sequence Models, and Transformers", styles["SubTitle"]))
    dl_lit = f"""
    Deep learning research on phishing URLs has expanded rapidly. Hybrid DNN-LSTM models, multimodel recurrent networks, convolutional neural networks, and attention-based transformers all attempt to learn phishing patterns directly from URL sequences or jointly from URL and webpage artifacts {cite(21,25,26,27,28,29,30)}. Xu reports that a transformer model can outperform classical baselines by learning long-range dependencies in character sequences {cite(18)}. Ozcan et al. show that a DNN-LSTM combination can exploit both local patterns and sequential context {cite(25)}, while Roy et al. compare multiple recurrent architectures on phishing URL detection and illustrate how model choice affects generalization {cite(26)}.

    More recent work pushes toward browser-ready or real-time deployment. Jishnu and Arthi propose knowledge-distilled ELECTRA for instant user-facing phishing alerts {cite(23)}. Lai et al. combine natural language processing with deep learning to enrich URL-based classification {cite(22)}. Haq et al. apply one-dimensional CNNs to phishing URLs and position deep learning as a way to reduce manual feature dependence {cite(24)}. Tang and Mahmoud present a broader deep learning framework for phishing website detection, showing how neural approaches can absorb richer feature representations when compute budget allows {cite(28)}.

    Yet deep learning is not automatically superior in every setting. Many sequence models require larger compute budgets, more careful regularization, and more extensive hyperparameter tuning than classical tree ensembles. Their practical advantage is greatest when the deployment context supports heavier inference or when the dataset contains subtle sequential patterns that simple handcrafted features cannot capture. For a lightweight student project designed to be runnable from a standard local Python environment, a gradient boosting model remains easier to reproduce and inspect, even if it leaves some performance on the table {cite(1,14,21,23,25,29)}.
    """
    paragraph_block(story, dl_lit, styles["Body"])

    story.append(Paragraph("Robustness, Graph Methods, and Adversarial Concerns", styles["SubTitle"]))
    robust_lit = f"""
    One weakness of many phishing detectors is that they overfit superficial regularities. Kim et al. argue that attackers can intentionally manipulate URL patterns to resemble benign links, and therefore propose a network-based approach that reasons over shared infrastructure and neighboring entities rather than only over visible tokens {cite(19)}. Guo et al. extend this line with graph-based inference and loopy belief propagation, showing that relational context can improve efficiency and robustness in the face of evasive URLs {cite(20)}. Rashid et al. focus on generalization across datasets through unsupervised domain adaptation, highlighting how strong performance on one corpus may not transfer cleanly to another {cite(14)}.

    Explainability studies reinforce the same concern. Shafin proposes an explainable feature-selection framework to identify the most useful phishing features, while Mia et al. explicitly ask whether phishing URL features can be trusted across diverse datasets and use explainable AI to examine feature stability {cite(13,15)}. These studies are especially relevant to the present project because our features were designed for portability rather than exhaustive coverage. They are useful features, but they are not guaranteed to be universally reliable. Dataset shift remains a real risk.
    """
    paragraph_block(story, robust_lit, styles["Body"])

    story.append(Paragraph("Visual Similarity and Zero-Day Phishing", styles["SubTitle"]))
    visual_lit = f"""
    Visual phishing remains one of the clearest challenges for URL-only systems. Attackers can host visually convincing copies of trusted sites on domains that do not necessarily look suspicious. Medvet et al. and Maurer and Herzner provide early visual-similarity frameworks, while Chen et al. and Abdelnabi et al. extend the idea using stronger image-based representations and deep neural visual matching {cite(33,34,35,32)}. DeltaPhish addresses a particularly important scenario: phishing pages hidden inside compromised legitimate websites, where the domain itself may not look suspicious and the page can only be distinguished by internal visual or structural deviations {cite(35)}.

    This stream of work clarifies what the current project does not do. It cannot verify screenshots, logos, style templates, form semantics, or compromised-site inconsistencies. Therefore, a polished credential-harvesting page on a benign-looking host may still evade lexical defenses. The project should thus be interpreted as a screening system, not a complete anti-phishing platform {cite(4,19,32,35)}.
    """
    paragraph_block(story, visual_lit, styles["Body"])
    story.append(literature_table(styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Table 1. Representative literature grouped by detection focus and signal family.", styles["Caption"]))

    story.append(Paragraph("Gaps Identified in the Literature", styles["SubTitle"]))
    gaps = f"""
    Despite impressive results in many papers, three gaps remain visible. First, evaluation is fragmented. Datasets differ in source, age, duplicate handling, feature availability, and label semantics, making it hazardous to compare raw percentages across papers {cite(1,2,3,14,15)}. Second, practical deployment often trails reported accuracy. Systems that require webpage rendering, third-party lookups, or large neural stacks may be less attractive in constrained environments despite strong benchmark performance {cite(4,8,16,23)}. Third, robustness to data shift and intentional evasion remains a leading concern, especially for feature-based models that can be gamed once their signals are understood {cite(14,15,19,20)}.

    The project described here responds to these gaps by choosing a transparent baseline. Instead of claiming to solve phishing in a universal sense, it focuses on reproducibility, low dependency overhead, measurable performance on a supplied dataset, and a clear path for future extension. This makes the project suitable for educational use, rapid prototyping, and local experimentation, while also making its limitations explicit.
    """
    paragraph_block(story, gaps, styles["Body"])
    story.append(PageBreak())

    story.append(Paragraph("3. Methodology", styles["SectionTitle"]))
    methodology_intro = f"""
    The methodology was organized around turning incomplete project code into a functioning, reproducible, and evaluable machine learning system. The implementation is centered in a Desktop folder called <i>major project</i> and includes training, prediction, dataset update, and feature-engineering modules. The workflow is intentionally reproducible: data are loaded from a local CSV file, labels are mapped deterministically, features are derived without remote services, and model artifacts are written to the local project folder.
    """
    paragraph_block(story, methodology_intro, styles["Body"])
    story.append(flowchart_drawing())
    story.append(Paragraph("Figure 1. End-to-end workflow of the implemented phishing URL detection project.", styles["Caption"]))

    story.append(Paragraph("Research Design", styles["SubTitle"]))
    research_design = f"""
    This study follows an applied experimental design. The primary artifact is a working phishing URL detector built from the supplied project files and dataset. The design combines software re-engineering with quantitative model evaluation. It is not a purely exploratory literature review, nor is it a purely theoretical machine learning paper. Instead, it operates at the intersection of implementation and empirical assessment. The study first reconstructs a functioning system, then evaluates it with standard classification metrics, and finally interprets the findings through the lens of prior phishing research {cite(1,3,4,11)}.

    The practical reconstruction step was necessary because the source archive contained several operational inconsistencies: one script imported a nonexistent module name, another expected a different function signature, and both relied on machine-specific hard-coded model paths. Additionally, a dependency used in the original logic was unavailable in the target environment. The final project therefore reimplemented feature extraction using standard library parsing and locally available packages while preserving the core task of phishing URL classification.
    """
    paragraph_block(story, research_design, styles["Body"])

    story.append(Paragraph("Data Collection and Dataset Description", styles["SubTitle"]))
    data_desc = f"""
    The project uses the user-supplied CSV file <i>phishing_site_urls.csv</i>. The dataset contains {stats["total_rows"]:,} rows and two columns: URL and Label. Labels were represented as strings, with <i>good</i> for benign URLs and <i>bad</i> for phishing URLs. No synthetic data were added. Null rows were removed, labels were normalized to lowercase, and the binary mapping <i>good</i> = 0 and <i>bad</i> = 1 was applied before training.

    The dataset is imbalanced but not severely skewed: {stats["good_rows"]:,} rows ({stats["good_pct"]:.2f}%) are benign, while {stats["bad_rows"]:,} rows ({stats["bad_pct"]:.2f}%) are phishing. The average URL length is {stats["avg_len"]:.2f} characters and the median length is {stats["median_len"]:.2f} characters. These statistics indicate a dataset large enough to support a robust supervised baseline while also reflecting the practical class imbalance typical of phishing detection tasks {cite(2,5,6,14)}.
    """
    paragraph_block(story, data_desc, styles["Body"])
    story.append(class_distribution_chart(stats))
    story.append(Paragraph("Figure 2. Label distribution in the supplied dataset after import into the rebuilt project.", styles["Caption"]))

    story.append(Paragraph("Feature Engineering", styles["SubTitle"]))
    feature_desc = f"""
    The final system extracts nineteen numerical features from each URL. The design follows the phishing literature on lightweight lexical analysis, especially the repeated observation that URL structure alone can carry meaningful evidence about phishing intent {cite(6,7,16,17)}. The features fall into three broad families.

    Structural features measure length, punctuation density, and path complexity. These include total URL length, number of dots, slashes, hyphens, digits, and special characters. Host and routing features capture whether the URL uses a direct IP address, how many subdomains exist, whether an explicit port is specified, whether HTTPS is present, and whether a fragment is used. Statistical and semantic features estimate entropy, suspicious keyword count, brand misuse, and number of query parameters. Together these features model both low-level lexical oddities and higher-level phishing cues such as identity confusion and credential-oriented phrasing.

    Two design decisions were especially important. First, the parser was hardened to handle malformed URLs, including cases that trigger parsing errors under strict standard-library behavior. This matters because phishing corpora often include intentionally irregular strings. Second, the implementation avoided dependencies on external services such as WHOIS, search engines, or page rendering. This keeps the pipeline fast and self-contained but necessarily limits the available evidence compared with hybrid frameworks like CANTINA+ or URL+HTML systems {cite(8,12,37,38)}.
    """
    paragraph_block(story, feature_desc, styles["Body"])
    story.append(feature_family_drawing())
    story.append(Paragraph("Figure 3. Feature families used in the implemented model.", styles["Caption"]))
    story.append(feature_table(stats))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 2. Feature set used by the deployed model in the rebuilt project.", styles["Caption"]))

    story.append(Paragraph("Model Selection and Training Procedure", styles["SubTitle"]))
    model_desc = f"""
    The selected classifier is <i>HistGradientBoostingClassifier</i>, a tree-based ensemble method that is efficient on large tabular datasets and performs well when feature interactions are nonlinear. This choice is consistent with the broader literature showing that tree ensembles and boosting methods remain highly competitive for phishing detection tasks when the input is a structured feature matrix {cite(5,10,11,12,13)}. The model was configured with a learning rate of 0.08, maximum depth of 8, 220 boosting iterations, and a minimum leaf size of 30. These values were chosen to provide a strong baseline without extensive hyperparameter search.

    The dataset was partitioned using an 80/20 train-test split with stratification by label, preserving the class ratio in both partitions. Features were computed for the full corpus and then split into training and evaluation matrices. After fitting, the model and its feature ordering were saved into a joblib bundle so that the prediction script could reproduce the exact training schema.

    This model choice reflects a practical compromise. More expressive deep models exist and often achieve stronger performance in controlled benchmarks {cite(18,22,23,24,25,26,27,28,29,30,31)}, but a histogram-based boosting model offers simpler training, fast inference, modest memory overhead, and good stability on tabular inputs. For a deployable major project whose purpose is both educational and functional, those advantages are material.
    """
    paragraph_block(story, model_desc, styles["Body"])

    story.append(Paragraph("Evaluation Metrics", styles["SubTitle"]))
    metrics_desc = """
    The study reports accuracy, ROC AUC, precision, recall, and F1-score. Accuracy is useful as a broad measure, but it can overstate performance in imbalanced datasets. ROC AUC captures ranking quality across thresholds. Precision indicates how many URLs flagged as phishing are actually phishing, while recall measures how many phishing URLs are successfully found. F1-score balances precision and recall and is therefore especially important for phishing detection, where both missed attacks and excessive false alarms can be costly.

    Because the positive class in this project is the phishing label, phishing-class recall and phishing-class F1-score are emphasized in the results and discussion. This follows the operational reality that a detector should not be judged only by overall accuracy; it must also be judged by how consistently it catches dangerous links without overwhelming the user with false positives.
    """
    paragraph_block(story, metrics_desc, styles["Body"])

    story.append(Paragraph("Reproducibility and Output Artifacts", styles["SubTitle"]))
    reproducibility = """
    The rebuilt project exposes three command-line entry points. The training script reads the CSV data, builds features, trains the model, evaluates the held-out split, and writes a model bundle and JSON metrics file. The prediction script loads the bundle, computes the same feature vector for a new URL, and outputs the predicted class and phishing probability. The dataset-update script appends a URL to the dataset only when model confidence crosses a configurable threshold. Together these scripts make the system reproducible, inspectable, and usable from a standard development environment such as Visual Studio Code.

    Reproducibility is important here not only as a software engineering convenience but also as a research quality requirement. In phishing detection studies, small mismatches in preprocessing can silently invalidate comparisons. For example, differences in label mapping, URL normalization, malformed-string handling, or feature ordering between training and inference can produce apparently correct scripts that nonetheless evaluate a different problem. The present project avoids that failure mode by centralizing the feature engineering logic inside a shared source module and by saving the learned feature order alongside the trained model bundle. This means the prediction workflow reuses the exact representation that was available during training rather than rebuilding an approximate version later.

    The output artifacts also support project extension. The saved `joblib` model bundle can be loaded by other interfaces such as a small Flask service, a desktop GUI, or a browser-integrated checker without retraining the classifier each time. The metrics JSON can be archived across runs so that successive experiments with new thresholds, additional features, or alternative classifiers remain comparable. In a thesis or viva setting, this is useful because it allows the student to demonstrate not only one static result but also a controlled experimental workflow in which each model version is tied to explicit evidence.

    Another practical advantage of the current artifact design is auditability. Because the system stores the feature names and evaluation outputs explicitly, a reviewer can inspect what the model expects, reproduce the train-test cycle, and trace how a new URL is transformed before classification. That level of transparency is especially valuable for cybersecurity applications, where black-box behavior can reduce trust. Even though the model itself is a boosting ensemble rather than a simple linear equation, the surrounding pipeline remains transparent enough to support debugging, classroom explanation, and incremental improvement.
    """
    paragraph_block(story, reproducibility, styles["Body"])
    story.append(PageBreak())

    story.append(Paragraph("4. Results", styles["SectionTitle"]))
    results_intro = f"""
    The full-dataset training run completed successfully after the project was restructured. The resulting model bundle was saved in the local <i>models</i> directory, and a separate metrics file recorded the final evaluation outputs. The measured results are strong enough to validate the rebuilt pipeline as a functioning phishing URL detector, while still leaving room for improvement relative to richer systems reported in the literature.
    """
    paragraph_block(story, results_intro, styles["Body"])

    story.append(Paragraph("Quantitative Performance", styles["SubTitle"]))
    quant_results = f"""
    On the held-out test set, the system achieved an accuracy of {stats["accuracy"]:.4f} and a ROC AUC of {stats["roc_auc"]:.4f}. For benign URLs, precision was {stats["good_precision"]:.4f}, recall was {stats["good_recall"]:.4f}, and F1-score was {stats["good_f1"]:.4f}. For phishing URLs, precision was {stats["bad_precision"]:.4f}, recall was {stats["bad_recall"]:.4f}, and F1-score was {stats["bad_f1"]:.4f}. The weighted F1-score was {stats["weighted_f1"]:.4f}, while the macro F1-score was {stats["macro_f1"]:.4f}.

    These results show a clear asymmetry. The model is especially strong at recognizing benign URLs, with high recall for the good class. It is still effective on the phishing class, but the phishing recall is noticeably lower than benign recall. This is consistent with the fact that some phishing URLs in the dataset likely look lexically ordinary and therefore are harder to separate without extra page, network, or visual context.
    """
    paragraph_block(story, quant_results, styles["Body"])
    story.append(metrics_chart(stats))
    story.append(Paragraph("Figure 4. Core evaluation metrics for the implemented model.", styles["Caption"]))
    story.append(precision_recall_chart(stats))
    story.append(Paragraph("Figure 5. Precision and recall comparison across the benign and phishing classes.", styles["Caption"]))

    result_table = Table(
        [
            ["Metric", "Value"],
            ["Accuracy", f"{stats['accuracy']:.4f}"],
            ["ROC AUC", f"{stats['roc_auc']:.4f}"],
            ["Good precision", f"{stats['good_precision']:.4f}"],
            ["Good recall", f"{stats['good_recall']:.4f}"],
            ["Good F1-score", f"{stats['good_f1']:.4f}"],
            ["Bad precision", f"{stats['bad_precision']:.4f}"],
            ["Bad recall", f"{stats['bad_recall']:.4f}"],
            ["Bad F1-score", f"{stats['bad_f1']:.4f}"],
            ["Weighted F1-score", f"{stats['weighted_f1']:.4f}"],
            ["Macro F1-score", f"{stats['macro_f1']:.4f}"],
        ],
        colWidths=[7.5 * cm, 5 * cm],
    )
    result_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17384e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef5fa")]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#8aa7be")),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(result_table)
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 3. Held-out evaluation results for the final gradient boosting model.", styles["Caption"]))

    story.append(Paragraph("Confusion Pattern Analysis", styles["SubTitle"]))
    confusion_text = f"""
    A simple reconstruction of the confusion pattern from the saved metrics suggests approximately {stats["tp_bad"]:,} phishing URLs were correctly identified, {stats["fn_bad"]:,} phishing URLs were missed, {stats["fp_bad"]:,} benign URLs were incorrectly flagged as phishing, and about {stats["tn_good"]:,} benign URLs were correctly labeled as safe. The most important practical number here is the missed-phish count. While the model provides strong screening performance, there remains a nontrivial set of dangerous URLs whose lexical pattern was insufficiently distinct.

    This behavior is not surprising given the design of the feature space. When a phishing URL uses clean HTTPS, a plausible domain, moderate length, few suspicious terms, and no obvious delimiter abuse, a lexical model has limited evidence. The literature repeatedly shows that these edge cases often require HTML analysis, brand matching, screenshot comparison, or graph/network reasoning to classify reliably {cite(8,14,19,20,32,35)}.
    """
    paragraph_block(story, confusion_text, styles["Body"])
    story.append(confusion_chart(stats))
    story.append(Paragraph("Figure 6. Approximate confusion-outcome counts reconstructed from the saved evaluation report.", styles["Caption"]))

    story.append(Paragraph("Interpretation Against Prior Work", styles["SubTitle"]))
    comparison = f"""
    The model's performance is credible but not state of the art, and this is an important strength rather than a weakness in interpretation. Several published systems report higher accuracy, including high-performing random forest, XGBoost, and feature-rich hybrid systems {cite(5,8,12)}. Some deep learning studies also report stronger results by learning sequence patterns or combining multiple evidence streams {cite(18,23,24,25,26,27,28,29,30)}. However, those systems often use richer features, stronger compute assumptions, additional preprocessing, or different datasets.

    By comparison, the present project operates with nineteen directly computed features and no dependency on search engines, WHOIS, page rendering, screenshots, or browser extensions. In that context, an accuracy near 0.90 and a ROC AUC above 0.94 are meaningful. The project therefore compares favorably not as a maximal benchmark chaser, but as a portable baseline that can be run, understood, and extended by students or practitioners without specialized infrastructure.
    """
    paragraph_block(story, comparison, styles["Body"])

    story.append(Paragraph("Practical Demonstration", styles["SubTitle"]))
    practical = """
    During validation, the prediction script correctly classified an OpenAI developer URL as benign with a phishing probability of approximately 0.21, demonstrating that the rebuilt CLI workflow functions correctly in a realistic user scenario. The project also successfully recognized a strongly suspicious test URL containing an IP address, an at-sign, and billing-themed wording as phishing with very high confidence. While such demonstrations are anecdotal rather than statistically central, they confirm that the local workflow from training to inference is operational.

    These practical checks are worth documenting because major-project evaluation often considers usability alongside raw model accuracy. A classifier may report strong metrics in isolation yet still fail as a project artifact if the surrounding workflow is brittle or difficult to run. In this case, the rebuilt implementation supports a straightforward sequence of actions: the user trains the model, observes the saved artifacts, executes a prediction command against a live URL example, and optionally updates the dataset through a confidence-gated utility. Each of those steps succeeded in the target local environment, which suggests the project is not only theoretically valid but operationally demonstrable.

    The demonstration phase also reveals how the model behaves qualitatively. Benign-looking URLs with clean HTTPS usage, ordinary host structure, and no obvious phishing keywords are generally assigned lower phishing probabilities, while suspicious URLs containing IP addresses, delimiter abuse, and credential-themed wording trigger much higher risk estimates. This pattern is consistent with the intended feature design discussed earlier in the methodology chapter. It also offers a useful sanity check: the model appears to be responding to semantically reasonable cues rather than producing arbitrary output.

    From a presentation perspective, these examples can be used effectively in a report defense or classroom demonstration. Showing both a benign and a suspicious URL allows the examiner to connect the abstract evaluation metrics with visible feature behavior. The value of this exercise is not that two examples prove correctness, but that they make the system’s reasoning more concrete for human reviewers who may not be satisfied with percentages alone.
    """
    paragraph_block(story, practical, styles["Body"])
    story.append(PageBreak())

    story.append(Paragraph("5. Discussion", styles["SectionTitle"]))
    discussion = f"""
    The discussion centers on what the rebuilt project contributes and what it does not. Its main contribution is not the invention of a novel phishing algorithm. Rather, its contribution lies in converting fragmented starter code into a functioning end-to-end system, grounding that system in a large real dataset, and evaluating it honestly against the contemporary literature. This is pedagogically and practically significant. A large portion of anti-phishing work is difficult to reproduce because of unavailable datasets, proprietary feeds, or hidden preprocessing assumptions. In contrast, this project can be executed locally from a standard editor and terminal.

    The model also demonstrates that handcrafted lexical features still matter. Much recent work emphasizes deep learning, transformers, or graph reasoning {cite(18,19,20,23,24,25,26,27,28,29,31,32)}. Those directions are important, but the results here confirm that interpretable URL-derived signals remain effective enough to justify their use in screening layers, browser plug-ins, educational tools, and local batch triage. Features such as entropy, suspicious keywords, IP address usage, and subdomain depth continue to encode useful information about phishing behavior.

    At the same time, the project's limitations should be stated clearly. First, the dataset labels reduce the problem to binary good or bad classes, while real-world malicious URLs may include malware, spam, defacement, scam landing pages, and mixed intent. Second, the features are entirely lexical or host-derived. The detector does not inspect HTML forms, document structure, JavaScript, screenshot similarity, certificate chains, or infrastructure relationships. Third, the evaluation uses a single train-test split on a single dataset; it therefore does not prove cross-dataset robustness. Fourth, because phishing evolves quickly, performance on future campaigns may drift unless retraining and validation are repeated {cite(2,14,15,19,20)}.

    There is also an ethical dimension. A phishing detector is a safety tool, but it can create a false sense of security if presented as perfect. The appropriate framing is assistive rather than absolute. Users should treat the model as an additional signal, not as a substitute for secure browsing habits or domain verification. This is consistent with the broader research record, which shows that phishing defense is most reliable when technical detection, interface cues, training, and policy controls reinforce each other {cite(3,4,37,38,40)}.
    """
    paragraph_block(story, discussion, styles["Body"])

    story.append(Paragraph("Implications for System Design", styles["SubTitle"]))
    implications = """
    For system designers, the project suggests a layered architecture. A lightweight lexical classifier can serve as the first gate because it is cheap, privacy-preserving, and easy to deploy. URLs with high suspicion scores can then be escalated to more expensive checks such as HTML parsing, screenshot similarity, domain-reputation lookup, or graph-based contextual analysis. This mirrors the architectural direction of many successful studies, which combine fast initial signals with richer second-stage inspection {cite(8,19,20,32,35,38)}.

    The rebuilt project is therefore best interpreted as layer one of a future anti-phishing stack. It already offers a useful first-pass classifier. Its value grows further when its outputs are fed into a larger decision pipeline rather than treated as the final verdict in every case.
    """
    paragraph_block(story, implications, styles["Body"])

    story.append(Paragraph("Limitations and Threats to Validity", styles["SubTitle"]))
    limitations_text = """
    Internal validity is influenced by the original dataset quality. Duplicate URLs, stale campaigns, or inconsistent labeling can inflate or depress results. Construct validity is limited by the feature set because phishing behavior is richer than URL syntax alone. External validity is limited because only one dataset and one main model family were evaluated. Finally, ecological validity is constrained because the model was tested offline on stored URLs rather than as a live browser extension facing streaming attacks.
    """
    paragraph_block(story, limitations_text, styles["Body"])
    threat_body = ParagraphStyle(
        name="ThreatBody",
        parent=styles["Body"],
        fontName="Helvetica",
        fontSize=8.3,
        leading=10.2,
        alignment=TA_JUSTIFY,
        spaceAfter=0,
    )
    threat_header = ParagraphStyle(
        name="ThreatHeader",
        parent=styles["Body"],
        fontName="Helvetica-Bold",
        fontSize=8.8,
        leading=10.2,
        textColor=colors.white,
        spaceAfter=0,
    )
    threat_rows = [
        ["Threat", "Why it matters", "Mitigation in this study"],
        ["Dataset shift", "URL patterns change over time and across sources, so a model that looks strong on one corpus may weaken when campaigns evolve.", "The paper explicitly interprets results as dataset-specific and cites adaptation literature instead of claiming universal generalization."],
        ["Feature incompleteness", "No HTML, screenshot, hyperlink, certificate, or graph context is used, which leaves blind spots for more subtle phishing pages.", "The system is framed as a lightweight baseline and the discussion clearly recommends richer multimodal extensions."],
        ["Single split evaluation", "Performance may vary under repeated resampling, time-based splits, or external validation datasets.", "Metrics are reported transparently and the limitations section warns against overgeneralizing from one held-out split."],
        ["Class imbalance", "Overall accuracy can hide missed phishing URLs if the benign class dominates the test set.", "Precision, recall, phishing-class F1-score, and ROC AUC are emphasized rather than accuracy alone."],
        ["Operational mismatch", "Offline experiments may differ from live browser deployment, where streaming attacks, latency, and user behavior matter.", "The workflow and future-work discussion identify deployment extensions and present the current model as an initial screening layer."],
    ]
    threat_table_rows = []
    for row_index, row in enumerate(threat_rows):
        style = threat_header if row_index == 0 else threat_body
        threat_table_rows.append([Paragraph(cell, style) for cell in row])
    threat_table = Table(
        threat_table_rows,
        colWidths=[2.8 * cm, 6.1 * cm, 7.0 * cm],
        repeatRows=1,
    )
    threat_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#244a63")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f8fc")]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9bb3c5")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(threat_table)
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 4. Main threats to validity and how they are addressed in the paper.", styles["Caption"]))

    story.append(Paragraph("Recommendations for Future Work", styles["SubTitle"]))
    future = f"""
    The strongest future improvement is to move from lexical-only detection toward staged multimodal detection. A reasonable next version would preserve the current URL classifier as a fast front-end, but add optional HTML extraction, favicon and screenshot similarity, and domain-level reputation features. Another high-value extension is model explainability. Because phishing tools may be used by analysts, students, or end users, the system would benefit from feature-level explanations or SHAP-style post hoc interpretation {cite(13,15)}.

    Domain adaptation and robustness testing are also essential. The literature increasingly warns that high scores on a single dataset do not guarantee durable performance elsewhere {cite(2,14,15)}. Future experiments should therefore include temporal splits, cross-dataset evaluation, and adversarial perturbation tests. On the modeling side, transformer and graph-based methods offer promising directions for cases in which handcrafted features are too weak {cite(18,19,20,23,29)}. Finally, the software itself could be extended into a graphical desktop utility, a browser extension, or a small web service for live URL scanning.
    """
    paragraph_block(story, future, styles["Body"])
    future_extension = f"""
    A particularly productive follow-up study would be to compare layered deployment strategies instead of only comparing individual classifiers. For example, the present lexical model could be retained as a first-pass filter that scores every URL quickly, while a second stage is invoked only for moderately risky or highly uncertain cases. That second stage could include HTML form analysis, screenshot matching, certificate inspection, or graph-based infrastructure reasoning. Measuring the combined effect of such a cascade would provide a more operationally realistic contribution than reporting isolated model scores alone. It would also align the project more closely with the layered defense philosophies discussed in the broader phishing literature {cite(4,8,19,20,32,38)}.

    Another avenue for improvement lies in richer experimental reporting. Future versions of the project could include threshold-sweep analysis, precision-recall curves, ablation studies, and feature-importance summaries so that readers can better understand which signals contribute most strongly to classification. This would deepen the explanatory value of the project and make it easier to compare the current handcrafted feature set with alternative representations such as character embeddings or sequence tokens. Such reporting is especially useful in academic settings because it shows not only that the system works, but also how and why it works.

    There is also room for human-centered improvement. If the project evolves into an end-user tool, the warning interface will matter almost as much as the model itself. Future work could therefore examine how phishing probabilities, highlighted risk cues, and explanatory messages should be presented to users so that they support better decisions without creating fatigue or confusion. This would connect the technical classifier more directly with practical cybersecurity usability, an area that remains important in real-world anti-phishing deployment.
    """
    paragraph_block(story, future_extension, styles["Body"])
    story.append(PageBreak())

    story.append(Paragraph("6. Conclusion", styles["SectionTitle"]))
    conclusion = f"""
    This paper presented a research-grounded study of a rebuilt phishing URL detection project based on the user-supplied dataset and repaired source code. The final system is fully functional, trains locally, predicts new URLs, and stores reusable model artifacts. Its architecture is intentionally lightweight: nineteen numerical URL features feed a histogram-based gradient boosting classifier that achieved an accuracy of {stats["accuracy"]:.4f} and ROC AUC of {stats["roc_auc"]:.4f} on a large held-out evaluation split.

    The literature review showed that the project belongs to the longstanding URL-based anti-phishing tradition while standing in contrast to newer hybrid, graph-based, and deep learning systems. This is not a drawback when interpreted correctly. The project offers a reproducible, low-dependency, fast-to-run baseline that is useful for learning, prototyping, and first-stage screening. At the same time, the paper acknowledges that richer context is needed for visually convincing or infrastructure-savvy phishing campaigns.

    In summary, the project succeeds as a solid major-project implementation and as a meaningful research case study. It demonstrates how a working system can be built from imperfect starter code, evaluated responsibly, and situated within the broader scientific conversation on phishing detection. The most important contribution is therefore methodological clarity: a simple system can still be valuable when its assumptions are explicit, its results are reproducible, and its limitations are honestly discussed.
    """
    paragraph_block(story, conclusion, styles["Body"])

    closing_note = """
    For that reason, the project should be seen as both a finished academic artifact and a foundation for further cybersecurity experimentation. It already demonstrates the essential lifecycle of a real machine learning security tool: data preparation, feature extraction, model training, evaluation, artifact storage, and practical inference on new inputs. That end-to-end completeness is one of the strongest outcomes of the work and distinguishes the project from narrower demonstrations that stop at isolated code fragments or partial notebooks.
    """
    paragraph_block(story, closing_note, styles["Body"])

    story.append(Paragraph("Appendix A. Implementation Snapshot", styles["SectionTitle"]))
    appendix_a = """
    The final project folder contains the following main files: <i>train.py</i> for training, <i>predict.py</i> for single-URL inference, <i>update_dataset.py</i> for confidence-gated dataset extension, and a <i>src</i> package containing URL feature extraction and model I/O utilities. The project also stores the copied dataset under the <i>data</i> directory and writes the trained model and metrics JSON into the <i>models</i> directory.

    From a software engineering perspective, the most important improvement over the original codebase is cohesion. File paths are relative to the project root, the feature contract is shared between training and prediction, malformed URLs are handled safely, and the runtime behavior can be reproduced from a standard Visual Studio Code terminal. This implementation discipline is especially important in machine learning projects, where small inconsistencies in preprocessing or feature order can invalidate results.
    """
    paragraph_block(story, appendix_a, styles["Body"])

    story.append(Paragraph("Appendix B. Suggested Extension Roadmap", styles["SectionTitle"]))
    appendix_b = """
    A practical roadmap for extending the project can be staged as follows. Stage one: add model explanation outputs for each prediction so users can see why a URL was flagged. Stage two: create a browser-ready or Flask-based interface that wraps the existing model bundle. Stage three: add HTML and hyperlink parsing as optional second-stage inspection. Stage four: evaluate on multiple external datasets and time-split scenarios. Stage five: experiment with transformer or graph-based methods while keeping the current lexical model as a baseline.

    This staged roadmap respects both engineering reality and research progression. It avoids jumping directly to complex models before the baseline has been documented, measured, and understood. That sequencing follows good scientific practice and makes future comparison more meaningful.
    """
    paragraph_block(story, appendix_b, styles["Body"])

    story.append(Paragraph("Appendix C. Annotated Literature Notes", styles["SectionTitle"]))
    appendix_c_intro = """
    This appendix provides short annotations for each reference used in the paper. The goal is twofold: first, to show how the cited papers informed the interpretation of the project, and second, to make the bibliography more useful for future extension of the system. These notes are not full reviews of each paper, but they summarize why each work matters to the logic of the present study.
    """
    paragraph_block(story, appendix_c_intro, styles["Body"])
    for idx, ref in enumerate(REFERENCES, start=1):
        story.append(Paragraph(f'[{idx}] <b>{ref["title"]}</b>', styles["SubTitle"]))
        story.append(Paragraph(reference_note(ref), styles["Body"]))

    story.append(Paragraph("Appendix D. Detailed Feature Interpretation", styles["SectionTitle"]))
    appendix_d_intro = """
    The major project relies on a relatively compact set of nineteen numerical features. Even though the final model is a boosted tree ensemble and therefore can learn nonlinear interactions automatically, it is still useful to explain each feature conceptually. This appendix expands on the feature table from the methodology chapter and connects each signal to plausible phishing behavior.
    """
    paragraph_block(story, appendix_d_intro, styles["Body"])
    for feature in stats["feature_names"]:
        story.append(Paragraph(feature.replace("_", " ").title(), styles["SubTitle"]))
        story.append(Paragraph(feature_note(feature), styles["Body"]))

    story.append(Paragraph("Appendix E. Replication and Experimentation Guide", styles["SectionTitle"]))
    appendix_e = f"""
    This appendix turns the research paper back into a practical project guide. The rebuilt system was designed so that a student can reproduce the main findings from a standard code editor and terminal. The first step is data placement. The dataset must remain in the <i>data</i> folder under the project root so that the training script can resolve it using relative paths rather than machine-specific absolute locations. During this study, the dataset contained {stats["total_rows"]:,} rows and preserved the original good and bad labels supplied by the user.

    The second step is training. Running the training script builds the full feature matrix, applies the binary label mapping, performs a stratified train-test split, trains the histogram-based gradient boosting model, and writes both the model bundle and the metrics JSON into the <i>models</i> directory. The training workflow is deterministic enough to serve as a stable baseline for later experimentation, though exact values can still vary if the dataset changes or if additional preprocessing is introduced.

    The third step is inference. The prediction script is intentionally narrow: it loads the saved model bundle, computes the same feature vector for a new URL, preserves the feature order used during training, and reports both the predicted class and the estimated phishing probability. This matters because machine learning projects often break when the training and inference pipelines drift apart. In this project, the shared feature contract avoids that error by keeping all feature logic inside the common source package.

    The fourth step is threshold management. The default prediction threshold is 0.5, which is appropriate for a balanced interpretation of the classifier output, but it is not the only sensible option. In a conservative organizational setting, one may prefer to lower the threshold slightly to catch more phishing URLs at the cost of higher false positives. In a user-facing browser assistant, a higher threshold may be preferred to avoid warning fatigue. This paper therefore treats thresholding as a deployment choice rather than a fixed scientific constant.

    The fifth step is controlled experimentation. A particularly useful exercise for students is feature ablation. One can remove individual features or feature families and retrain the model to estimate how much predictive signal each group contributes. For example, removing suspicious keyword counts and brand misuse tests the contribution of semantic cues. Removing entropy and punctuation-related features tests how much the model depends on statistical irregularity. Removing host-related features such as IP usage and subdomain count tests how much phishing behavior is encoded in hostname structure. Such ablation work would turn the project from a strong implementation study into a more analytical machine learning investigation.

    A second valuable experiment is threshold sweeping. Rather than reporting only one operating point, future users can compute precision-recall trade-offs across many thresholds and select the value that best matches their risk tolerance. This is especially important in phishing detection because the balance between missed attacks and false alarms is context dependent. A university lab, a personal browser assistant, and an enterprise gateway may all prefer different decision thresholds even when using the same underlying classifier.

    A third experiment is temporal evaluation. If the dataset can be timestamped or refreshed with newly observed URLs, the model should be evaluated across time rather than only through random splits. Temporal drift is one of the largest hidden weaknesses in phishing detection, because attackers adapt their tactics and infrastructure rapidly. A model that performs well on historical data may degrade when new campaigns use cleaner lexical forms, better domain camouflage, or compromised benign hosts. The literature repeatedly warns about this issue, and the major project would benefit from testing it directly {cite(2,14,15,19,20)}.

    A fourth experiment is cross-dataset validation. The current paper intentionally remains honest about its evidence: the model was trained and evaluated on the supplied dataset only. To strengthen external validity, future work should evaluate the same feature-engineering pipeline on other public phishing URL corpora, including corpora with multiclass labels such as benign, phishing, malware, and defacement. The resulting differences would reveal whether the model learns robust phishing structure or merely adapts to artifacts of the local dataset.

    A fifth experiment is interface integration. The current command-line workflow is excellent for reproducibility, but many users would benefit from a graphical wrapper. The same trained model could power a simple desktop form, a small Flask API, or a browser extension. The key engineering principle is to preserve the same feature extraction logic and model bundle so that deployment does not silently diverge from the validated research pipeline.
    """
    paragraph_block(story, appendix_e, styles["Body"])

    story.append(Paragraph("Appendix F. Extended Project-to-Literature Mapping", styles["SectionTitle"]))
    appendix_f = """
    A useful way to interpret the major project is to ask which parts of the literature it directly reflects and which parts it intentionally leaves out. It directly reflects the URL-based machine learning tradition. The feature set is rooted in the same class of evidence used by many lightweight phishing detectors: lexical structure, host complexity, suspicious tokens, entropy, and identity confusion. It also reflects the argument made in several papers that URL-only signals remain attractive because they can be computed before page rendering and without exposing the client to hostile content.

    The project only partially reflects the hybrid literature. It borrows the idea that multiple evidence families should be combined, but it applies that principle within the URL itself rather than across URL, HTML, DOM, and external intelligence. This is why the methodology chapter repeatedly describes the system as a compact baseline rather than a fully hybrid detector. If the project were extended with hyperlink features, HTML text features, and page-level consistency checks, it would move much closer to the hybrid systems discussed in the literature review.

    The project also only partially reflects the modern deep learning literature. It acknowledges the rise of sequence models, CNNs, LSTMs, transformers, and graph-based approaches, yet it chooses a simpler ensemble model for reasons of reproducibility and ease of deployment. This decision is defensible because the research objective here is not to outcompete every neural baseline, but to produce a working and interpretable system from the supplied materials. In that sense, the project functions as a bridge between classroom implementation and more advanced future research.

    Finally, the project deliberately excludes visual similarity and compromised-site detection, even though those areas are important. This exclusion is not accidental. It keeps the system operational within a local machine learning workflow and prevents the project from depending on rendering engines, screenshot pipelines, or large additional corpora. The literature review treats those omitted areas as the natural next stage of development, which is why they appear prominently in the recommendations for future work.
    """
    paragraph_block(story, appendix_f, styles["Body"])

    story.append(Paragraph("Appendix G. Operational Usage Notes", styles["SectionTitle"]))
    appendix_g = """
    For day-to-day use, the rebuilt project follows a simple cycle. The user opens the project folder in a development environment, trains the model when the dataset changes, tests candidate URLs with the prediction script, and optionally appends new URLs to the dataset only when model confidence is sufficiently high. This workflow makes the project usable not only as a research artifact but also as a small operational tool for classroom demonstration or personal experimentation.

    The command structure is intentionally minimal. Training is initiated through the training script, which writes both the model artifact and evaluation metrics. Prediction uses the saved artifact and accepts a target URL as input. Dataset update is gated by a threshold so that uncertain model outputs do not automatically contaminate the original CSV file. These operational details matter in a research setting because a paper is more convincing when the described system can actually be executed by another reader.

    One final operational recommendation is versioned experimentation. Whenever the model is retrained with a new dataset sample, feature set, or threshold policy, the corresponding metrics file should be archived alongside the model bundle. Doing so would turn the project into a small but disciplined research platform in which each run is reproducible, comparable, and easier to discuss in a thesis, viva, or project report.
    """
    paragraph_block(story, appendix_g, styles["Body"])

    story.append(Paragraph("References", styles["SectionTitle"]))
    for idx, ref in enumerate(REFERENCES, start=1):
        line = f'[{idx}] {ref["authors"]}, "{ref["title"]}," {ref["venue"]}, {ref["year"]}. Available: {ref["url"]}'
        story.append(Paragraph(line, styles["Reference"]))
    return story


def build_pdf():
    stats = load_project_data()
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )
    story = build_story(stats, styles)
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    build_pdf()
