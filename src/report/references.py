"""
APA 7 reference list for the interim report.

One pattern per source type, applied consistently:
  Journal:      Author, A. A., & Author, B. B. (Year). Title in sentence case. <i>Journal Name, Vol</i>(Issue), pages. https://doi.org/...
  Proceedings:  Author, A. A. (Year). Title in sentence case. In <i>Proceedings title</i> (pp. x–y). Publisher. https://doi.org/...
  Preprint:     Author, A. A. (Year). <i>Title in sentence case</i> (arXiv:xxxx.xxxxx). arXiv. https://doi.org/10.48550/arXiv.xxxx.xxxxx
  Book:         Author, A. A. (Year). <i>Title in sentence case</i> (ed.). Publisher. https://doi.org/...
Every entry is cited in the text and every in-text citation appears here.
"""

ACL = "Association for Computational Linguistics"

REFERENCES = [
    "Acikgoz, E. C., Guo, C., Dey, S., Datta, A., Kim, T., Tur, G., & Hakkani-Tür, D. (2025). TD-EVAL: Revisiting "
    "task-oriented dialogue evaluation by combining turn-level precision with dialogue-level comparisons. In "
    "<i>Proceedings of the 26th Annual Meeting of the Special Interest Group on Discourse and Dialogue</i> "
    f"(pp. 113–132). {ACL}. https://doi.org/10.18653/v1/2025.sigdial-1.7",

    "Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., "
    "Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D. M., "
    "Wu, J., Winter, C., . . . Amodei, D. (2020). Language models are few-shot learners. In <i>Advances in Neural "
    "Information Processing Systems</i> (Vol. 33, pp. 1877–1901). Curran Associates. "
    "https://doi.org/10.48550/arXiv.2005.14165",

    "Budzianowski, P., Wen, T.-H., Tseng, B.-H., Casanueva, I., Ultes, S., Ramadan, O., & Gašić, M. (2018). MultiWOZ: "
    "A large-scale multi-domain Wizard-of-Oz dataset for task-oriented dialogue modelling. In <i>Proceedings of the "
    f"2018 Conference on Empirical Methods in Natural Language Processing</i> (pp. 5016–5026). {ACL}. "
    "https://doi.org/10.18653/v1/D18-1547",

    "Buhalis, D., & Sinarta, Y. (2019). Real-time co-creation and nowness service: Lessons from tourism and "
    "hospitality. <i>Journal of Travel & Tourism Marketing, 36</i>(5), 563–582. "
    "https://doi.org/10.1080/10548408.2019.1592059",

    "Cohen, J. (1988). <i>Statistical power analysis for the behavioral sciences</i> (2nd ed.). Lawrence Erlbaum "
    "Associates. https://doi.org/10.4324/9780203771587",

    "Davies, D. L., & Bouldin, D. W. (1979). A cluster separation measure. <i>IEEE Transactions on Pattern Analysis "
    "and Machine Intelligence, PAMI-1</i>(2), 224–227. https://doi.org/10.1109/TPAMI.1979.4766909",

    "El Asri, L., Schulz, H., Sharma, S., Zumer, J., Harris, J., Fine, E., Mehrotra, R., & Suleman, K. (2017). "
    "Frames: A corpus for adding memory to goal-oriented dialogue systems. In <i>Proceedings of the 18th Annual "
    f"SIGdial Meeting on Discourse and Dialogue</i> (pp. 207–219). {ACL}. https://doi.org/10.18653/v1/W17-5526",

    "Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis "
    "program for the social, behavioral, and biomedical sciences. <i>Behavior Research Methods, 39</i>(2), 175–191. "
    "https://doi.org/10.3758/BF03193146",

    "Gilardi, F., Alizadeh, M., & Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. "
    "<i>Proceedings of the National Academy of Sciences, 120</i>(30), Article e2305016120. "
    "https://doi.org/10.1073/pnas.2305016120",

    "Greenhouse, S. W., & Geisser, S. (1959). On methods in the analysis of profile data. <i>Psychometrika, 24</i>(2), "
    "95–112. https://doi.org/10.1007/BF02289823",

    "Hennig, C. (2007). Cluster-wise assessment of cluster stability. <i>Computational Statistics & Data Analysis, "
    "52</i>(1), 258–271. https://doi.org/10.1016/j.csda.2006.11.025",

    "Hubert, L., & Arabie, P. (1985). Comparing partitions. <i>Journal of Classification, 2</i>(1), 193–218. "
    "https://doi.org/10.1007/BF01908075",

    "Inaba, M., Chiba, Y., Higashinaka, R., Komatani, K., Miyao, Y., & Nagai, T. (2022). Collection and analysis of "
    "travel agency task dialogues with age-diverse speakers. In <i>Proceedings of the Thirteenth Language Resources "
    "and Evaluation Conference</i> (pp. 5759–5767). European Language Resources Association. "
    "https://aclanthology.org/2022.lrec-1.619",

    "Ivanov, S., & Webster, C. (2019). Conceptual framework of the use of robots, artificial intelligence and service "
    "automation in travel, tourism, and hospitality companies. In <i>Robots, artificial intelligence, and service "
    "automation in travel, tourism and hospitality</i> (pp. 7–37). Emerald Publishing Limited. "
    "https://doi.org/10.1108/978-1-78756-687-320191001",

    "Jannach, D., Manzoor, A., Cai, W., & Chen, L. (2021). A survey on conversational recommender systems. <i>ACM "
    "Computing Surveys, 54</i>(5), Article 105. https://doi.org/10.1145/3453154",

    "Johnson, J., Douze, M., & Jégou, H. (2021). Billion-scale similarity search with GPUs. <i>IEEE Transactions on "
    "Big Data, 7</i>(3), 535–547. https://doi.org/10.1109/TBDATA.2019.2921572",

    "Lee, J., Chen, F., Dua, S., Cer, D., Shanbhogue, M., Naim, I., Hernández Ábrego, G., Li, Z., Chen, K., "
    "Schechter Vera, H., Ren, X., Zhang, S., Salz, D., Boratko, M., Han, J., Chen, B., Huang, S., Rao, V., "
    "Suganthan, P., . . . Duerig, T. (2025). <i>Gemini embedding: Generalizable embeddings from Gemini</i> "
    "(arXiv:2503.07891). arXiv. https://doi.org/10.48550/arXiv.2503.07891",

    "Liu, J., Shen, D., Zhang, Y., Dolan, B., Carin, L., & Chen, W. (2022). What makes good in-context examples for "
    "GPT-3? In <i>Proceedings of Deep Learning Inside Out (DeeLIO 2022): The 3rd Workshop on Knowledge Extraction and "
    f"Integration for Deep Learning Architectures</i> (pp. 100–114). {ACL}. "
    "https://doi.org/10.18653/v1/2022.deelio-1.10",

    "McInnes, L., Healy, J., & Astels, S. (2017). hdbscan: Hierarchical density based clustering. <i>Journal of Open "
    "Source Software, 2</i>(11), Article 205. https://doi.org/10.21105/joss.00205",

    "McInnes, L., Healy, J., & Melville, J. (2018). <i>UMAP: Uniform manifold approximation and projection for "
    "dimension reduction</i> (arXiv:1802.03426). arXiv. https://doi.org/10.48550/arXiv.1802.03426",

    "Melián-González, S., Gutiérrez-Taño, D., & Bulchand-Gidumal, J. (2021). Predicting the intentions to use "
    "chatbots for travel and tourism. <i>Current Issues in Tourism, 24</i>(2), 192–210. "
    "https://doi.org/10.1080/13683500.2019.1706457",

    "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., "
    "Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. "
    "(2011). Scikit-learn: Machine learning in Python. <i>Journal of Machine Learning Research, 12</i>, 2825–2830. "
    "https://jmlr.org/papers/v12/pedregosa11a.html",

    "Rebedea, T., Dinu, R., Sreedhar, M. N., Parisien, C., & Cohen, J. (2023). NeMo Guardrails: A toolkit for "
    "controllable and safe LLM applications with programmable rails. In <i>Proceedings of the 2023 Conference on "
    f"Empirical Methods in Natural Language Processing: System Demonstrations</i> (pp. 431–445). {ACL}. "
    "https://doi.org/10.18653/v1/2023.emnlp-demo.40",

    "Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. In "
    "<i>Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th "
    f"International Joint Conference on Natural Language Processing</i> (pp. 3982–3992). {ACL}. "
    "https://doi.org/10.18653/v1/D19-1410",

    "Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. "
    "<i>Journal of Computational and Applied Mathematics, 20</i>, 53–65. "
    "https://doi.org/10.1016/0377-0427(87)90125-7",

    "Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. In "
    "<i>Proceedings of the 9th Python in Science Conference</i> (pp. 92–96). SciPy. "
    "https://doi.org/10.25080/Majora-92bf1922-011",

    "Wobbrock, J. O., Findlater, L., Gergle, D., & Higgins, J. J. (2011). The aligned rank transform for "
    "nonparametric factorial analyses using only ANOVA procedures. In <i>Proceedings of the SIGCHI Conference on "
    "Human Factors in Computing Systems</i> (pp. 143–146). Association for Computing Machinery. "
    "https://doi.org/10.1145/1978942.1978963",

    "Yao, S., Shinn, N., Razavi, P., & Narasimhan, K. (2024). <i>τ-bench: A benchmark for tool-agent-user interaction "
    "in real-world domains</i> (arXiv:2406.12045). arXiv. https://doi.org/10.48550/arXiv.2406.12045",

    "Zang, X., Rastogi, A., Sunkara, S., Gupta, R., Zhang, J., & Chen, J. (2020). MultiWOZ 2.2: A dialogue dataset "
    "with additional annotation corrections and state tracking baselines. In <i>Proceedings of the 2nd Workshop on "
    f"Natural Language Processing for Conversational AI</i> (pp. 109–117). {ACL}. "
    "https://doi.org/10.18653/v1/2020.nlp4convai-1.13",

    "Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020). BERTScore: Evaluating text generation "
    "with BERT. In <i>Proceedings of the 8th International Conference on Learning Representations</i>. OpenReview. "
    "https://openreview.net/forum?id=SkeHuCVFDr",
]
