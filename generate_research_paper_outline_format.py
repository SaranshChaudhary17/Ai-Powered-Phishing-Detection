from pathlib import Path

from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import generate_research_paper as base


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = PROJECT_ROOT / "major_project_research_paper_outline_format.pdf"


def add_section(story, title, body, styles):
    story.append(Paragraph(title, styles["SectionTitle"]))
    base.paragraph_block(story, body, styles["Body"])


def add_subsection(story, title, body, styles):
    story.append(Paragraph(title, styles["SubTitle"]))
    base.paragraph_block(story, body, styles["Body"])


def wrapped_table(rows, col_widths, styles, header_bg="#244a63", body_bg1="#ffffff", body_bg2="#f3f8fc", font_size=10.6, leading=13.2):
    table_body = base.ParagraphStyle(
        name=f"OutlineTableBody{len(rows)}{len(col_widths)}",
        parent=styles["Body"],
        fontName="Helvetica",
        fontSize=font_size,
        leading=leading,
        alignment=base.TA_JUSTIFY,
        spaceAfter=0,
    )
    table_header = base.ParagraphStyle(
        name=f"OutlineTableHeader{len(rows)}{len(col_widths)}",
        parent=styles["Body"],
        fontName="Helvetica-Bold",
        fontSize=font_size + 0.2,
        leading=leading,
        textColor=base.colors.white,
        spaceAfter=0,
    )
    parsed = []
    for i, row in enumerate(rows):
        style = table_header if i == 0 else table_body
        parsed.append([Paragraph(cell, style) for cell in row])
    table = Table(parsed, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), base.colors.HexColor(header_bg)),
        ("TEXTCOLOR", (0, 0), (-1, 0), base.colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [base.colors.HexColor(body_bg1), base.colors.HexColor(body_bg2)]),
        ("GRID", (0, 0), (-1, -1), 0.35, base.colors.HexColor("#9bb3c5")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def build_story(stats: dict, styles):
    styles["Body"].fontSize = 14.8
    styles["Body"].leading = 23.8
    styles["CenterBody"].fontSize = 14.0
    styles["CenterBody"].leading = 21.8
    styles["Reference"].fontSize = 13.2
    styles["Reference"].leading = 20.4
    styles["Reference"].spaceAfter = 8
    story = []
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("Design and Evaluation of a Machine Learning-Based Phishing URL Detection System Using Lexical Feature Engineering", styles["CenterTitle"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Outline-Formatted Research Paper Version", styles["CenterBody"]))
    story.append(Paragraph("Prepared in the exact major-section structure requested by the project outline.", styles["CenterBody"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("Abstract", styles["SubTitle"]))
    abstract = f"""
    This paper presents an outline-structured study of a phishing URL detection project rebuilt from incomplete starter code and evaluated on a large user-supplied dataset. The implemented system relies on lightweight lexical and host-derived features, a reproducible preprocessing pipeline, and a histogram-based gradient boosting classifier trained on {stats["total_rows"]:,} labeled URLs. The final model achieved an accuracy of {stats["accuracy"]:.4f}, ROC AUC of {stats["roc_auc"]:.4f}, and phishing-class F1-score of {stats["bad_f1"]:.4f}, indicating that compact tabular feature engineering remains a practical baseline for phishing screening {base.cite(1,5,8,12,19)}.

    The paper is intentionally organized to match a classical research outline consisting of Introduction, Literature Review, Methodology, Results, Discussion, Conclusion, and References. In addition to documenting the implementation, it synthesizes more than forty online research papers to position the project within the broader anti-phishing literature. The study concludes that the rebuilt system is academically defensible and operationally useful as a low-dependency baseline, while also identifying clear directions for richer multimodal, robust, and deployable future systems {base.cite(2,3,4,14,19,20,32,38)}.

    In a broader sense, the study demonstrates that strong project work in cybersecurity depends on disciplined integration across multiple layers. The code must run reliably, the feature engineering must remain consistent between training and inference, the evaluation must be interpretable, and the final research narrative must connect implementation choices to prior scholarship. By addressing all of these layers together, the paper turns a local machine learning project into a more complete research artifact that can be defended in both technical and academic terms.

    The rebuilt system is therefore valuable not only because of the metrics it reports, but also because of the workflow it establishes. A user can place the dataset in the project folder, train the model through a single script, inspect persisted metrics, and then apply the saved model to new URLs without modifying the underlying codebase. That continuity between experimentation and use is a central reason the project is suitable for a major research paper rather than only for a coding demonstration.
    """
    base.paragraph_block(story, abstract, styles["Body"])
    story.append(Paragraph("Keywords: phishing URL detection, lexical features, machine learning, cybersecurity, gradient boosting, malicious URL classification, phishing website detection", styles["Body"]))
    story.append(PageBreak())

    add_section(story, "I. Introduction", """
    Phishing remains one of the most persistent cybersecurity threats because it combines social engineering, deceptive interface design, and scalable web infrastructure abuse. Attackers increasingly use URLs as the first contact point through email, instant messaging, social media, paid advertisements, and compromised websites. For this reason, URL analysis continues to be one of the most useful first layers in phishing defense, especially in settings where early screening can prevent page rendering and user exposure.
    """, styles)

    add_subsection(story, "A. Background Information", f"""
    Phishing detection has evolved from blacklist-centered approaches toward a broad family of lexical, content-based, hybrid, visual, and deep learning systems {base.cite(1,3,4,37,38)}. While blacklists remain useful, they often respond too slowly to brand-new attacks. Lexical URL analysis emerged as a lightweight alternative because suspicious URLs frequently contain cues such as misleading tokens, excessive subdomains, IP addresses, entropy spikes, or credential-themed keywords. The rebuilt project in this paper follows that tradition by using nineteen numerical URL features that can be computed without browser rendering or external reputation services.

    From an operational viewpoint, phishing is attractive to attackers because it scales cheaply and adapts quickly. A single campaign can reuse domain registration tricks, compromised websites, mass emailing, and social engineering templates to reach large numbers of potential victims. Even when the payload changes from credential theft to payment fraud or malware delivery, the URL remains a critical early indicator. This is why URL-based detection continues to receive attention even in an era dominated by large-scale neural models. It addresses the security problem at the first observable technical artifact in the attack chain.

    The project studied in this paper emerged from a realistic educational context rather than a controlled research lab. The starting code was incomplete and inconsistent, yet it already embodied the central idea that phishing URLs can be classified through feature extraction and supervised learning. Rebuilding such a project is valuable because it demonstrates how cybersecurity knowledge becomes usable software. The resulting paper therefore treats implementation repair not as an incidental coding exercise, but as part of the methodological contribution of the study.
    """, styles)

    add_subsection(story, "B. Research Problem or Question", """
    The central research problem is whether a lightweight URL-based machine learning system, rebuilt from incomplete project code and trained on the supplied phishing URL dataset, can provide meaningful detection performance while remaining reproducible and operationally simple. The main research question is: how effective is this rebuilt lexical-feature-based detector, and how should its results be interpreted when compared with broader phishing detection research?

    This research problem can be divided into several smaller questions. First, which lexical and host-oriented signals remain useful enough to justify a low-dependency model in 2026, despite the rapid growth of hybrid and transformer-based systems? Second, how well does the reconstructed project perform on a dataset with more than half a million labeled URLs when evaluated through standard classification metrics? Third, what can be learned from the model’s limitations, particularly its difficulty with phishing URLs that are deliberately crafted to appear structurally ordinary?

    These questions matter because many project reports stop once a classifier produces a plausible number. In contrast, the present paper asks whether the model is meaningful, reproducible, and contextually justified. The goal is therefore not only to measure performance, but also to understand what kind of phishing detector this project really is and what role it could realistically play inside a layered cybersecurity workflow.
    """, styles)

    add_subsection(story, "C. Significance of the Research", """
    The significance of the study lies in its practical and academic value. Practically, it transforms a broken project into a working cybersecurity tool with train, predict, and controlled dataset-update workflows. Academically, it demonstrates how implementation choices, dataset construction, feature engineering, and evaluation strategy should be tied directly to the literature rather than treated as isolated coding decisions. This makes the paper useful both as a project report and as a research-grounded case study.

    The research is also significant because it focuses on reproducibility. Many machine learning security projects become difficult to defend academically when the preprocessing pipeline is opaque, the model path is hard-coded to one machine, or the feature logic differs between training and inference. By correcting those issues directly in the codebase and documenting the repairs inside the paper, the study shows that reproducibility itself is part of scientific rigor. In a major project setting, that kind of rigor can be as important as achieving a slightly higher benchmark score.

    Finally, the project matters as a baseline. In cybersecurity, baseline systems are not unimportant simply because they are simpler than state-of-the-art models. A well-documented baseline allows future work to measure improvement honestly. It also gives students and reviewers a transparent point of reference for understanding what richer systems gain and what they cost. The present study therefore contributes not only a functioning phishing detector, but also a defensible reference point for future extensions.
    """, styles)

    add_section(story, "II. Literature Review", """
    The anti-phishing literature can be divided into several interconnected streams: URL-based methods, content-based and hybrid approaches, deep learning systems, and robustness-oriented methods such as graph or domain-adaptation techniques. Together, these studies show that phishing detection is not a single-method problem but a layered design space shaped by data quality, runtime cost, and deployment constraints {base.cite(1,2,3,4,19,20,32)}.
    """, styles)

    add_subsection(story, "A. Overview of Relevant Literature", f"""
    Survey and benchmark studies provide the broadest context. Sahoo et al. review malicious URL detection as a machine learning problem shaped by feature representation and system constraints {base.cite(1)}. Hannousse and Yahiouche emphasize that dataset quality and comparability strongly influence reported results {base.cite(2)}. Safi and Singh synthesize phishing website detection techniques and note recurring issues in evaluation consistency {base.cite(3)}. Castano et al. distinguish content-based and hybrid systems and explain why stronger accuracy often comes with heavier dependencies {base.cite(4)}.

    Classical machine learning studies show that feature-engineered systems remain highly competitive. Bahaghighat et al. report strong XGBoost performance on a large curated dataset {base.cite(5)}, while Rao and Pais demonstrate that random-forest-based systems perform well when richer feature families are combined {base.cite(12)}. Hybrid approaches such as Aljofey et al. and the CANTINA lineage illustrate how URL evidence can be improved through HTML, DOM, or search-related features {base.cite(8,37,38)}. More recent work explores transformers, recurrent networks, and CNN variants to learn phishing patterns directly from URL or webpage sequences {base.cite(18,23,24,25,26,28,29)}.

    A second trend in the literature is the movement toward richer contextual awareness. Researchers increasingly argue that phishing should not be modeled as a purely lexical problem because attackers can host convincing phishing pages on compromised but otherwise reputable infrastructure. This has pushed the field toward screenshot comparison, page-content consistency checks, hyperlink analysis, and graph-based reasoning over domain and hosting relationships {base.cite(19,20,32,35)}. The present project does not implement those layers, but the literature review includes them because they define the broader environment in which a URL-based baseline should be judged.

    A third theme is the tension between deployability and maximum accuracy. Browser- or cloud-integrated systems can use external services and intensive page rendering to improve performance, but such systems may be slower, harder to reproduce, or less suitable for local educational environments. Several studies explicitly or implicitly navigate this trade-off by asking how much phishing detection can be achieved with cheaper signals alone {base.cite(7,16,17,23)}. The current project belongs squarely to that part of the research landscape.

    Taken together, the overview literature suggests that phishing detection should be thought of as a continuum rather than a single best method. At one end are extremely lightweight URL heuristics and blacklist systems. At the other end are computationally heavier multimodal or relational architectures. In between lies a wide range of classical and hybrid machine learning systems that offer different balances between interpretability, cost, and performance. The major project in this paper is positioned intentionally near the lightweight middle of that continuum: more systematic than a rule-only filter, but less infrastructure-heavy than a fully multimodal security platform.
    """, styles)

    add_subsection(story, "B. Key Theories or Concepts", """
    Three concepts are especially relevant to this project. The first is lexical feature engineering, which assumes that phishing behavior leaves structural traces in the URL string itself. The second is staged or layered detection, where cheap signals are used first and more expensive analysis is applied only when needed. The third is generalization: a detector should not only score well on one dataset, but also remain robust under data drift, adversarial change, or cross-dataset variation. These concepts shape the entire design and interpretation of the present system.

    Lexical feature engineering is rooted in the theory that attacker goals leak into the surface form of malicious URLs. Credential theft campaigns often require tokens such as login, verify, update, password, or billing to look convincing. Similarly, deceptive hosts may use brand terms in subdomains, numeric noise, long paths, or direct IP addresses to balance realism with operational convenience. The features in the current project are built around this theory. Even if each individual cue is weak, the combined pattern can become predictive when modeled through a nonlinear classifier.

    The layered-detection concept reflects a systems perspective rather than a purely algorithmic one. A first-stage model is not expected to solve every phishing problem by itself; it is expected to filter, rank, and escalate. In that sense, the project can be interpreted as a front-end screening component that could hand suspicious URLs to more expensive downstream modules. This theoretical framing is important because it prevents the evaluation from being overly harsh on the absence of HTML or screenshot analysis while still acknowledging those omissions as real limitations.

    Generalization theory enters because phishing is adversarial. Attackers adapt to the features defenders use. A model that works well on one dataset may partially fail when the distribution of URLs changes, when campaigns become cleaner-looking, or when compromised domains make malicious URLs resemble legitimate infrastructure. Research on transfer, domain adaptation, and explainable feature trustworthiness warns repeatedly that performance should be interpreted with this adversarial instability in mind {base.cite(14,15,19)}.

    A fourth concept relevant to the paper is explainability. Security systems often need to justify their decisions to developers, analysts, reviewers, or end users. Handcrafted features make explanation easier because the model’s inputs have semantic meaning: entropy, subdomain count, suspicious keyword hits, and brand misuse are all concepts that can be described in plain language. This does not make the model fully transparent, but it does make it more suitable for project defense and human-centered improvement than many opaque alternatives.
    """, styles)

    add_subsection(story, "C. Gaps or Controversies in the Literature", f"""
    The literature contains several important gaps. Reported metrics often come from non-identical datasets, making direct comparison difficult {base.cite(2,3,14,15)}. Some systems achieve excellent performance but rely on features or services that are expensive to deploy in local environments {base.cite(4,8,38)}. Others are strong on controlled data but may weaken when the URL distribution changes over time or when attackers deliberately craft cleaner-looking links {base.cite(14,19,20)}. These gaps justify the current project’s emphasis on reproducibility and honest interpretation rather than purely on maximum benchmark accuracy.

    Another controversy concerns how much trust should be placed in very high accuracy figures when the experimental design is not fully transparent. Some studies use balanced subsets, older datasets, or aggressive filtering that can simplify the classification task. Others do not clarify whether duplicate or near-duplicate URLs were removed before splitting the data. These choices can influence the apparent difficulty of the benchmark. The present paper therefore treats its own performance as meaningful but bounded evidence rather than as a universal claim of superiority.

    There is also a conceptual debate between interpretability and representational richness. Handcrafted feature systems are easier to explain and often easier to deploy, but they may miss subtle patterns that sequence models or visual similarity systems can capture. Conversely, richer models may perform better while being harder to debug, audit, or present clearly in a student project. This tension appears throughout the field and is directly relevant to the design trade-offs of the major project discussed here.

    A further gap concerns project reproducibility at the educational level. Many papers describe polished final systems, but there is less discussion of how incomplete academic projects can be repaired into working research artifacts. The current paper addresses that gap indirectly by documenting the reconstruction process as part of the methodology. This does not replace mainstream phishing research, but it adds a pedagogically useful dimension: it shows how research concepts become reliable project code.
    """, styles)
    story.append(base.literature_table(styles))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 1. Representative literature included in the review.", styles["Caption"]))
    literature_rows = [
        ["Theme", "Representative references", "Implication for this project"],
        ["Surveys and benchmarks", "Sahoo et al. [1], Hannousse and Yahiouche [2], Safi and Singh [3], Castano et al. [4]", "Support careful interpretation of metrics and justify the emphasis on reproducibility."],
        ["Classical ML baselines", "Bahaghighat et al. [5], Ahammad et al. [6], Rao and Pais [12]", "Show that feature-engineered systems remain strong comparison points."],
        ["Hybrid/content systems", "Aljofey et al. [8], Ding et al. [36], CANTINA [37], CANTINA+ [38]", "Illustrate what richer context can add beyond pure URL analysis."],
        ["Deep learning systems", "Xu [18], Jishnu and Arthi [23], Ozcan et al. [25], Tang and Mahmoud [28]", "Provide future directions when handcrafted features are not expressive enough."],
        ["Robustness and visual methods", "Kim et al. [19], Guo et al. [20], Abdelnabi et al. [32], DeltaPhish [35]", "Highlight failure modes of lexical-only systems and motivate layered defense."],
    ]
    synth = wrapped_table(literature_rows, [3.7 * cm, 6.1 * cm, 6.0 * cm], styles, header_bg="#1d445c", body_bg2="#eff5fa", font_size=10.4, leading=13.0)
    story.append(synth)
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 2. Literature synthesis matrix used to position the current project.", styles["Caption"]))
    story.append(PageBreak())

    add_section(story, "III. Methodology", """
    The methodology combines software reconstruction with supervised machine learning evaluation. The original project archive contained incomplete and inconsistent files, so the first methodological task was to rebuild the implementation into a coherent training and inference pipeline. The second task was to train and evaluate that pipeline using the supplied phishing URL dataset under a transparent experimental setup.
    """, styles)

    add_subsection(story, "A. Research Design", """
    This work follows an applied experimental design. It is not only a conceptual review of phishing detection, but a project-centered study in which code, data, features, and evaluation are all part of the evidence. The study therefore combines engineering repair, feature design, model training, quantitative testing, and literature-grounded interpretation.

    In practical terms, the research design includes two phases. The first phase is reconstruction: resolving broken imports, mismatched function signatures, hard-coded machine paths, and unavailable dependencies in the original archive. The second phase is controlled evaluation: training the repaired system on the supplied dataset, measuring performance on a held-out split, and interpreting the results in relation to the surrounding literature. This two-phase design is important because the final results are only meaningful once the implementation itself is stable and reproducible.

    The design is also intentionally transparent. Each major action in the project corresponds to an explicit script or output artifact. The training script generates the model and metrics. The prediction script demonstrates inference on new URLs. The dataset-update utility shows how the system might evolve incrementally while still controlling label quality. Together, these components make the project suitable for reproduction by another student, examiner, or developer.
    """, styles)
    story.append(base.flowchart_drawing())
    story.append(Paragraph("Figure 1. Overall workflow of the rebuilt phishing URL detection project.", styles["Caption"]))

    add_subsection(story, "B. Data Collection Methods", f"""
    Data were collected from the supplied CSV file stored in the project folder. The file contains {stats["total_rows"]:,} rows with two columns: URL and Label. Labels were normalized to lowercase and mapped to binary form, with good URLs treated as class 0 and bad URLs treated as class 1. Rows with missing label or URL values were excluded. The resulting class distribution was {stats["good_rows"]:,} benign URLs ({stats["good_pct"]:.2f}%) and {stats["bad_rows"]:,} phishing URLs ({stats["bad_pct"]:.2f}%).

    The dataset is large enough to support a substantial supervised learning experiment, but its practical value depends on how it is handled. The rebuilt pipeline treats the CSV not as a static artifact to be inspected manually, but as a formal input to a repeatable process. Every training run reads from the same project-relative location, applies the same cleaning logic, and maps labels through the same binary convention. This consistency matters because differences in ingestion are a common but under-discussed source of irreproducibility in student machine learning projects.

    Descriptively, the corpus contains a mix of short and long URLs, with an average length of {stats["avg_len"]:.2f} characters and a median of {stats["median_len"]:.2f}. This suggests that the model is exposed to both compact web addresses and more heavily structured or tokenized URLs. Such variety is helpful because phishing behavior is not uniform: some campaigns rely on blatant obfuscation, while others depend on visually simple yet strategically misleading links.
    """, styles)
    story.append(base.class_distribution_chart(stats))
    story.append(Paragraph("Figure 2. Class distribution in the supplied phishing URL dataset.", styles["Caption"]))

    add_subsection(story, "C. Sample Selection", """
    The full cleaned dataset was used for the main experiment, and the evaluation split was created through an 80/20 stratified partition so that class proportions were preserved between training and testing subsets. This design was chosen to produce a strong baseline while avoiding sample-selection drift within the single-dataset experiment. A smaller sample-size option remains available in the code for rapid experimentation, but the final reported results come from full-dataset training.

    The decision to use the full dataset rather than a reduced benchmark subset reflects the project’s applied emphasis. In many educational projects, models are trained on small samples for speed, but doing so can hide how the system behaves under realistic class ratios and lexical diversity. By using the full corpus, the present study produces a more credible estimate of how the model handles scale, even though it still remains a single-dataset experiment.

    Stratification was especially important because class imbalance is a known issue in phishing datasets. If the split were not stratified, evaluation metrics could fluctuate simply because the test set happened to contain an easier or harder class distribution. The chosen approach therefore helps stabilize the evaluation and makes the reported metrics easier to interpret.
    """, styles)

    add_subsection(story, "D. Data Analysis Techniques", f"""
    Nineteen numerical features were extracted from each URL, covering structural length signals, host-related cues, statistical measures such as entropy, and semantic indicators such as suspicious keyword hits and brand misuse. These features were provided to a histogram-based gradient boosting classifier, chosen for its suitability to nonlinear tabular problems and its strong balance between performance and simplicity. Evaluation focused on accuracy, ROC AUC, precision, recall, and F1-score, with particular emphasis on phishing-class recall and F1 because missed phishing URLs are operationally significant.

    The feature-engineering stage can be understood as the analytical heart of the model. Each feature operationalizes a small hypothesis about phishing behavior. For example, subdomain count captures domain disguise depth, entropy captures lexical disorder, suspicious keyword count captures credential-oriented wording, and brand misuse captures identity borrowing. The classifier then learns how these signals interact rather than treating any one of them as decisive in isolation. This is particularly useful because phishing URLs vary widely: some are suspicious for structural reasons, while others are suspicious for semantic reasons.

    The model choice also reflects a methodological compromise. A boosting ensemble can learn nonlinear interactions across tabular features without requiring token embeddings, sequence padding, or expensive GPU-backed training. For the purposes of a major project that must run reliably on an ordinary local machine, this choice is defensible. It does not exclude future deep learning experimentation; rather, it establishes a robust baseline against which more complex models can later be compared.

    From a reproducibility standpoint, the analysis pipeline is intentionally modular. Feature extraction is centralized in a shared source file, model persistence is handled by a dedicated utility, and output metrics are stored in machine-readable form. That modularity is analytically useful because it reduces the risk of hidden divergence between training, testing, and deployment phases. In many small machine learning projects, the real methodological weakness is not the choice of model but the silent mismatch between these phases. The current design explicitly tries to avoid that problem.
    """, styles)
    story.append(base.feature_family_drawing())
    story.append(Paragraph("Figure 3. Feature families used in the final URL classifier.", styles["Caption"]))
    story.append(base.feature_table(stats))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 3. Feature set used in the rebuilt system.", styles["Caption"]))
    feature_groups = wrapped_table(
        [
            ["Feature group", "Examples", "Analytical purpose"],
            ["Structural", "URL length, dots, slashes, hyphens, digits", "Capture visible complexity and suspicious formatting behavior."],
            ["Host-oriented", "Hostname length, subdomain count, IP usage, port flag", "Model routing and domain disguise patterns."],
            ["Semantic", "Suspicious keywords, brand misuse", "Represent phishing intent and impersonation cues."],
            ["Statistical", "Entropy, query count, fragment flag", "Measure irregularity and unusually engineered URL structure."],
        ],
        [4.0 * cm, 5.5 * cm, 6.3 * cm],
        styles
    )
    story.append(feature_groups)
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 4. Analytical grouping of the features used in the methodology.", styles["Caption"]))
    story.append(PageBreak())

    add_section(story, "IV. Results", """
    The rebuilt project trained successfully on the full dataset and produced stable model artifacts and evaluation metrics. The resulting classifier showed strong overall discrimination while also revealing the expected asymmetry between benign-URL recognition and more difficult phishing detection.
    """, styles)

    add_subsection(story, "A. Presentation of Findings", f"""
    The final model achieved an accuracy of {stats["accuracy"]:.4f}, ROC AUC of {stats["roc_auc"]:.4f}, weighted F1-score of {stats["weighted_f1"]:.4f}, and phishing-class F1-score of {stats["bad_f1"]:.4f}. For benign URLs, precision was {stats["good_precision"]:.4f} and recall was {stats["good_recall"]:.4f}. For phishing URLs, precision was {stats["bad_precision"]:.4f} and recall was {stats["bad_recall"]:.4f}. These values demonstrate that the system provides a credible and usable phishing-screening baseline.

    The saved artifacts reinforce the credibility of these findings. The project writes the trained model bundle to the local models directory and stores evaluation outputs in JSON format. This means the reported metrics are not informal observations printed once to the terminal; they are persisted results that can be rechecked, reused, or compared across future experiments. In a research-paper context, that persistence is valuable because it turns the project into a traceable experimental artifact.
    """, styles)
    story.append(base.metrics_chart(stats))
    story.append(Paragraph("Figure 4. Core evaluation metrics for the implemented model.", styles["Caption"]))
    story.append(base.precision_recall_chart(stats))
    story.append(Paragraph("Figure 5. Precision and recall comparison across classes.", styles["Caption"]))
    story.append(wrapped_table(
        [
            ["Metric", "Value", "Interpretive note"],
            ["Accuracy", f"{stats['accuracy']:.4f}", "Shows strong overall correctness but should not be read alone in an imbalanced setting."],
            ["ROC AUC", f"{stats['roc_auc']:.4f}", "Indicates strong ranking ability across decision thresholds."],
            ["Good recall", f"{stats['good_recall']:.4f}", "Suggests benign URLs are recognized very consistently."],
            ["Bad recall", f"{stats['bad_recall']:.4f}", "Shows that phishing detection is strong but still the more difficult class."],
            ["Bad F1-score", f"{stats['bad_f1']:.4f}", "Balances phishing precision and recall, making it one of the most useful safety metrics."],
        ],
        [3.8 * cm, 2.8 * cm, 8.8 * cm],
        styles,
        header_bg="#17384e",
        body_bg2="#eef5fa",
        font_size=10.5,
        leading=13.2
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 5. Summary interpretation of the main reported evaluation metrics.", styles["Caption"]))

    add_subsection(story, "B. Data Analysis and Interpretation", f"""
    The evaluation suggests that the model is especially strong at recognizing benign URLs, while phishing detection remains effective but more challenging. Approximate confusion counts reconstructed from the saved report indicate around {stats["tp_bad"]:,} correctly identified phishing URLs and {stats["fn_bad"]:,} phishing URLs that were missed. This pattern is consistent with the known weakness of lexical-only systems when phishing URLs use cleaner or more plausible structures. It also reinforces the argument that more sophisticated content, visual, or graph-based signals may be needed for edge cases.

    Interpreting the results carefully matters more than restating the numbers. The classifier’s strong benign-class recall indicates that it has learned a fairly stable notion of ordinary URL structure within this dataset. The lower phishing recall, by contrast, suggests that malicious URLs are more heterogeneous and therefore harder to capture with a compact feature set. This asymmetry is common in phishing detection because attackers deliberately balance realism and deception. Some URLs remain obviously suspicious, but others are designed specifically to evade lexical detection.

    The graphs included in this section support that interpretation visually. Overall metrics show that the model is not weak; confusion patterns show that its errors are concentrated where the phishing class becomes less lexically distinctive. Together, the numeric report and visual summaries provide a more complete view of model behavior than accuracy alone could offer.
    """, styles)
    story.append(base.confusion_chart(stats))
    story.append(Paragraph("Figure 6. Approximate confusion-outcome counts from the saved evaluation report.", styles["Caption"]))

    add_subsection(story, "C. Support for the Research Question or Hypothesis", """
    The results support the main research question. A rebuilt lexical-feature-based system can indeed produce meaningful phishing detection performance on the supplied dataset while remaining easy to run and reproduce. At the same time, the findings also support the secondary hypothesis that such a system should be treated as a baseline rather than a complete anti-phishing solution. The evidence therefore supports both the effectiveness and the bounded scope of the project.

    In other words, the project succeeds according to the criteria that were actually set for it. It is not meant to be the most sophisticated anti-phishing architecture in the literature; it is meant to be a functioning, defensible, research-aware implementation of a URL-focused detector. By that standard, the system clearly meets its goals. The stronger claim that phishing is solved universally would not be supported, but the more precise claim that the project establishes a credible and useful baseline is well supported by the evidence.

    This support is further strengthened by the fact that the project can be demonstrated end to end. The same codebase that produced the reported metrics can load the saved model, score new URLs, and manage controlled dataset updates. That continuity between experimentation and use is a meaningful form of evidence in project-centered research because it shows that the findings are attached to a functioning system rather than to a one-off notebook run.

    The section also supports a more subtle conclusion: research questions in cybersecurity are often best answered in qualified rather than absolute terms. The present detector is effective under the experimental conditions documented in the methodology and meaningful in the context established by the literature review. However, it is not presented as a universally optimal detector for every phishing scenario. This balanced interpretation strengthens the paper because it aligns the conclusion with the real scope of the evidence rather than overstating what the model can prove.

    From the perspective of project evaluation, this alignment between question, method, and result is important. A strong major project is not simply one that produces a favorable number, but one in which the claims are proportional to the evidence. The current study meets that standard by showing both what the system can do and where its present architecture remains limited.
    """, styles)
    story.append(PageBreak())

    add_section(story, "V. Discussion", """
    The discussion interprets the project not as a claim of universal phishing detection, but as a careful demonstration of what a well-built baseline can accomplish. Its contribution lies in bridging code repair, machine learning implementation, and literature-aware interpretation inside one coherent project.
    """, styles)

    add_subsection(story, "A. Interpretation of Results", """
    The results indicate that a lightweight tabular approach remains viable. Features such as entropy, suspicious keyword usage, IP-address detection, and host complexity still capture enough phishing structure to support strong overall classification. This validates the design choice of using a low-dependency feature pipeline rather than relying immediately on heavier deep learning or browser-rendered analysis.

    This interpretation should be understood in systems terms rather than as a narrow algorithmic claim. The value of the current project lies in the combination of performance, transparency, and ease of execution. A model that can be trained quickly, reasoned about clearly, and reused across scripts offers a strong educational and prototyping advantage. Those qualities matter in cybersecurity, where detection tools must often be reviewed, explained, and adapted under practical constraints.
    """, styles)

    add_subsection(story, "B. Comparison with Existing Literature", f"""
    Compared with high-performing published systems, the current project does not claim state-of-the-art status. Studies using XGBoost, random forests with richer features, or hybrid URL+HTML pipelines often report stronger top-line results {base.cite(5,8,12,38)}. Deep learning models and graph-based systems also offer stronger generalization in some scenarios {base.cite(18,19,20,23,25,28,29,32)}. However, the present project remains competitive as a reproducible and lightweight baseline because it avoids many of the external dependencies that make such systems harder to deploy or explain.

    This comparison is important for academic honesty. It is easy for project reports to quote the best numbers from unrelated papers and treat them as direct benchmarks. The current paper avoids that mistake by emphasizing the differences in dataset scope, feature richness, model family, and deployment assumptions. A strong hybrid or transformer system may be the better choice in a production environment with sufficient infrastructure. Yet that does not reduce the value of a compact baseline that can be trained locally and understood by students or reviewers. The two kinds of systems serve different but complementary purposes.
    """, styles)

    add_subsection(story, "C. Implications and Limitations of the Study", """
    The study has both practical implications and clear limitations. Practically, it shows that a student project can become a usable anti-phishing baseline when the code, data flow, and evaluation are cleaned up properly. It also suggests that lightweight classifiers can serve as first-stage filters in layered cybersecurity pipelines. The limitations are equally important: the study uses one dataset, one main model family, and a feature set limited to URL-level evidence. Therefore, the reported results should not be interpreted as universal evidence of phishing detection performance under all conditions.

    The implications extend beyond the project itself. For instructors and reviewers, the paper demonstrates a way to assess cybersecurity machine learning work holistically. Instead of asking only whether the model works, one can ask whether the data ingestion is clear, whether the artifacts are saved reliably, whether the evaluation is interpretable, and whether the limitations are acknowledged honestly. In that sense, the present study offers a small methodological example of how project-based machine learning research can be presented responsibly.

    The limitations table below summarizes the main threats to validity in condensed form, but the broader lesson is that every phishing detector occupies a position on a trade-off curve. More context usually increases potential accuracy, but also increases runtime cost, dependency burden, and system complexity. The current project sits deliberately toward the interpretable and deployable side of that curve.
    """, styles)
    story.append(wrapped_table(
        [
            ["Threat", "Why it matters", "Mitigation in this study"],
            ["Dataset shift", "URL patterns may evolve over time and across sources.", "Results are interpreted cautiously and linked to adaptation literature."],
            ["Feature incompleteness", "No HTML, screenshot, or graph context is used.", "The system is framed as a lightweight baseline, not a universal detector."],
            ["Single split evaluation", "One train-test split may not reflect all future distributions.", "The paper emphasizes transparency and recommends further cross-dataset testing."],
        ],
        [3 * cm, 6.5 * cm, 6.4 * cm],
        styles
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 6. Condensed summary of major study limitations and mitigations.", styles["Caption"]))
    add_subsection(story, "D. Extended Recommendations for Practice", f"""
    Although the formal outline provided by the user ends the discussion section with implications and limitations, the practical interpretation of those limitations suggests several immediate recommendations for practice. First, organizations or project users should treat lexical phishing detection as a screening layer rather than as the final authority. Second, any deployment should preserve model versioning and metrics logging so that retraining over time can be audited. Third, if the system is adapted into a user-facing application, warning design should communicate uncertainty rather than implying that every output is absolute.

    These practical recommendations align with the literature’s broader message that phishing defense is most effective when multiple signals are combined thoughtfully {base.cite(4,8,19,20,32,38)}. The major project therefore demonstrates a workable first component of a broader architecture. Its main operational strength is speed and simplicity; its main operational limitation is the lack of page-level or infrastructure-level context. Both points are central to understanding how the project might be used responsibly beyond the classroom.

    A further practical recommendation concerns maintenance. Even a well-performing phishing detector should not be treated as static. Campaign styles change, hosting strategies evolve, and attackers quickly imitate benign URL structures once defenders emphasize lexical screening. For that reason, any serious use of the present system should include periodic retraining, comparison of newer metrics against archived runs, and review of false-positive or false-negative patterns that emerge over time. This maintenance perspective transforms the model from a one-time experiment into a sustainable tool.

    Another recommendation is documentation-centered deployment. If the system is integrated into a classroom demonstration, institutional pilot, or small application, the surrounding documentation should explain not only how to run it but how to interpret it. Users should understand that a phishing probability is a model estimate, not a legal or security guarantee. This kind of framing helps prevent overtrust and keeps the system aligned with the ethical caution that appears throughout the broader phishing literature.
    """, styles)
    story.append(PageBreak())

    add_section(story, "VI. Conclusion", """
    The rebuilt phishing URL detection project successfully demonstrates the core lifecycle of a machine learning security tool: data preparation, feature engineering, model training, evaluation, artifact storage, and inference on new inputs. By combining these implementation steps with a structured literature review, the paper presents a project report that is both technically grounded and academically defensible.
    """, styles)

    add_subsection(story, "A. Summary of Key Findings", f"""
    The key findings are that the rebuilt system is fully functional, reproducible, and capable of strong phishing URL screening on the supplied dataset. The model reached an accuracy of {stats["accuracy"]:.4f} and ROC AUC of {stats["roc_auc"]:.4f}, confirming that compact handcrafted URL features still hold significant predictive value.

    A second key finding is that project quality depends on more than classifier choice. The repaired scripts, cleaned data flow, shared feature contract, and saved artifacts were all necessary for the final system to become academically defensible. This is an important outcome because it demonstrates that implementation discipline is part of research quality rather than a separate concern.
    """, styles)

    add_subsection(story, "B. Contributions to the Field", """
    The main contribution of the project is not a novel anti-phishing algorithm, but a disciplined case study that demonstrates how incomplete project code can be transformed into a coherent research artifact. This contributes to the field by emphasizing reproducibility, transparency, and honest baseline construction in phishing detection work.

    It also contributes by showing how literature and implementation can be integrated in a major project. Many reports either summarize papers without building anything concrete or build models without interpreting them in a scholarly context. The present outline-format paper deliberately combines both activities, making it more useful as an academic document and as a project-defense resource.
    """, styles)

    add_subsection(story, "C. Recommendations for Future Research", f"""
    Future research should evaluate the same pipeline under temporal drift, multiple external datasets, and adversarially altered URLs. It should also explore staged architectures that combine the current lexical classifier with HTML, visual, certificate, or graph-based analysis {base.cite(14,19,20,32,38)}. From a deployment perspective, the model could be embedded into a desktop utility, browser extension, or web service for live URL screening and user-facing explanation.

    More broadly, future work should examine not only how to improve the classifier, but also how to improve the user experience of phishing warnings. End-user tools benefit when they explain why a link is risky rather than simply stating that it is dangerous. Integrating interpretable cues, calibrated probabilities, and warning design research could help turn the present baseline into a more human-centered security tool. This would connect the machine learning core of the project with the broader usability dimension of anti-phishing defense.
    """, styles)

    add_section(story, "VIII. Research Notes and Source Integration", """
    The following short notes explain how the scholarly references informed the structure of the current paper. This section is included to preserve the requested outline-oriented style while still demonstrating that the cited works were actively used in shaping the project interpretation rather than being added only as a bibliography. These notes also help extend the paper into a fuller academic artifact by connecting the literature directly to implementation choices.
    """, styles)
    integration_rows = [["Reference cluster", "Role in the current paper"]]
    clusters = [
        ("[1]-[4]", "Used to define the overall research landscape, taxonomy of phishing detection methods, and concerns about reproducibility and dataset comparability."),
        ("[5]-[17]", "Used to justify feature-engineered and classical machine learning baselines, especially lexical URL analysis and lightweight deployable detection."),
        ("[18]-[30]", "Used to compare the project against deep learning, transformer, and recurrent approaches and to frame future work directions."),
        ("[31]-[40]", "Used to discuss visual similarity, hybrid content-based methods, and broader system-level defenses beyond URL-only screening."),
    ]
    for left, right in clusters:
        integration_rows.append([left, right])
    integration = wrapped_table(integration_rows, [3.5 * cm, 12.0 * cm], styles, font_size=10.8, leading=13.5)
    story.append(integration)
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Table 7. How the reference groups were used inside the outline-formatted paper.", styles["Caption"]))
    base.paragraph_block(story, """
    Including this source-integration section serves an academic purpose. In many project reports, references appear only at the end and are not clearly tied to specific design or interpretation decisions. By explicitly grouping the references according to their role in the paper, this section shows how the literature informed the introduction, methodology, evaluation, discussion, and future-work reasoning. It also makes the project easier to defend in an oral presentation because the relationship between cited scholarship and implemented design becomes more visible.

    The section also reinforces a central message of the project: research value is not limited to inventing a new model. It also includes careful synthesis, transparent positioning, and the ability to show why a given design belongs where it does in the wider field. For a major project, that form of integration is especially useful because it demonstrates subject understanding in addition to coding ability.
    """, styles["Body"])

    add_section(story, "IX. References", "", styles)
    for idx, ref in enumerate(base.REFERENCES, start=1):
        line = f'[{idx}] {ref["authors"]}, "{ref["title"]}," {ref["venue"]}, {ref["year"]}. Available: {ref["url"]}. This source was included as part of the research base supporting the design, evaluation, or interpretation of the current project.'
        story.append(Paragraph(line, styles["Reference"]))
    return story


def build_pdf():
    stats = base.load_project_data()
    styles = base.make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=base.A4,
        leftMargin=2.45 * cm,
        rightMargin=2.45 * cm,
        topMargin=2.1 * cm,
        bottomMargin=2.1 * cm,
    )
    story = build_story(stats, styles)
    doc.build(story, onFirstPage=base.add_page_number, onLaterPages=base.add_page_number)


if __name__ == "__main__":
    build_pdf()
